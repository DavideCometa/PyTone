import tkinter as tk
from UI.LED import LED
from UI.Knob import Knob
import Constants
from tkinter import font
from pubsub import pub

class UI:

    @property
    def S_BUTTON_W(self):
        return 1

    @property
    def BUTTON_W(self):
        return 3
    
    @property
    def SMALL_BTN_DIM(self):
        return 3

    @property
    def MEDIUM_BTN_DIM(self):
        return 6

    @property
    def BUTTON_H(self):
        return 12
    
    @property
    def S_BUTTON_H(self):
        return 5

    def __init__(self, root):
        self.tempo = 60  # beats per minute
        self.is_playing = False
        # 3 FRAMES
        self.top = tk.Frame(root)
        self.top.pack(side="top", fill="both", expand=True)
        self.middle = tk.Frame(root)
        self.middle.pack(side="top", fill="both", expand=True)
        self.piano = tk.Frame(root)
        self.piano.pack(side="bottom", fill="both", expand=True)
        self.piano_keys = []

        self.font_L = font.Font(size=26)

        self.createChordsButton()
        self.setSubscriptions()

    def createChordsButton(self):

######## Top ########
        self.stop_btn = tk.Button(self.top, text="⏹", width=self.BUTTON_W, height=self.BUTTON_W)
        self.stop_btn.grid(row=0, column=10)
        self.record_btn = tk.Button(self.top, text="⏺", width=self.BUTTON_W, height=self.BUTTON_W)
        self.record_btn.grid(row=0, column=11)
        self.play_btn = tk.Button(self.top, text="⏵", width=self.BUTTON_W, height=self.BUTTON_W)
        self.play_btn.grid(row=0, column=12)

        self.metronome_btn = tk.Button(self.top, text="🕑", width=self.BUTTON_W, height=self.BUTTON_W)
        self.metronome_btn.grid(row=1, column=0)
        self.tick_sound_trigger = tk.Button(self.top, text="🔉", width=self.S_BUTTON_W, relief="raised")
        self.tick_sound_trigger.grid(row=2, column=0)
        tk.Label(self.top, text="BPM").grid(row=0, column=2)
        self.tempo_slider = tk.Scale(self.top, from_=20, to=220, orient=tk.HORIZONTAL)
        self.tempo_slider.grid(row=1, column =2)

        self.led = LED()
        self.led.initialize(self.top)

        ######## ARP ########
        self.arp_toggle = tk.Button(self.top, text="Arpeggiator", width=self.MEDIUM_BTN_DIM, height=self.SMALL_BTN_DIM)
        self.arp_toggle.grid(row=1, column=3)
        tk.Label(self.top, text="Type").grid(row=2, column=3)
        self.arp_type_slider = tk.Scale(self.top, from_=0, to=4, orient=tk.HORIZONTAL)
        self.arp_type_slider.grid(row=3, column =3)

        tk.Label(self.top, text="Speed").grid(row=4, column=3)
        self.arp_speed_slider = tk.Scale(self.top, from_=1, to=len(Constants.SPEEDS)-1, orient=tk.HORIZONTAL)
        self.arp_speed_slider.grid(row=5, column =3)

        self.top.columnconfigure(4, weight=1)

        ######## Tone section ########
        self.tone_inc_btn = tk.Button(self.top, text="Tone +", width=self.MEDIUM_BTN_DIM, height=self.SMALL_BTN_DIM)
        self.tone_inc_btn.grid(row=6, column=13)
        self.tone_dec_btn = tk.Button(self.top, text="Tone -", width=self.MEDIUM_BTN_DIM, height=self.SMALL_BTN_DIM)
        self.tone_dec_btn.grid(row=6, column=12)

        ######## Scale section ########
        self.minor_btn = tk.Button(self.top, text="Minor Scale", width=self.MEDIUM_BTN_DIM, height=self.SMALL_BTN_DIM)
        self.minor_btn.grid(row=7, column=12)
        self.major_btn = tk.Button(self.top, text="Major Scale", width=self.MEDIUM_BTN_DIM, height=self.SMALL_BTN_DIM)
        self.major_btn.grid(row=7, column=13)

######## Middle #######
        #tk.Label(self.middle, text="** This is just a test for the middle frame **").grid(row=0, column=1)
        self.chord_variation_type = Knob(self.middle, 1, 1, 8, Constants.CHORD_QUALIFIERS)

######## Piano #######

        ######## Chords section ########
        for i, note in enumerate(Constants.CHORDS):
            key = tk.Button(self.piano, text=note, width=self.BUTTON_W, height=self.BUTTON_H)
            key.grid(row=2, column=i)
            self.piano_keys.append(key)
        self.c8_btn = tk.Button(self.piano, text="1st M", width=self.S_BUTTON_W, height=self.S_BUTTON_H, bg='#ffb3fe', fg="black")
        self.c8_btn.place(x=40, y=0)
        self.c9_btn = tk.Button(self.piano, text="2nd M", width=self.S_BUTTON_W, height=self.S_BUTTON_H, bg="black", fg="black")
        self.c9_btn.place(x=105, y=0)
        self.c10_btn = tk.Button(self.piano, text="3rd M", width=self.S_BUTTON_W, height=self.S_BUTTON_H, bg="black", fg="black")
        self.c10_btn.place(x=230, y=0)
        self.c11_btn = tk.Button(self.piano, text="4th M", width=self.S_BUTTON_W, height=self.S_BUTTON_H, bg="black", fg="black")
        self.c11_btn.place(x=292, y=0)
        self.c12_btn = tk.Button(self.piano, text="***", width=self.S_BUTTON_W, height=self.S_BUTTON_H, bg="black", fg="black")
        self.c12_btn.place(x=355, y=0)

        ######## Bass section ########
        tk.Label(self.piano, text="Bass section").grid(row=4, column=12)
        self.bass_auto_trigger_type = Knob(self.piano, 5, 10, 4)
        self.bass_auto_trigger_btn = tk.Button(self.piano, text="A", width=self.S_BUTTON_W, relief="raised")
        self.bass_auto_trigger_btn.grid(row=5, column=11)
        self.bass_btn = tk.Button(self.piano, text="Bass on key", width=self.MEDIUM_BTN_DIM, height=self.SMALL_BTN_DIM)
        self.bass_btn.grid(row=5, column=12)
        self.bass_on_third_btn = tk.Button(self.piano, text="Bass on third", width=self.MEDIUM_BTN_DIM, height=self.SMALL_BTN_DIM)
        self.bass_on_third_btn.grid(row=5, column=13)

    def setSubscriptions(self):
        pub.subscribe(self.setRecordText, Constants.EV_RECORD)
        pub.subscribe(self.setPlayText, Constants.EV_PLAY)

    def setRecordText(self, msg):
        self.record_btn.config(text="⏺ ON" if msg else "⏺")

    def setPlayText(self, msg):
        self.play_btn.config(text="⏵ ON" if msg else "⏵")