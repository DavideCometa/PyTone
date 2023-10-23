##################### CONFIGS #####################
IS_LOG_ACTIVE = True
LOGGER_TYPES = {
    'LOOPER': True,
    'METRONOME': True,
    'GENERIC': False
}
OCTAVE_OFFSET = 12
START_KEY = 60
SLEEP_TIME_BETWEEN_CHORDS = 0.2  # 200 milliseconds = 0.2 seconds -> TODO check if really necessary or can be reduced
BAR_LENGTH = 4 # 4 beats
SUB_BEATS_PER_BEAT = 8
TOT_SUB_BEATS_PER_BAR = BAR_LENGTH * SUB_BEATS_PER_BEAT

LOOPER_BARS = 3 # TEMP
LOOPER_WARMUPS = 5 # 4 + 1 to avoid notify for sub_beats during the last beat (while warmups are set to 0) TODO fix by checking for -1 on warmups

SPEEDS = [0, 2, 4, 8, 16]

CHORDS = ["I", "II", "III", "IV", "V", "VI", "VII"]



##################### MIDI CHANNELS #####################
NUM_CHANNELS = 16
CHORD_CH = 0
BASS_CH = 1
ARP_CH = 2

##################### MIDI MSG #####################
NOTE_OFF = 0x80
CHANNEL_STOP = 123


# 0 = MAJOR
# 1 = MINOR
# 2 = DIMINISHED
# 3 = HALF_DIMINISHED
# 4 = DOMINANT
################## TONAL HARMONY ##################
TONAL_MAJOR_DOMINANTS = [0,2,4,5,7,9,11]
TONAL_MINOR_DOMINANTS = [0,2,3,5,7,8,10]


TONAL_MAJOR = [0,1,1,0,0,1,2]
TONAL_MINOR = [1,2,0,1,1,0,0]
TONAL_MAJOR_7TH = [0,1,1,0,4,1,3]
TONAL_MINOR_7TH = [1,3,0,1,1,0,4]

TONALS = {
    0: TONAL_MAJOR,
    1: TONAL_MINOR,
    2: TONAL_MAJOR_7TH,
    3: TONAL_MINOR_7TH
}
################## CHORD INTERVALS ##################
MAJOR_QUAD = [4, 3, 5]
MINOR_QUAD = [3, 4, 5] 
DOMINANT_QUAD = [4, 3, 5]
DIM_QUAD = [3, 3, 6]
HALF_DIM_QUAD = [3, 3, 6]

# 7TH
MAJOR_QUAD_7TH = [4, 3, 4]
MINOR_QUAD_7TH = [3, 4, 3] 
DOMINANT_QUAD_7TH = [4, 3, 3]
DIM_QUAD_7TH = [3, 3, 3]
HALF_DIM_QUAD_7TH = [3, 3, 4]

QUADS = {
    0: MAJOR_QUAD,
    1: MINOR_QUAD,
    2: DIM_QUAD,
    3: HALF_DIM_QUAD,
    4: DOMINANT_QUAD
}

################## CHORD QUALIFIERS ##################
CHORD_QUALIFIERS = {
    0: "Triad",
    1: "7th",
    2: "9th",
    3: "11th",
    4: "13th"
}



################## EVENTS ##################
EV_RECORD = 'ev_record'
EV_PLAY = 'ev_play'
EV_SUB_BEAT = 'ev_sub_beat'
EV_FORCE_STOP = 'ev_force_stop'
EV_BEAT = 'ev_beat'
EV_SEND_MIDI_NOTE = 'ev_send_midi_note'
EV_SEND_MIDI_MSG = 'ev_send_midi_msg'