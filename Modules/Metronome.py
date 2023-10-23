import time
import threading
from UI.LED import LED
from Utils.Logger import Logger
import Constants
from State import State_Singleton
from pubsub import pub
import os

class Metronome:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Metronome, cls).__new__(cls, *args, **kwargs)
            cls._instance.tempo = 120  # initial bpm
            cls._instance.is_active = False
            cls._instance.LED = LED()
            cls._instance.state = State_Singleton()
            cls._instance.is_sound_on = True
            cls._instance.looper_warmups = 0
        return cls._instance

    def start(self):
        self.is_active = True
        self.reset()
        self.tick()
        Logger.log('METRONOME',["Metronome Started"])
        
    def stop(self):
        self.is_active = False
        self.reset()
        pub.sendMessage(Constants.EV_FORCE_STOP)
        Logger.log('METRONOME',["Metronome Stopped"])

    def reset(self):
        self.state.curr_beat = 0
        self.state.curr_sub_beat = 0

    def set_tempo(self, value):
        self.tempo = int(value)

    def tick(self):
        while self.is_active:
            self.state.curr_beat = self.state.curr_sub_beat // Constants.SUB_BEATS_PER_BEAT

            # Notify sub beats only if metronome is not warming up
            if not self.looper_warmups:
                Logger.log('METRONOME',["Metronome notify tick"])
                pub.sendMessage(Constants.EV_SUB_BEAT, msg=self.state.curr_sub_beat)

            if self.state.curr_sub_beat % Constants.SUB_BEATS_PER_BEAT == 0: # Do this only for main beats
                if self.is_sound_on or self.looper_warmups:
                    if self.looper_warmups:
                        self.looper_warmups -= 1
                    threading.Thread(target=self.play_beep).start() # TODO fix timing of the beep -> increase thread priority
                    pub.sendMessage(Constants.EV_BEAT, msg=self.state.curr_beat)
                
                self.LED.flash(self.state.curr_beat == 0)

            # Update curr_sub_beat
            self.state .curr_sub_beat = (self.state.curr_sub_beat + 1) % Constants.TOT_SUB_BEATS_PER_BAR  # Cycle from 0 to 31
            time.sleep((60.0 / self.tempo) / Constants.SUB_BEATS_PER_BEAT)  # Sleep until next sub beat

    def toggle_metronome(self, forceActive=False, forceStop=False):
        if not self.is_active:
            threading.Thread(target=self.start).start()
        elif not forceActive or forceStop:
            self.stop()

    def play_beep(self):
        if os.name == 'posix':
            os.system('osascript -e "beep"')
        else:
            print("Beep sound not supported on this platform.") # works only on unix kernel