import os
import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import translators as ts

# --- Pipeline setting ---
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)
processor = AutoProcessor.from_pretrained(model_id)
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

# --- Language Dictionary ---
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Spanish": "es",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "German": "de",
    "French": "fr",
    "Tamil": "ta",
    "Telugu": "te",
    "Gujarati": "gu",
    "Punjabi": "pa"
}
language_names = list(language_codes.keys())

# --- Create Main Window ---
win = tk.Tk()
win.title("Real-Time Voice Translator")
win.geometry("850x550")
win.resizable(False, False)
icon = tk.PhotoImage(file="icon.png")
win.iconphoto(False, icon)

# --- Style the ttk widgets ---
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", padding=5, font=("Segoe UI", 10))
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", padding=5, font=("Segoe UI", 10, "bold"))

# --- Title ---
title_label = tk.Label(win, text="🎧 Real-Time Voice Translator", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# --- Language Selection Frame ---
lang_frame = tk.Frame(win)
lang_frame.pack(pady=5)

tk.Label(lang_frame, text="Input Language:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
input_lang = ttk.Combobox(lang_frame, values=language_names, state="readonly", width=22)
input_lang.set("English")
input_lang.grid(row=0, column=1, padx=5, pady=5)

tk.Label(lang_frame, text="Output Language:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
output_lang = ttk.Combobox(lang_frame, values=language_names, state="readonly", width=22)
output_lang.set("Hindi")
output_lang.grid(row=0, column=3, padx=5, pady=5)

# --- Text Display Frame ---
text_frame = tk.Frame(win)
text_frame.pack(pady=10)

# Recognized Text
input_box_frame = tk.LabelFrame(text_frame, text="🗣 Recognized Speech", padx=10, pady=10)
input_box_frame.grid(row=0, column=0, padx=20, pady=10)
input_text = tk.Text(input_box_frame, height=8, width=45, wrap="word")
input_text.pack()

# Translated Text
output_box_frame = tk.LabelFrame(text_frame, text="🌐 Translated Output", padx=10, pady=10)
output_box_frame.grid(row=0, column=1, padx=20, pady=10)
output_text = tk.Text(output_box_frame, height=8, width=45, wrap="word")
output_text.pack()

# --- Control Buttons ---
button_frame = tk.Frame(win)
button_frame.pack(pady=15)

run_button = tk.Button(button_frame, text="▶ Start Translation", width=20, command=lambda: run_translator(), bg="#4CAF50", fg="white")
run_button.grid(row=0, column=0, padx=15)

kill_button = tk.Button(button_frame, text="🛌 Kill Execution", width=20, command=lambda: kill_execution(), bg="#f44336", fg="white")
kill_button.grid(row=0, column=1, padx=15)

clear_button = tk.Button(button_frame, text="🪹 Clear Text", width=20, command=lambda: (input_text.delete("1.0", tk.END), output_text.delete("1.0", tk.END)), bg="#607d8b", fg="white")
clear_button.grid(row=0, column=2, padx=15)

# --- Status Bar ---
status_var = tk.StringVar()
status_var.set("Idle...")
status_bar = tk.Label(win, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor="w", font=("Segoe UI", 9))
status_bar.pack(fill="x", side="bottom")

# --- Core Logic ---
keep_running = False

def update_translation():
    global keep_running
    if keep_running:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            status_var.set("Listening...")
            win.update_idletasks()
            # Replace with live for microphone input; testing only:
            audio = r.listen(source)

            try:
                status_var.set("Transcribing...")
                win.update_idletasks()
                with open("temp.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                speech_text = pipe("temp.wav")
                os.remove("temp.wav")
                input_text.insert(tk.END, speech_text["text"] + "\n")

                status_var.set("Translating...")
                win.update_idletasks()
                selected_output_code = language_codes[output_lang.get()]
                translated_text = ts.translate_text(speech_text["text"], translator='bing', to_language=selected_output_code)

                voice = gTTS(translated_text, lang=selected_output_code)
                voice.save('voice.mp3')
                playsound('voice.mp3')
                os.remove('voice.mp3')

                output_text.insert(tk.END, translated_text + "\n")
                status_var.set("Translation Complete.")

            except sr.UnknownValueError:
                output_text.insert(tk.END, "Could not understand!\n")
                status_var.set("Could not understand speech.")
            except sr.RequestError:
                output_text.insert(tk.END, "Request failed.\n")
                status_var.set("Request failed.")

    win.after(100, update_translation)

def run_translator():
    global keep_running
    if not keep_running:
        keep_running = True
        update_translation()

def kill_execution():
    global keep_running
    keep_running = False

# --- Run App ---
win.mainloop()
