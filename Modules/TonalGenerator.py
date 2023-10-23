from State import State_Singleton
import numpy as np
import Constants

class TonalGenerator:
    def __init__(self):
        self.state = State_Singleton()

    # It always returns the quad chord (4th note is the octave)
    def get_chord(self, chord_index, forcedMajor = False):
        dominant_offset = Constants.TONAL_MAJOR_DOMINANTS[chord_index] if self.state.scale == 0 else Constants.TONAL_MINOR_DOMINANTS[chord_index]
        root = self.state.root_note + dominant_offset
        self.state.curr_chord_num = chord_index
        self.state.chord_scale = Constants.TONALS[self.state.scale][chord_index] if not forcedMajor else 0 
        return self.get_chord_notes(root, self.state.chord_scale)

    def get_chord_notes(self, root, tonality):
        intervals = Constants.QUADS[tonality]
        # generate start notes
        notes = [root, root + intervals[0], root + sum(intervals[:2]), root + sum(intervals)]

        # eventually add variations
        if self.state.chord_variation_type[0] == 2:
             notes = self.get_add9_chord(notes)
        if self.state.chord_variation_type[0] == 3:
             notes = self.get_add11_chord(notes)
        if self.state.chord_variation_type[0] == 4:
             notes = self.get_add13_chord(notes)

        self.state.prev_chord_notes = self.state.curr_chord_notes
        self.state.curr_chord_notes = notes
        return notes

    # 0 = root, 1 = third, 2 = fifth, 3 = seventh
    def get_bass_note(self, target):
        return self.state.curr_chord_notes[target] - 2 * Constants.OCTAVE_OFFSET

    def get_arp_note(self, curr_arp_note):
        return self.state.curr_chord_notes[curr_arp_note]

    def get_additional_major(self, index):
        curr_tonal = np.array(Constants.TONALS[self.state.scale])
        idx_non_major_chords = np.where(curr_tonal != 0)[0] # take non major chords from the current tonal
        idx = idx_non_major_chords[index]
    
        return self.get_chord(idx, True)
    
    def get_add9_chord(self, original_chord):
        root, third, fifth, seventh = original_chord
        ninth = root + 14  # Adding 14 semitones (a major 9th interval)
        return [root, third, fifth, seventh, ninth]
    
    def get_add11_chord(self, original_chord):
        root, third, fifth, seventh = original_chord
        eleventh = root + 17 - Constants.OCTAVE_OFFSET# Adding 17 semitones (a perfect 11th interval)
        return [root, third, fifth, seventh, eleventh]
    
    def get_add13_chord(self, original_chord):
        root, third, fifth, seventh = original_chord
        thirteenth = root + 21  - Constants.OCTAVE_OFFSET# Adding 21 semitones (a major 13th interval)
        return [root, third, fifth, seventh, thirteenth]

    def get_augmented_chord(self, chord):
        root, third, fifth, seventh = chord

        # If already agumented return
        if (fifth - root) == 8:
            return chord

        is_suspended = ((third - root) == 5) or ((third - root) == 7)
        is_diminished = (third == root + 3) and (fifth == root + 6)
        is_altered = (seventh - root) == 10 # altered dominant chord
        is_half_diminished = ((third - root) == 3) and ((fifth - root) == 6) and ((seventh - root) == 10)

        if is_suspended:
            # For suspended chords, raise the third note by a half step
            augmented_third = third + 1
            return [root, augmented_third, fifth, seventh]
        elif is_diminished:
            # For diminished chords, raise the root note by a half step instead of the fifth
            augmented_root = root + 1
            return [augmented_root, third, fifth, seventh]
        elif is_altered:
            # For altered dominant chords, raise the fifth, ninth, and thirteenth notes by a half step
            augmented_fifth = fifth + 1
            augmented_ninth = seventh + 2
            augmented_thirteenth = seventh + 6
            return [root, third, augmented_fifth, augmented_ninth, augmented_thirteenth]
        elif is_half_diminished:
            # For half diminished chords, raise the fifth and seventh notes by a half step
            augmented_fifth = fifth + 1
            augmented_seventh = seventh + 1
            return [root, third, augmented_fifth, augmented_seventh]
        else:
            # For other chords, raise the fifth note by a half step
            augmented_fifth = fifth + 1
            return [root, third, augmented_fifth, seventh]