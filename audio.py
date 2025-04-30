import pyttsx3
import wave
import pyaudio
import time

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Slow down the speech rate if needed

# Save the audio to file
engine.save_to_file("good morning guys have a nice day ", "good_morning.wav")
engine.runAndWait()

print("WAV file 'good_morning.wav' created successfully.")
