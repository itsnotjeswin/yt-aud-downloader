import streamlit as st
from pytubefix import YouTube
from pathlib import Path
import os
import unicodedata

# Function to sanitize the filename
def sanitize_filename(filename):
    filename = unicodedata.normalize("NFKD", filename)  # Normalize Unicode
    return "".join(c if c.isalnum() or c in " ._-" else "_" for c in filename)

# Function to download audio
def audio(thelink):
    try:
        yt = YouTube(thelink)
        st.write(f"**Title:** {yt.title}")
        st.write(f"**Views:** {yt.views}")
        yd = yt.streams.get_audio_only()
        yt_title = sanitize_filename(yt.title)

        # Save to the current working directory
        save_dir = Path(os.getcwd())
        file_path = save_dir / f"{yt_title}.mp3"

        # Download the audio
        yd.download(output_path=save_dir, filename=f"{yt_title}.mp3")
        
        # Print the file path to the console
        print(f"Audio downloaded to: {file_path}")
        st.success(f"Audio downloaded successfully: {file_path}")
        return file_path
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Streamlit app
def main():
    # Set page configuration
    st.set_page_config(
        page_title="YouTube Audio Downloader",
        page_icon="🎵",
        layout="wide",
    )

    # Custom CSS to style the app
    st.markdown(
        """
        <style>
        .title {
            font-size:50px !important;
            color: #ff4b4b;
            text-align: center;
        }
        .subtitle {
            font-size:20px !important;
            color: #4b4bff;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # App title and subtitle
    st.markdown('<p class="title">🎵 YouTube Audio Downloader</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Download and play audio from YouTube videos effortlessly!</p>', unsafe_allow_html=True)
    st.write("---")
    st.markdown("Enter a YouTube video URL to download the audio file.")

    # Input field for URL
    url = st.text_input("YouTube Video URL", "")

    # Button to trigger download
    if st.button("Download Audio"):
        if url:
            st.info("Downloading audio...")
            file_path = audio(url)
            if file_path and file_path.exists():
                # Play the audio using st.audio
                with open(file_path, "rb") as audio_file:
                    st.audio(audio_file, format="audio/mp3")

                # Provide a download button
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="Download MP3",
                        data=file,
                        file_name=file_path.name,
                        mime="audio/mpeg",
                    )
        else:
            st.warning("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
