from UI.UI import UI
import tkinter as tk
import Constants
from Modules.TonalGenerator import TonalGenerator
from Modules.Metronome import Metronome
from Modules.Looper import Looper
from State import State_Singleton
from Modules.Arpeggiator import Arpeggiator
from MIDI_Manager import MIDI_Manager
from pubsub import pub

class Controller:
    def __init__(self):
        self.state = State_Singleton()
        self.root = tk.Tk()
        self.root.title("PyTONE Controller")
        self.UI = UI(self.root)
        self.TonalGen = TonalGenerator()
        self.Arpeggiator = Arpeggiator()
        self.Looper = Looper()
        self.MIDI_Manager = MIDI_Manager()
        self.Metronome = Metronome()

        self._setButtonsCommands()
        self.root.bind('<KeyPress>', self.on_key_press) # set key press listener and execute key related cmd
    
    def _setButtonsCommands(self):
        for i, key_btn in enumerate(self.UI.piano_keys):
            key_btn.config(command=lambda i=i: self.play_chord(i)) 
        self.UI.c8_btn.config(command=lambda: self.play_chord(0, True))
        self.UI.c9_btn.config(command=lambda: self.play_chord(1, True))
        self.UI.c10_btn.config(command=lambda: self.play_chord(2, True))
        self.UI.c11_btn.config(command=lambda: self.play_chord(3, True))

        self.UI.bass_btn.config(command=lambda: self.play_bass(0))
        self.UI.bass_on_third_btn.config(command=lambda: self.play_bass(2))

        self.UI.tone_inc_btn.config(command=lambda: self.switch_tone(1))
        self.UI.tone_dec_btn.config(command=lambda: self.switch_tone(-1))

        self.UI.minor_btn.config(command=lambda: self.update_scale(1))
        self.UI.major_btn.config(command=lambda: self.update_scale(0))

        self.UI.stop_btn.config(command=lambda: self.stop())
        self.UI.record_btn.config(command=lambda: self.Looper.toggle_recording())
        self.UI.play_btn.config(command=lambda: self.Looper.toggle_play())
        self.UI.metronome_btn.config(command=lambda: self.Metronome.toggle_metronome())
        self.UI.tick_sound_trigger.config(command= lambda: self.toggle_metronome_mute())
        self.UI.tempo_slider.set(self.Metronome.tempo)
        self.UI.tempo_slider.config(command=self.Metronome.set_tempo)

        self.UI.arp_toggle.config(command=lambda: self.Arpeggiator.toggle())

        self.UI.arp_type_slider.set(self.Arpeggiator.type)
        self.UI.arp_type_slider.config(command=self.Arpeggiator.change_type)

        self.UI.arp_speed_slider.set(2)
        self.UI.arp_speed_slider.config(command=self.Arpeggiator.change_note_lenght)

        self.UI.bass_auto_trigger_btn.config(command=self.toggle_auto_bass)
        self.UI.bass_auto_trigger_type.link_var(self.state.auto_bass_type)
        self.UI.chord_variation_type.link_var(self.state.chord_variation_type)

    def on_key_press(self, event):
        if event.keysym.isupper():
            self.state.mute_chords = True
        else:
            self.state.mute_chords = False

        keysym = event.keysym.lower()

        key_mapping = {
            "a": self.UI.piano_keys[0].invoke,
            "s": self.UI.piano_keys[1].invoke,
            "d": self.UI.piano_keys[2].invoke,
            "f": self.UI.piano_keys[3].invoke,
            "g": self.UI.piano_keys[4].invoke,
            "h": self.UI.piano_keys[5].invoke,
            "j": self.UI.piano_keys[6].invoke,
            "w": self.UI.c8_btn.invoke,
            "e": self.UI.c9_btn.invoke,
            "t": self.UI.c10_btn.invoke,
            "y": self.UI.c11_btn.invoke,
            "o": self.UI.tone_dec_btn.invoke,
            "p": self.UI.tone_inc_btn.invoke,
            "n": self.UI.bass_btn.invoke,
            "m": self.UI.bass_on_third_btn.invoke,
            "space": self.UI.stop_btn.invoke
        }

        if keysym in key_mapping:
            key_mapping[keysym]()
    
    def play_bass(self, target):
        self.stop_bass()
        bass_note = self.state.curr_bass_note = self.TonalGen.get_bass_note(target)
        self.MIDI_Manager.send_midi_note(Constants.BASS_CH, bass_note, 100)

    def stop_bass(self):
        self.MIDI_Manager.stop_midi_note(Constants.BASS_CH, self.state.curr_bass_note)

    def switch_tone(self, offset):
        self.state.root_note += offset
        if(self.state.root_note >= Constants.START_KEY + Constants.OCTAVE_OFFSET or self.state.root_note <= Constants.START_KEY - Constants.OCTAVE_OFFSET):
            self.state.root_note = Constants.START_KEY

    def update_scale(self, scale):
        self.state.scale = scale

    def stop(self):
        self.MIDI_Manager.stop_midi_chord()
        self.stop_bass()
        self.Metronome.stop()

    def toggle_auto_bass(self):
        if self.UI.bass_auto_trigger_btn.config('relief')[-1] == 'sunken':
            self.UI.bass_auto_trigger_btn.config(relief="raised")
            self.UI.bass_auto_trigger_btn.config(text="OFF", background='red')
            self.state.auto_bass = False
            self.stop_bass()
        else:
            self.UI.bass_auto_trigger_btn.config(relief="sunken")
            self.UI.bass_auto_trigger_btn.config(text="ON", background='green')
            self.state.auto_bass = True
 
    def play_chord(self, chord_index, is_additional = False):

        if self.state.chord_variation_type[0] == 0:
            chord_type = 3
        elif self.state.chord_variation_type[0] == 1:
            chord_type = 4
        elif self.state.chord_variation_type[0] >= 2:
            chord_type = 5

        if is_additional:
            self.MIDI_Manager.send_midi_chord(*self.TonalGen.get_additional_major(chord_index)[:chord_type]) 
        else:
            self.MIDI_Manager.send_midi_chord(*self.TonalGen.get_chord(chord_index)[:chord_type])
        
        if self.state.auto_bass:
            self.play_bass(self.state.auto_bass_type[0])

    def toggle_metronome_mute(self):
        if self.Metronome.is_sound_on:
            self.UI.tick_sound_trigger.config(text="🔇")
        else:
            self.UI.tick_sound_trigger.config(text="🔉")

        setattr(self.Metronome, 'is_sound_on', not self.Metronome.is_sound_on)