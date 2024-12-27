import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
import pysrt

def load_captions(file_path):
    subs = pysrt.open(file_path)
    caption_text = "\n\n".join(
        f"{sub.index}\n{sub.start} --> {sub.end}\n{sub.text}" for sub in subs
    )
    return caption_text

def save_captions(file_path, text):
    lines = text.strip().split("\n\n")
    subs = pysrt.SubRipFile()
    for line in lines:
        parts = line.split("\n")
        if len(parts) >= 3:
            index = int(parts[0])
            time_range = parts[1].split(" --> ")
            text_content = "\n".join(parts[2:])
            start = pysrt.SubRipTime.from_string(time_range[0])
            end = pysrt.SubRipTime.from_string(time_range[1])
            subs.append(pysrt.SubRipItem(index=index, start=start, end=end, text=text_content))
    subs.save(file_path, encoding="utf-8")

class CaptionEditor:
    def __init__(self, root):
        self.root = root
        self.text_editor = ScrolledText(root, wrap=tk.WORD, width=100, height=30)
        self.text_editor.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("SRT Files", "*.srt")])
        if file_path:
            captions = load_captions(file_path)
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert(tk.END, captions)
            messagebox.showinfo("Success", "Captions loaded successfully!")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SRT Files", "*.srt")])
        if file_path:
            edited_text = self.text_editor.get("1.0", tk.END)
            try:
                save_captions(file_path, edited_text)
                messagebox.showinfo("Success", "Captions saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save captions: {e}")