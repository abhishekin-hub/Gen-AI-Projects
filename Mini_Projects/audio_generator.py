"""
In this solution, The audio file is created from the user text input provided in the frontend.
A simple streamlit UI, Just write the input text and audio file will be ready for download.
"""

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ---- SYSTEM VOICE STYLE INSTRUCTION ----
system_instruction = (
    "Speak in a strong and deep male voice of a Hindi and English speaking Indian man."
    "The narration demands energy, excitement, and a slight dramatic flair."
    "Make it sound as natural as possible. Speak a little faster, like people generally do."
)

#system_instruction = (
    #"Voice Tone: Deep baritone with warm, rich chest resonance. Smooth, clean timbre without nasal or harsh overtones."
    #"Delivery Style: Calm, authoritative, steady. Subtle expression; avoid dramatic or exaggerated emotion."
    #"Pacing: Medium–slow, deliberate rhythm. Insert brief pauses for emphasis and clarity."
    #"Articulation: Crisp, clear diction. Neutral Indian-English broadcast accent; globally intelligible."
    #"Modulation: Controlled pitch movement; gentle rises and falls. Slight emphasis on keywords; no sudden pitch jumps."
    #"Dynamics & Breath: Consistent loudness with even breath support. Minimal breathiness; polished, studio-like presence."
    #"Persona: Professional narrator with composure and clarity. Avoid casual, overly conversational, or comedic tone. Do not imitate any real individual; maintain a general deep-narrator vibe."
#)

# Streamlit UI
st.title("🎙️ Text-to-Speech")
st.write("Paste any text in English or Hindi. The system will convert it into an audio file.")

text = st.text_area(
    "Enter your Text:",
    height=200,
    placeholder="English or हिंदी"
)

if st.button("🔊 Convert to Audio"):
    if text.strip() == "":
        st.error("Please enter some text.")
    else:
        with st.spinner("Generating audio..."):

            # Call TTS with system instruction + user text
            response = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",
                input=text,  # Use Hindi/English text
                response_format="mp3",
                speed = 1.25,
                instructions=system_instruction
            )

            # Save audio to memory
            audio_bytes = response.read()

            # Provide a download link
            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                label="⬇️ Download Audio",
                data=audio_bytes,
                file_name="Male_voice_bold.mp3",
                mime="audio/mp3"
            )

            st.success("Audio generated successfully!")