import os
import re
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, PhotoImage
from moviepy import VideoFileClip
from pytube import YouTube
from PIL import Image, ImageTk

#command for conversion to executable with pyinstaller:
#pyinstaller --onefile --noconsole --icon=Logo.ico main.py

class YouTubeDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader & Converter")
        self.geometry("700x600")
        
        # Apply a theme
        style = ttk.Style(self)
        style.theme_use('clam')
        
        self.create_widgets()
        self.ensure_directories()

    def ensure_directories(self):
        if not os.path.exists("videos"):
            os.makedirs("videos")
        if not os.path.exists(os.path.join("videos", "mp3")):
            os.makedirs(os.path.join("videos", "mp3"))

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        try:
            # Usa o Pillow para abrir e redimensionar com alta qualidade (LANCZOS)
            with Image.open("Logo.png") as img:
                # Calcula o novo tamanho dividindo por 6, assim como no original
                resized_img = img.resize((img.width // 6, img.height // 6), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(resized_img)
            title_label = ttk.Label(main_frame, image=self.logo_image)
        except Exception:
            title_label = ttk.Label(main_frame, text="YouTube_DwL", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 10))

        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text="Video URLs (one per line)", padding="5")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.url_text = scrolledtext.ScrolledText(input_frame, height=10, font=("Consolas", 10))
        self.url_text.pack(fill=tk.BOTH, expand=True)

        # Controls Section
        controls_frame = ttk.Frame(main_frame, padding="5")
        controls_frame.pack(fill=tk.X, pady=5)

        self.load_btn = ttk.Button(controls_frame, text="Load from url.txt", command=self.load_from_file)
        self.load_btn.pack(side=tk.LEFT, padx=5)

        self.convert_var = tk.BooleanVar()
        self.convert_check = ttk.Checkbutton(controls_frame, text="Convert to MP3", variable=self.convert_var)
        self.convert_check.pack(side=tk.LEFT, padx=5)

        self.download_btn = ttk.Button(controls_frame, text="Start Download", command=self.start_download_thread)
        self.download_btn.pack(side=tk.RIGHT, padx=5)

        # Log Section
        log_frame = ttk.LabelFrame(main_frame, text="Status Log", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, state='disabled', font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def load_from_file(self):
        if os.path.exists("url.txt"):
            with open("url.txt", "r") as file:
                content = file.read()
                self.url_text.delete("1.0", tk.END)
                self.url_text.insert(tk.END, content)
            self.log("URLs loaded from url.txt")
        else:
            messagebox.showerror("Error", "url.txt not found, creating it now.")
            with open("url.txt", "w") as file:
                file.write("")
            self.log("url.txt created.")

    def clean_link_youtube(self, url: str) -> str:
        standart = r'(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([\w-]{11})'
        match = re.search(standart, url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/watch?v={video_id}"
        return url

    def convert_video_to_mp3(self, video_path: str):
        self.log(f"Converting to MP3: {os.path.basename(video_path)}...")
        try:
            clip = VideoFileClip(video_path)
            
            filename = os.path.basename(video_path)
            name, _ = os.path.splitext(filename)
            mp3_dir = os.path.join("videos", "mp3")
            mp3_path = os.path.join(mp3_dir, f"{name}.mp3")

            clip.audio.write_audiofile(mp3_path, logger=None)
            clip.close()
            self.log(f"Saved MP3: {mp3_path}")
        except Exception as e:
            self.log(f"Conversion error: {e}")

    def start_download_thread(self):
        urls = self.url_text.get("1.0", tk.END).strip().split('\n')
        urls = [u.strip() for u in urls if u.strip()]
        
        if not urls:
            messagebox.showwarning("Warning", "No URLs provided.")
            return

        self.download_btn.config(state='disabled')
        threading.Thread(target=self.process_videos, args=(urls,), daemon=True).start()

    def process_videos(self, urls):
        self.log("Starting download process...")
        for url in urls:
            clean_url = self.clean_link_youtube(url)
            self.log(f"Processing: {clean_url}")
            try:
                yt = YouTube(clean_url)
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                if stream:
                    self.log(f"Downloading: {stream.default_filename}...")
                    file_path = stream.download(output_path="videos")
                    self.log("Download complete.")
                    if self.convert_var.get():
                        self.convert_video_to_mp3(file_path)
                else:
                    self.log(f"No suitable stream found for {clean_url}")
            except Exception as e:
                self.log(f"Error: {e}")
        
        self.log("All tasks finished.")
        self.download_btn.config(state='normal')

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()