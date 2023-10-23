import pyaudio
import wave

def record_sound(output_file, duration, sample_rate=44100, channels=1, format=pyaudio.paInt16):
    frames = []
    chunk = 1024

    audio = pyaudio.PyAudio()

    stream = audio.open(format=format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)

    print("Recording started.")

    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wave_file = wave.open(output_file, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(audio.get_sample_size(format))
    wave_file.setframerate(sample_rate)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

# Example usage
output_file = 'output.wav'
duration = 3  # Recording duration in seconds
record_sound(output_file, duration)
