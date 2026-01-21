# YouTube_Dwl

A simple Python script to download YouTube videos from a list of URLs and optionally convert them to MP3 format.

## Features

- **Bulk Download**: Downloads multiple YouTube videos listed in a text file.
- **Link Cleaning**: Automatically standardizes different YouTube URL formats to ensure compatibility.
- **MP3 Conversion**: Converts downloaded videos (MP4 format) to MP3 audio files.
- **Simple Interface**: Command-line execution with basic user interaction.

## Prerequisites

Before running the script, make sure you have the following prerequisites installed:

- **Python 3.x**
- **pytube**: 
  ```bash
   pip install pytube  # Library for downloading YouTube videos
   ```
- **moviepy**: 
  ```bash
   pip install moviepy  # Library for converting to MP3
   ```
- **requirements.txt**: For other required libraries, see the `requirements.txt` file.

## How to Use

1. **Create the `url.txt` file**: In the same directory as `main.py`, create a file named `url.txt`.

2. **Add the URLs**: Add one YouTube video link per line in this file. For example:
   ```txt
   https://www.youtube.com/watch?v=[VIDEO_ID]
   https://youtu.be/[VIDEO_ID]
   ```

3. **Run the script**: Open your terminal, navigate to the project directory, and run the following command:
   ```bash
   python main.py
   ```

4. **Download Process**: The script will display a stylized title and start downloading the videos from `url.txt`. The videos will be saved in a new folder called `videos`.

5. **MP3 Conversion**: After the downloads are finished, the script will ask if you want to convert the videos to MP3.
   ```
   Do you want to convert all videos to MP3? (y/n):
   ```
   - Type `y` and press `Enter` to start the conversion.
   - The MP3 files will be saved in a `videos/mp3/` subfolder.
   - Type `n` to cancel the operation and exit the script.

## File Structure

The script will create the `videos` and `mp3` directories, resulting in the following structure:

```
.
├── main.py
├── url.txt
└── videos/
    ├── video1.mp4
    ├── video2.mp4
    └── mp3/
        ├── video1.mp3
        └── video2.mp3
```