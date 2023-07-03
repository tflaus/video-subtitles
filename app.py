import os
import streamlit as st
from whisper_transcriber import WhisperTranscriber

def main():
    st.title("Video Subtitle Generator")

    # Initialize WhisperTranscriber
    whisper_transcriber = WhisperTranscriber()

    # Upload video
    video_file = st.file_uploader("Upload a video", type=["mp4", "mov"])
    if video_file:
        # Display video
        st.video(video_file)

        # Save video
        with open("uploaded_video.mp4", "wb") as f:
            f.write(video_file.read())

        # Get timestamps from video transcription
        if st.button("Generate Subtitles"):
            with st.spinner("Transcribing subtitles..."):
                timestamps = whisper_transcriber.transcribe_video_with_timestamps("uploaded_video.mp4")

            # Remove video
            os.remove("uploaded_video.mp4")

            # Write timestamps to a text file
            with open("timestamps.txt", "w", encoding="utf-8") as f:
                for timestamp in timestamps:
                    start_time, end_time, text = timestamp
                    f.write(f"{start_time} - {end_time}: {text}" + "\n")

            # Provide download link for the text file
            with open("timestamps.txt", "r", encoding="utf-8") as f:
                file_content = f.read()

            st.download_button(
                label="Download Timestamps",
                data=file_content,
                file_name="timestamps.txt",
                mime="text/plain",
                on_click=download_button_clicked,
            )

def download_button_clicked():
    pass  # You can add custom logic here if needed

if __name__ == "__main__":
    main()
