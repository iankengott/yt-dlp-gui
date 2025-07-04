import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def choose_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_dir.set(directory)

def start_download():
    url = url_entry.get()
    out_dir = output_dir.get()
    mode = format_var.get()
    embed = embed_thumbnail.get()

    if not url or not out_dir:
        messagebox.showerror("Missing Info", "Please provide a URL and select an output folder.")
        return

    # Construct yt-dlp command
    command = ["yt-dlp", url, "-o", os.path.join(out_dir, "%(title)s.%(ext)s")]

    if mode == "audio":
        command += ["-f", "bestaudio", "--extract-audio", "--audio-format", "mp3"]
        if embed:
            command += ["--embed-thumbnail", "--add-metadata"]
    else:
        command += ["-f", "bestvideo+bestaudio", "--merge-output-format", "mp4"]
    
    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", "Download completed!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Download failed.")

# GUI Setup
root = tk.Tk()
root.title("yt-dlp Simple GUI")

tk.Label(root, text="YouTube Link / Playlist:").grid(row=0, column=0, sticky="w")
url_entry = tk.Entry(root, width=60)
url_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Output Folder:").grid(row=1, column=0, sticky="w")
output_dir = tk.StringVar()
tk.Entry(root, textvariable=output_dir, width=45).grid(row=1, column=1, sticky="w", padx=(0,5))
tk.Button(root, text="Browse", command=choose_directory).grid(row=1, column=2)

format_var = tk.StringVar(value="audio")
tk.Label(root, text="Download Type:").grid(row=2, column=0, sticky="w")
tk.Radiobutton(root, text="Audio (MP3)", variable=format_var, value="audio").grid(row=2, column=1, sticky="w")
tk.Radiobutton(root, text="Video (MP4)", variable=format_var, value="video").grid(row=3, column=1, sticky="w")

embed_thumbnail = tk.BooleanVar()
tk.Checkbutton(root, text="Embed Thumbnail (for audio)", variable=embed_thumbnail).grid(row=4, column=1, sticky="w")

tk.Button(root, text="Download", command=start_download, bg="#4CAF50", fg="white", height=2, width=20).grid(row=5, column=1, pady=10)

root.mainloop()
