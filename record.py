import sounddevice as sd
from scipy.io.wavfile import write

# Settings
duration = 10  # Duration in seconds
filename = "my_recording.wav"
samplerate = 44100  # Standard sample rate (CD quality)

# Set the device ID for your microphone
device_id = 8

print("Recording... Speak now!")

# Record audio using the specified device ID
audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='int16', device=device_id)
sd.wait()  # Wait until recording is finished

# Save as WAV
write(filename, samplerate, audio_data)

print(f"Recording saved as '{filename}'")
