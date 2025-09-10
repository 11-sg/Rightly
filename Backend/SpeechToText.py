import speech_recognition as sr

def recognize_speech(language="en-IN", timeout=10, phrase_time_limit=25):
    """
    Listens for speech, recognizes it, and formats it as a question or statement.
    """
    r = sr.Recognizer()
    
    # Key Change 1: Increase the pause threshold.
    # The default is 0.8 seconds. We're increasing it to 2 seconds to allow
    # for natural pauses in speech without cutting off early.
    r.pause_threshold = 1.5
    
    with sr.Microphone() as source:
        print("Please speak now...")
        # Adjust for ambient noise to improve accuracy
        r.adjust_for_ambient_noise(source, duration=1)
        
        try:
            # Listen for audio from the microphone
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
            return ""

    try:
        # Recognize the speech using Google's Web Speech API
        text = r.recognize_google(audio, language=language)
        new_query = text.lower().strip()

        if not new_query:
            print("Empty speech detected.")
            return ""

        # Key Change 2: More robust way to check for questions
        question_words = (
            "how", "what", "who", "where", "when", "why", "which",
            "whose", "whom", "can you", "what's", "where's", "how's", "is there"
        )

        # Format the output with correct punctuation
        if new_query.startswith(question_words):
            # Remove existing punctuation and add a question mark
            new_query = new_query.rstrip(".?!") + "?"
        else:
            # Remove existing punctuation and add a period
            new_query = new_query.rstrip(".?!") + "."
            
        # Capitalize the first letter and return the result
        return new_query.capitalize()

    except sr.UnknownValueError:
        # This error means the API could not understand the audio
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        # This error is for network issues or API problems
        return f"Could not request results; {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__ == "__main__":
    while True:
        recognized_text = recognize_speech()
        
        # Check if the result is not an error message or empty
        if recognized_text and not recognized_text.lower().startswith(("sorry", "could not", "no speech")):
            print(f"Recognized: {recognized_text}")
            
            # Check for exit commands
            if any(word in recognized_text.lower() for word in ["stop", "exit", "quit", "bye"]):
                print("Exiting program.")
                break
        elif recognized_text:
            # Print the error message from the function
            print(recognized_text)
        else:
            # Handle cases where nothing was returned
            print("No valid speech recognized, please try again.")