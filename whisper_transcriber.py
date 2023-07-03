import os
import openai
from dotenv import load_dotenv
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip


class WhisperTranscriber:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Retrieve the API key from the environment variables
        api_key = os.getenv("OPENAI_API_KEY")

        # Check if the API key is set
        if api_key is None:
            raise ValueError("API key not found in the environment variables.")

        # Set the OpenAI API key
        openai.api_key = api_key

    def transcribe_video_with_timestamps(self, video_path):
        # Convert video to audio
        audio_path = self._convert_video_to_audio(video_path)

        # Perform audio transcription
        timestamps = self._transcribe_audio_with_timestamps(audio_path)

        # Delete temporary audio file
        os.remove(audio_path)

        return timestamps

    def _convert_video_to_audio(self, video_path):
        # Convert video to audio and create audio_path
        audio = AudioSegment.from_file(video_path)
        audio_path = video_path.split('.')[0] + '.mp3'

        # Export the audio file
        audio.export(audio_path, format='mp3')
        return audio_path

    def _transcribe_audio_with_timestamps(self, audio_path):
        # Read audio file
        audio_file = open(audio_path, "rb")

        # Perform audio transcription
        response = openai.Audio.transcribe(
            "whisper-1",
            audio_file,
            response_format="verbose_json",
        )

        # Extract transcriptions and timestamps
        transcriptions = response['segments']
        timestamps = []
        for transcription in transcriptions:
            start_time = transcription['start']
            end_time = transcription['end']
            text = transcription['text']
            timestamps.append((start_time, end_time, text))

        return timestamps
    
    def create_subtitle_clips(self, timestamps, videosize, fontsize=24, font='Arial', color='yellow'):
        subtitle_clips = []

        for timestamp in timestamps:
            start_time, end_time, text = timestamp
            duration = end_time - start_time

            video_width, video_height = videosize

            text_clip = TextClip(
                text,
                fontsize=fontsize,
                font=font,
                color=color,
                bg_color='black',
                size=(video_width * 3 / 4, None),
                method='caption'
            ).set_start(start_time).set_duration(duration)

            subtitle_x_position = 'center'
            subtitle_y_position = video_height * 4 / 5

            text_position = (subtitle_x_position, subtitle_y_position)
            subtitle_clips.append(text_clip.set_position(text_position))

        return subtitle_clips


    def add_subtitles_to_video(self, video_path, timestamps, output_path):
        # Load the video clip
        video = VideoFileClip(video_path)

        # Create subtitle clips
        subtitle_clips = self.create_subtitle_clips(timestamps,video.size)

        # Add subtitles to the video
        final_video = CompositeVideoClip([video] + subtitle_clips)

        # Write output video file
        final_video.write_videofile(output_path)



# # Initialize WhisperTranscriber
# whisper_transcriber = WhisperTranscriber()

# # Define paths
# video_path = "test.mp4"
# output_path = "test_st.mp4"

# # Get timestamps from video transcription
# timestamps = whisper_transcriber.transcribe_video_with_timestamps(video_path)

# for timestamp in timestamps:
#     start_time, end_time, text = timestamp
#     print(f"{start_time} - {end_time}: {text}")

# # # Add subtitles to video and save the modified video
# # whisper_transcriber.add_subtitles_to_video(video_path, timestamps, output_path)


# # # Example usage
# # video_file = "test.mp4"

# # transcriber = WhisperTranscriber()
# # timestamps = transcriber.transcribe_video_with_timestamps(video_file)


