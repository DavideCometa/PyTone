import rtmidi2
from State import State_Singleton
import time
import Constants
from Utils.Logger import Logger
from Modules.Looper import Looper
from Modules.Metronome import Metronome
from pubsub import pub

class MIDI_Manager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MIDI_Manager, cls).__new__(cls, *args, **kwargs)
            cls._instance.state = State_Singleton()
            cls._instance.Looper = Looper()
            cls._instance.Metronome = Metronome()
            cls._instance.midi_out = rtmidi2.MidiOut()
            cls._instance.midi_out.open_port(0) #open all available channels

            cls._instance.setSubscriptions()

        return cls._instance
    
    def setSubscriptions(self):
        pub.subscribe(self.on_send_midi_note, Constants.EV_SEND_MIDI_NOTE)
        pub.subscribe(self.on_send_midi_msg, Constants.EV_SEND_MIDI_MSG)

    def on_send_midi_note(self, data):
        channel, note, velocity = data['channel'], data['note'], data['velocity']
        self.send_midi_note(channel, note, velocity, True)

    def on_send_midi_msg(self, data):
        channel, note, msg = data['channel'], data['note'], data['msg']
        self.send_midi_msg(channel, msg, note, True) 

    def send_midi_note(self, channel, note, velocity, skip_record=False):
        Logger.log('GENERIC',["Note ", note - 60])
        if self.Looper.is_recording and not self.Metronome.looper_warmups and not skip_record:
            self.Looper.record(channel, note, velocity)
        self.midi_out.send_noteon(channel, note, velocity)

    def send_midi_chord(self, n1, n2, n3, n4=None, n5=None):
        current_time = time.perf_counter()
        elapsed_time = current_time - self.state.last_execution_time
        if elapsed_time >= Constants.SLEEP_TIME_BETWEEN_CHORDS: # -> needed in order to avoid spamming the channel with too many MIDI cmds
            if self.state.mute_chords == False:
                # Stop previous chord in case of notes with release/sustain
                self.stop_midi_chord(False)
                Logger.log('GENERIC',["==Playing chord=="])
                self.send_midi_note(Constants.CHORD_CH, n1, 80)
                self.send_midi_note(Constants.CHORD_CH, n2, 80)
                self.send_midi_note(Constants.CHORD_CH, n3, 80)
                if n4:
                    self.send_midi_note(Constants.CHORD_CH, n4, 80)
                if n5:
                    self.send_midi_note(Constants.CHORD_CH, n5, 80)
                Logger.log('GENERIC',["================="])
                self.state.last_execution_time = current_time
    
    def send_midi_msg(self, channel, cmd, note=None, skip_record=False):
        if channel:
            cmd = cmd + channel

        self.midi_out.send_raw(cmd, note, 0)
        if self.Looper.is_recording and not self.Metronome.looper_warmups and not skip_record:
            self.Looper.record(cmd, note)

    def stop_midi_note(self,channel, note):
        self.send_midi_msg(channel, Constants.NOTE_OFF, note)

    def stop_midi_chord(self, stop_curr = True):
        target_notes = self.state.curr_chord_notes if stop_curr else self.state.prev_chord_notes
        self.send_midi_msg(Constants.CHORD_CH, Constants.NOTE_OFF, target_notes[0])
        self.send_midi_msg(Constants.CHORD_CH, Constants.NOTE_OFF, target_notes[1])
        self.send_midi_msg(Constants.CHORD_CH, Constants.NOTE_OFF, target_notes[2])
        self.send_midi_msg(Constants.CHORD_CH, Constants.NOTE_OFF, target_notes[3])
        if len(target_notes) > 4:
            self.send_midi_msg(Constants.CHORD_CH, Constants.NOTE_OFF, target_notes[4])

    # def stop_channel(self, channel):
    #     self.send_midi_msg(channel, Constants.CHANNEL_STOP, 0)
