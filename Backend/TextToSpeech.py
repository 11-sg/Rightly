# import win32com.client

# def say(text):
#     speaker = win32com.client.Dispatch("SAPI.SpVoice")
#     voices = speaker.GetVoices()

#     # Select voice by index or by name matching
#     speaker.Voice = voices.Item(0)  # first voice in the list
#     speaker.Speak(text)

import win32com.client
import pythoncom

def say(text):
    pythoncom.CoInitialize()  # Initialize COM in this thread
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()
    speaker.Voice = voices.Item(1)  # Select first voice
    speaker.Speak(text)
    pythoncom.CoUninitialize()  # Optional, clean up COM initialization


# Example usage: text-to-speech only
if __name__ == "__main__":
    while True:
        text = input("Enter the text: ")
        if text.lower() in ['exit', 'quit', 'stop']:
            break
        say(text)
