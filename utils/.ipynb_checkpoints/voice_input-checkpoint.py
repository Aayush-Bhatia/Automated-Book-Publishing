import os
import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr


VOICE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "voice_transcripts"))
os.makedirs(VOICE_DIR, exist_ok=True)

fs = 44100  

def record_voice(duration=30):
    """
    Record user's voice using the microphone for the given duration (in seconds).
    Returns the path to the saved WAV file and the timestamp string.
    """
    print(f"🎙️ Recording for {duration} seconds...")

    try:
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        wav_path = os.path.join(VOICE_DIR, f"voice_{timestamp}.wav")
        write(wav_path, fs, audio)
        print(f"💾 Audio saved: {wav_path}")

        return wav_path, timestamp
    
    except Exception as e:
        print(f"-- Error during recording: {e}")
        return None, None


def transcribe_and_append(wav_path, timestamp):
    """
    Transcribes the WAV file using Google Speech Recognition and saves the output.
    Appends to transcript_latest.txt and also saves as a new timestamped file.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(wav_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)

        
        transcript_path = os.path.join(VOICE_DIR, f"transcript_{timestamp}.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(text)

        #latest transcript file
        latest_path = os.path.join(VOICE_DIR, "transcript_latest.txt")
        with open(latest_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n--- {timestamp} ---\n{text}\n")

        print(f"-- Transcript saved at: {transcript_path}")
        print(f"-- Also appended to: {latest_path}")
        print(f"-- Preview:\n{text[:300]}...")

        return text

    except sr.UnknownValueError:
        print("-- Could not understand the audio.")
    except sr.RequestError as e:
        print(f"-- Google Speech API error: {e}")
    except Exception as e:
        print(f"-- Transcription error: {e}")

    return ""
