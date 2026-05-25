import os
import sys
import re
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from moviepy import VideoFileClip
from pytubefix import YouTube
from PIL import Image, ImageTk

# pyinstaller --onefile --windowed --icon=Logo.ico --copy-metadata=imageio --add-data "Logo.png;." main.py


class YouTubeDownloaderApp(tk.Tk):
    # ── Color Palette (Catppuccin Mocha) ──────────────────────────
    BG      = "#1e1e2e"
    SURFACE = "#313244"
    OVERLAY = "#45475a"
    TEXT    = "#cdd6f4"
    SUBTEXT = "#a6adc8"
    ACCENT  = "#cba6f7"
    RED     = "#f38ba8"
    RED_HOVER = "#eba0ac"
    GREEN   = "#a6e3a1"
    GREEN_HOVER = "#b8e6b8"
    BLUE    = "#89b4fa"
    BLUE_HOVER = "#74c7ec"
    YELLOW  = "#f9e2af"

    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader & Converter")
        self.geometry("940x800")
        self.configure(bg=self.BG)
        self.center_window()
        self.setup_styles()
        self.create_widgets()
        self.ensure_directories()

    # ── Window helpers ──────────────────────────────────────────────

    def center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    # ── ttk Styles ─────────────────────────────────────────────────

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Frames
        style.configure("TFrame", background=self.BG)
        style.configure("Header.TFrame", background=self.SURFACE)
        style.configure("HeaderTitle.TLabel", background=self.SURFACE,
                        foreground=self.TEXT, font=("Segoe UI", 15, "bold"))
        style.configure("HeaderSubtitle.TLabel", background=self.SURFACE,
                        foreground=self.SUBTEXT, font=("Segoe UI", 9))
        style.configure("Card.TFrame", background=self.SURFACE)
        style.configure("CardTitle.TLabel", background=self.SURFACE,
                        foreground=self.ACCENT, font=("Segoe UI", 10, "bold"))
        style.configure("CardLabel.TLabel", background=self.SURFACE,
                        foreground=self.SUBTEXT, font=("Segoe UI", 9))

        # General labels & checkbuttons
        style.configure("TLabel", background=self.BG, foreground=self.TEXT,
                        font=("Segoe UI", 10))
        style.configure("TCheckbutton", background=self.SURFACE,
                        foreground=self.TEXT, font=("Segoe UI", 10))
        style.map("TCheckbutton",
                  background=[("active", self.SURFACE)],
                  foreground=[("active", self.TEXT)])

        # Buttons
        base_btn = dict(font=("Segoe UI", 10, "bold"),
                        borderwidth=0, focusthickness=0, focuscolor="",
                        padding=(14, 6))

        style.configure("TButton", background=self.OVERLAY,
                        foreground=self.TEXT, **base_btn)
        style.map("TButton",
                  background=[("active", "#585b70")])

        style.configure("Download.TButton", background=self.RED,
                        foreground=self.BG, **base_btn)
        style.map("Download.TButton",
                  background=[("active", self.RED_HOVER)],
                  foreground=[("disabled", self.SUBTEXT)])

        style.configure("Load.TButton", background=self.GREEN,
                        foreground=self.BG, **base_btn)
        style.map("Load.TButton",
                  background=[("active", self.GREEN_HOVER)])

        style.configure("Clear.TButton", background=self.OVERLAY,
                        foreground=self.TEXT,
                        font=("Segoe UI", 9), borderwidth=0,
                        focusthickness=0, focuscolor="",
                        padding=(10, 4))
        style.map("Clear.TButton",
                  background=[("active", self.BLUE_HOVER)],
                  foreground=[("active", self.BG)])

        # Progress bar
        style.configure("Horizontal.TProgressbar",
                        background=self.ACCENT,
                        troughcolor=self.OVERLAY,
                        bordercolor=self.OVERLAY,
                        lightcolor=self.ACCENT,
                        darkcolor=self.ACCENT,
                        thickness=12)

        # Separator
        style.configure("TSeparator", background=self.OVERLAY)

    # ── Directory setup ─────────────────────────────────────────────

    def ensure_directories(self):
        os.makedirs("videos", exist_ok=True)
        os.makedirs(os.path.join("videos", "mp3"), exist_ok=True)

    # ── Widget tree ─────────────────────────────────────────────────

    def create_widgets(self):
        outer = ttk.Frame(self, padding="16")
        outer.pack(fill=tk.BOTH, expand=True)

        # ── Header ──────────────────────────────────────────────────
        header = ttk.Frame(outer, style="Header.TFrame")
        header.pack(fill=tk.X, pady=(0, 16))
        self._build_header(header)

        # ── Input card ──────────────────────────────────────────────
        input_card = ttk.Frame(outer, style="Card.TFrame", padding="16")
        input_card.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        # Top row: Load button + Convert MP3 checkbox
        top_row = ttk.Frame(input_card, style="Card.TFrame")
        top_row.pack(fill=tk.X, pady=(0, 10))

        self.load_btn = ttk.Button(top_row, text="   Load from url.txt",
                                   style="Load.TButton",
                                   command=self.load_from_file)
        self.load_btn.pack(side=tk.LEFT)

        self.convert_var = tk.BooleanVar()
        self.convert_check = ttk.Checkbutton(top_row, text="Convert to MP3",
                                             variable=self.convert_var)
        self.convert_check.pack(side=tk.LEFT, padx=(20, 0))

        # Separator
        ttk.Separator(input_card, orient=tk.HORIZONTAL).pack(
            fill=tk.X, pady=(0, 10))

        # URL text area
        self.url_text = scrolledtext.ScrolledText(
            input_card, height=8,
            font=("Consolas", 10),
            bg=self.BG, fg=self.TEXT,
            insertbackground=self.TEXT,
            borderwidth=0, relief="flat",
            highlightthickness=1,
            highlightbackground=self.OVERLAY,
            highlightcolor=self.ACCENT,
            padx=10, pady=10)
        self.url_text.pack(fill=tk.BOTH, expand=True)

        # Bottom row: queue counter + download button
        bottom_row = ttk.Frame(input_card, style="Card.TFrame")
        bottom_row.pack(fill=tk.X, pady=(10, 0))

        self.queue_label = ttk.Label(bottom_row, style="CardLabel.TLabel")
        self.update_queue_count(0)
        self.queue_label.pack(side=tk.LEFT)

        self.download_btn = ttk.Button(bottom_row, text="   Start Download",
                                       style="Download.TButton",
                                       command=self.start_download_thread)
        self.download_btn.pack(side=tk.RIGHT)

        # ── Log card ────────────────────────────────────────────────
        log_card = ttk.Frame(outer, style="Card.TFrame", padding="16")
        log_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        log_header = ttk.Frame(log_card, style="Card.TFrame")
        log_header.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(log_header, text="Status Log",
                  style="CardTitle.TLabel").pack(side=tk.LEFT)

        self.clear_log_btn = ttk.Button(log_header, text="Clear",
                                        style="Clear.TButton",
                                        command=self.clear_log)
        self.clear_log_btn.pack(side=tk.RIGHT)

        self.log_text = scrolledtext.ScrolledText(
            log_card, height=9,
            state="disabled",
            font=("Consolas", 9),
            bg=self.BG, fg=self.TEXT,
            insertbackground=self.TEXT,
            borderwidth=0, relief="flat",
            highlightthickness=1,
            highlightbackground=self.OVERLAY,
            highlightcolor=self.ACCENT,
            padx=10, pady=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.log_text.tag_configure("info",    foreground=self.TEXT)
        self.log_text.tag_configure("success", foreground=self.GREEN)
        self.log_text.tag_configure("error",   foreground=self.RED)
        self.log_text.tag_configure("warning", foreground=self.YELLOW)
        self.log_text.tag_configure("accent",  foreground=self.ACCENT)

        # ── Progress bar ────────────────────────────────────────────
        progress_frame = ttk.Frame(outer, style="TFrame")
        progress_frame.pack(fill=tk.X, pady=(0, 10))

        self.status_label = ttk.Label(progress_frame, text="",
                                      font=("Segoe UI", 9))
        self.status_label.pack(fill=tk.X, pady=(0, 4))

        self.progress = ttk.Progressbar(progress_frame, mode="determinate")
        # hidden until a download starts

        # ── Footer hint ─────────────────────────────────────────────
        footer = ttk.Frame(outer, style="TFrame")
        footer.pack(fill=tk.X)
        ttk.Label(footer,
                  text="Paste YouTube URLs (one per line) or use "
                       "'Load from url.txt'",
                  font=("Segoe UI", 9, "italic"),
                  foreground=self.SUBTEXT).pack(side=tk.LEFT)

    def _build_header(self, parent):
        try:
            if hasattr(sys, "_MEIPASS"):
                logo_path = os.path.join(sys._MEIPASS, "Logo.png")
            else:
                logo_path = "Logo.png"
            with Image.open(logo_path) as img:
                resized = img.resize(
                    (img.width // 6, img.height // 6),
                    Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(resized)
            logo_label = ttk.Label(parent, image=self.logo_image,
                                   style="Header.TFrame")
            logo_label.pack(side=tk.LEFT, padx=(0, 16))
        except Exception:
            pass

        block = ttk.Frame(parent, style="Header.TFrame")
        block.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(block, text="YouTube Downloader & Converter",
                  style="HeaderTitle.TLabel").pack(anchor=tk.W)
        ttk.Label(block, text="Download videos and convert to MP3",
                  style="HeaderSubtitle.TLabel").pack(anchor=tk.W)

    # ── Logging ─────────────────────────────────────────────────────

    def log(self, message, level="info"):
        self.log_text.config(state="normal")
        tag = level if level in ("info", "success", "error",
                                 "warning", "accent") else "info"
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state="disabled")

    # ── Progress helpers (callable from any thread) ─────────────────

    def set_progress(self, value):
        self.after(0, lambda: self.progress.config(value=value))

    def show_progress(self, show=True):
        if show:
            self.progress.pack(fill=tk.X)
        else:
            self.progress.pack_forget()
        self.progress["value"] = 0

    def set_status(self, text):
        self.after(0, lambda: self.status_label.config(text=text))

    def update_queue_count(self, count):
        self.queue_label.config(text=f"Queue: {count} video{'s' if count != 1 else ''}")

    # ── File / URL utilities ────────────────────────────────────────

    def load_from_file(self):
        if os.path.exists("url.txt"):
            with open("url.txt", "r", encoding="utf-8") as f:
                content = f.read()
            self.url_text.delete("1.0", tk.END)
            self.url_text.insert(tk.END, content)
            self.log("URLs loaded from url.txt", "success")
        else:
            messagebox.showerror("Error",
                                 "url.txt not found. Creating it now.")
            with open("url.txt", "w", encoding="utf-8") as f:
                f.write("")
            self.log("url.txt has been created.", "warning")

    @staticmethod
    def clean_link_youtube(url: str) -> str:
        pattern = (r"(?:https?:\/\/)?(?:www\.)?"
                   r"(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|"
                   r"watch\?v=|watch\?.+&v=))([\w-]{11})")
        match = re.search(pattern, url)
        if match:
            return f"https://www.youtube.com/watch?v={match.group(1)}"
        return url

    # ── MP3 conversion ──────────────────────────────────────────────

    def convert_video_to_mp3(self, video_path: str):
        self.log(f"Converting: {os.path.basename(video_path)} ...", "accent")
        try:
            clip = VideoFileClip(video_path)
            name, _ = os.path.splitext(os.path.basename(video_path))
            mp3_dir = os.path.join("videos", "mp3")
            mp3_path = os.path.join(mp3_dir, f"{name}.mp3")
            clip.audio.write_audiofile(mp3_path, logger=None)
            clip.close()
            self.log(f"MP3 saved: {mp3_path}", "success")
        except Exception as e:
            self.log(f"Conversion error: {e}", "error")

    # ── Download logic ──────────────────────────────────────────────

    def start_download_thread(self):
        raw = self.url_text.get("1.0", tk.END).strip()
        urls = [u.strip() for u in raw.split("\n") if u.strip()]

        if not urls:
            messagebox.showwarning("Warning", "No URLs provided.")
            return

        self.update_queue_count(len(urls))
        self.download_btn.config(state="disabled")
        self.load_btn.config(state="disabled")
        self.show_progress(True)
        self.set_progress(0)
        self.set_status(f"Starting download of {len(urls)} video(s)...")

        t = threading.Thread(target=self.process_videos, args=(urls,),
                             daemon=True)
        t.start()

    def process_videos(self, urls):
        total = len(urls)
        self.log(f"{'─' * 40}", "accent")
        self.log(f"Processing {total} video(s)", "accent")

        for idx, url in enumerate(urls, 1):
            clean = self.clean_link_youtube(url)
            self.log(f"[{idx}/{total}] {clean}")

            try:
                yt = YouTube(clean)
                stream = (yt.streams
                          .filter(progressive=True, file_extension="mp4")
                          .order_by("resolution").desc().first())
                if stream:
                    self.log(f"Downloading: {stream.default_filename}",
                             "accent")
                    file_path = stream.download(output_path="videos")
                    self.log("Download complete.", "success")

                    if self.convert_var.get():
                        self.convert_video_to_mp3(file_path)
                else:
                    self.log("No suitable stream found.", "error")
            except Exception as e:
                self.log(f"Error: {e}", "error")

            pct = int(idx / total * 100)
            self.set_progress(pct)
            self.set_status(f"Progress: {idx} / {total}  ({pct}%)")

        self.log(f"{'─' * 40}", "accent")
        self.log("All tasks finished.", "success")
        self.set_status("All tasks completed.")
        self.set_progress(100)
        self.after(0, lambda: self.download_btn.config(state="normal"))
        self.after(0, lambda: self.load_btn.config(state="normal"))


if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
