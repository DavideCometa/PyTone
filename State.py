class State_Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(State_Singleton, cls).__new__(cls, *args, **kwargs)
            cls._instance.curr_chord_num = 0
            cls._instance.prev_chord_notes = [60,64,67,71]
            cls._instance.curr_chord_notes = [60,64,67,71] # starting chord for arp -> C
            cls._instance.chord_variation_type = [0]
            cls._instance.curr_bass_note = 60
            cls._instance.auto_bass = False
            cls._instance.auto_bass_type = [0]
            cls._instance.root_note = 60
            cls._instance.scale = 0 #==> Major
            cls._instance.last_execution_time = 0
            cls._instance.mute_chords = False
            cls._instance.curr_beat = 0
            cls._instance.curr_sub_beat = 0

        return cls._instance
    
    #def __init__(self): #this is called each time state is retrieved