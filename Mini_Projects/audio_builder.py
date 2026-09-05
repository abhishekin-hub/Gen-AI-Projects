"""
In this solution, The audio file is created from the user text input or text input within this code.
No UI needed, Just run the code in the terminal.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Type the text input for the audio file.
#text_input = "दोस्तों! स्वागत है उस सफ़र में जहाँ आपकी सोच नई ऊँचाइयों को छूने वाली है!"
text_input = input("Type the text input: \n")


# The default system prompt for voiceover
system_instruction= (
    "Speak in a strong and deep male voice of a Hindi and English speaking Indian man."
    "The narration demands energy, excitement, and a slight dramatic flair."
    "Make it sound as natural as possible. Speak a little faster, like people generally do."
)

# Output folder and file name
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
output_file = "voiceover.mp3"
output_path = os.path.join(downloads_folder, output_file)

# Ensure folder exists
os.makedirs(downloads_folder, exist_ok=True)

# Call TTS API
response = client.audio.speech.create(
    model="gpt-4o-mini-tts",  # TTS model
    voice="alloy",  # Best general-purpose Indian-friendly voice
    input=text_input,  # Use Hindi text
    response_format="mp3",
    speed = 1.25,
    instructions = system_instruction
)

# Save MP3 file
with open(output_path, "wb") as f:
    f.write(response.read())

print(f"Audio saved to: {output_path}")
