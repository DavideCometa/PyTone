import time
from Utils.Logger import Logger
from Modules.Metronome import Metronome
import Constants
import threading
from pubsub import pub

class Looper:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Looper, cls).__new__(cls, *args, **kwargs)
            cls._instance.sequence = [[] for _ in range(Constants.BAR_LENGTH * Constants.SUB_BEATS_PER_BEAT * Constants.LOOPER_BARS)] 
            cls._instance.Metronome = Metronome()
            cls._instance.is_recording = False
            cls._instance.is_playing = False
            cls._instance.curr_looper_sub_beat = 0
            cls._instance.looper_length = Constants.BAR_LENGTH * Constants.LOOPER_BARS
            
            pub.subscribe(cls._instance.on_sub_beat_event, Constants.EV_SUB_BEAT)
            pub.subscribe(cls._instance.on_force_stop, Constants.EV_FORCE_STOP)
        return cls._instance
    
    def record(self, msg_or_channel, note, velocity=None):
        midi_msg = {
            'msg': msg_or_channel if msg_or_channel > Constants.NUM_CHANNELS else None,
            'note': note,
            'channel': msg_or_channel if msg_or_channel <= Constants.NUM_CHANNELS else None,
            'velocity': velocity
        }
        self.sequence[self.curr_looper_sub_beat].append(midi_msg)
        Logger.log('LOOPER',["Recorded: {", msg_or_channel, ", ", note, ", ", velocity, "}"])
            
    
    def toggle_play(self):
        if not self.is_playing:
            print("Goin to play this ", self.sequence)
            self.is_recording = False # TODO then remove this
            self.Metronome.toggle_metronome(True)

        self.curr_looper_sub_beat = 0
        self.is_playing = not self.is_playing
        pub.sendMessage(Constants.EV_PLAY, msg=self.is_playing)

    def process_sequence(self):
        self.process_next_beat(self.sequence[self.curr_looper_sub_beat])

    def process_next_beat(self, beat_data):
        for data in beat_data:
            msg_type = Constants.EV_SEND_MIDI_MSG if data['msg'] else Constants.EV_SEND_MIDI_NOTE
            pub.sendMessage(msg_type, data=data)
        Logger.log('LOOPER', ["Step processed"])
    

    def toggle_recording(self):
        if self.is_recording == True:
            self.Metronome.looper_warmups = 0
            self.Metronome.toggle_metronome(False, True) # forceStop
        else:
            self.clear()
            self.Metronome.looper_warmups = 5
            self.Metronome.toggle_metronome(True)

        self.is_recording = not self.is_recording
        pub.sendMessage(Constants.EV_RECORD, msg=self.is_recording)

    def clear(self, channel=None):
        self.sequence = [[] for _ in range(Constants.BAR_LENGTH * Constants.SUB_BEATS_PER_BEAT * Constants.LOOPER_BARS)] 
        self.curr_looper_sub_beat = 0

    def on_sub_beat_event(self, msg):   
        if (not self.is_playing and not self.is_recording) or (self.is_recording and self.Metronome.looper_warmups != 0):
            Logger.log('LOOPER',["Update while not playing/recording"])
            return
        
        if self.is_playing:
            Logger.log('LOOPER',["Playing sub_beat"])
            threading.Thread(target=self.process_sequence).start() # TODO fix timing of the beep -> try increasing bpm

        self.curr_looper_sub_beat += 1
        if self.curr_looper_sub_beat == (self.looper_length * Constants.SUB_BEATS_PER_BEAT) - 1: # equals end of looper's loop
            if self.is_recording:
                Logger.log('LOOPER',["Stopped recording"])
                self.toggle_recording()

            self.curr_looper_sub_beat = 0      

    def on_force_stop(self):
        return