from State import State_Singleton
from MIDI_Manager import MIDI_Manager
from Modules.TonalGenerator import TonalGenerator
from pubsub import pub
import Constants

class Arpeggiator:
    def __init__(self):
        self.state = State_Singleton()
        self.midi = MIDI_Manager()
        self.is_playing = False
        self.warming_up = False
        self.TonalGen = TonalGenerator()
        self.type = 0
        self.note_length = 4
        self.curr_arp_note = 0
        pub.subscribe(self.on_sub_beat_event, Constants.EV_SUB_BEAT)
        pub.subscribe(self.on_force_stop, Constants.EV_FORCE_STOP)

    def on_sub_beat_event(self, msg):
        curr_sub_beat = msg
        if self.warming_up and curr_sub_beat == 0:
            self.warming_up = False
            self.start()
        if self.is_playing:
            if curr_sub_beat % self.note_length == 0:
                self.midi.send_midi_note(Constants.ARP_CH, self.TonalGen.get_arp_note(self.get_note_from_type()), 80)
                self.curr_arp_note = (self.curr_arp_note + 1) % 4  # Move to next -> Cycle from 0 to 3

    def warm_up(self):
        self.warming_up = True

    def start(self):
        self.is_playing = True

    def stop(self):
        self.warming_up = False
        self.is_playing = False
        self.curr_arp_note = 0

    def toggle(self):
        if self.is_playing:
            self.stop()
        else:
            self.warm_up()
        
    def on_force_stop(self):
        self.stop()

    def get_note_from_type(self):
        if self.type == 0:
            return self.curr_arp_note
        elif self.type == 1:
            return self.curr_arp_note % 2
        elif self.type == 2:
            return self.curr_arp_note % 1
        elif self.type == 3:
            return self.curr_arp_note % 1
        elif self.type == 4:
            return self.curr_arp_note % 1
    
    def change_type(self, value):
        self.type = int(value)

    def change_note_lenght(self, value):
        self.note_length = Constants.SPEEDS[int(value)]
