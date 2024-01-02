import mido
from mido import MidiFile, MidiTrack
import copy
import os
import glob

gm_percussion = {
    35: 'Acoustic Bass Drum', 36: 'Bass Drum 1', 37: 'Side Stick', 38: 'Acoustic Snare',
    39: 'Hand Clap', 40: 'Electric Snare', 41: 'Low Floor Tom', 42: 'Closed Hi Hat',
    43: 'High Floor Tom', 44: 'Pedal Hi-Hat', 45: 'Low Tom', 46: 'Open Hi-Hat',
    47: 'Low-Mid Tom', 48: 'Hi-Mid Tom', 49: 'Crash Cymbal 1', 50: 'High Tom',
    51: 'Ride Cymbal 1', 52: 'Chinese Cymbal', 53: 'Ride Bell', 54: 'Tambourine',
    55: 'Splash Cymbal', 56: 'Cowbell', 57: 'Crash Cymbal 2', 58: 'Vibraslap',
    59: 'Ride Cymbal 2', 60: 'Hi Bongo', 61: 'Low Bongo', 62: 'Mute Hi Conga',
    63: 'Open Hi Conga', 64: 'Low Conga', 65: 'High Timbale', 66: 'Low Timbale',
    67: 'High Agogo', 68: 'Low Agogo', 69: 'Cabasa', 70: 'Maracas',
    71: 'Short Whistle', 72: 'Long Whistle', 73: 'Short Guiro', 74: 'Long Guiro',
    75: 'Claves', 76: 'Hi Wood Block', 77: 'Low Wood Block', 78: 'Mute Cuica',
    79: 'Open Cuica', 80: 'Mute Triangle', 81: 'Open Triangle'
}

def transpose(note):
    c3 = 60
    return c3

def process_midi(input_file, output_file):
    mid = MidiFile(input_file)
    new_mid = MidiFile(ticks_per_beat=mid.ticks_per_beat)

    tracks = {}
    track_time = {}

    for track in mid.tracks:
        current_ticks = 0
        for msg in track:
            if not msg.is_meta:
                current_ticks += msg.time

            if msg.type == 'note_on' or msg.type == 'note_off':
                pitch = msg.note
                if pitch not in tracks:
                    track_name = gm_percussion.get(pitch, f'Pitch {pitch}')
                    new_track = MidiTrack()
                    new_track.append(mido.MetaMessage('track_name', name=track_name, time=0))
                    tracks[pitch] = new_track
                    track_time[pitch] = 0
                    new_mid.tracks.append(new_track)
                
                new_msg = copy.copy(msg)
                new_msg.note = transpose(pitch)
                new_msg.time = current_ticks - track_time[pitch]
                track_time[pitch] = current_ticks
                tracks[pitch].append(new_msg)
            else:
                for pitch, t in tracks.items():
                    new_msg = copy.copy(msg)
                    new_msg.time = current_ticks - track_time[pitch]
                    track_time[pitch] = current_ticks
                    t.append(new_msg)

    new_mid.save(output_file)

def process_all_midis():
    output_folder = 'Processed'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in glob.glob('*.mid'):
        output_file = os.path.join(output_folder, f'{file}')
        process_midi(file, output_file)

process_all_midis()