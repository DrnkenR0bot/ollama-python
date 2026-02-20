import pyttsx3

# Initialize the engine
engine = pyttsx3.init()

# Adjust properties
engine.setProperty('rate', 150)    # Speed (words per minute)
engine.setProperty('volume', 0.9) # Volume (0.0 to 1.0)

# Queue speech
engine.say("This is a more professional way to use e-speak in Python.")
engine.runAndWait() # This blocks until the speech is finished

