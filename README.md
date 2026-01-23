# YouTube_Dwl

A Python application to download YouTube videos from a list of URLs and optionally convert them to MP3 format using a Graphical User Interface (GUI).

## Features

- **Bulk Download**: Downloads multiple YouTube videos listed in the application or loaded from a text file.
- **Link Cleaning**: Automatically standardizes different YouTube URL formats to ensure compatibility.
- **MP3 Conversion**: Converts downloaded videos (MP4 format) to MP3 audio files.
- **Simple Interface**: User-friendly Graphical User Interface (GUI).

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
- **Pillow**:
  ```bash
   pip install Pillow  # Library for image processing
   ```
- **requirements.txt**: For other required libraries, see the `requirements.txt` file.

## How to Use

1. **Run the script**: Open your terminal, navigate to the project directory, and run the following command:
   ```bash
   python main.py
   ```

2. **Add URLs**:
   - **Paste** video URLs directly into the text area (one per line).
   - **OR** Click **"Load from url.txt"** to load URLs from a `url.txt` file in the same directory.

3. **MP3 Conversion**: Check the **"Convert to MP3"** box if you wish to convert the videos to audio.

4. **Start Download**: Click on **"Start Download"** to begin the process.
   - The status log will show the progress.
   - Videos are saved in the `videos` folder.
   - MP3s are saved in `videos/mp3`.

## Using the Executable (Windows)

The standalone executable version simplifies usage by not requiring Python or any dependency installation.

1.  **Run the Application**: Place the `main.exe` file in any folder and double-click it to run.
2.  **Functionality**: The application window will open, and all features work as described above.
    - You can paste URLs directly into the text area.
    - If you click **"Load from url.txt"**, the `url.txt` file will be created in the same folder as the `.exe`. You can then edit this file and load the URLs from it.
3.  **Output Folders**: The downloaded files will be saved in the `videos` and `videos/mp3` subfolders, which will be created inside the same directory where `main.exe` is located.

## File Structure

Whether you run the Python script or the executable, the necessary directories will be created, resulting in a structure like this:

```
.
├── main.py or YouTube_Dwl.exe
├── url.txt
└── videos/
    ├── video1.mp4
    ├── video2.mp4
    └── mp3/
        ├── video1.mp3
        └── video2.mp3
```