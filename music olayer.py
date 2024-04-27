import os
import pygame
from tkinter import Tk, Button, Label, Listbox, Scrollbar, filedialog, Frame

class MusicPlayer:
    def __init__(self):
        self.root = Tk()
        self.root.title("Music Player")
        self.root.geometry("500x400")
        
        # Initialize pygame
        pygame.init()
        
        # Initialize variables
        self.music_files = []
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        
        # Create GUI elements
        self.folder_label = Label(self.root, text="No folder selected", font=("Belinda", 16))
        self.folder_label.pack(pady=10)
        
        self.song_listbox = Listbox(self.root, width=50, height=15, font=("Belinda", 14))
        self.song_listbox.pack(pady=5)
        
        self.scrollbar = Scrollbar(self.root, orient="vertical")
        self.scrollbar.config(command=self.song_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        self.song_listbox.config(yscrollcommand=self.scrollbar.set)
        
        button_frame = Frame(self.root)
        button_frame.pack(pady=10)
        
        self.previous_button = Button(button_frame, text="Previous", command=self.play_previous, state="disabled", font=("Belinda", 14))
        self.previous_button.pack(side="left", padx=5)
        
        self.play_button = Button(button_frame, text="Play", command=self.toggle_play, font=("Belinda", 14))
        self.play_button.pack(side="left", padx=5)
        
        self.next_button = Button(button_frame, text="Next", command=self.play_next, state="disabled", font=("Belinda", 14))
        self.next_button.pack(side="left", padx=5)
        
        self.select_button = Button(self.root, text="Select Folder", command=self.select_folder, font=("Belinda", 14))
        self.select_button.pack(side="bottom", pady=10)
        
        self.song_listbox.bind("<<ListboxSelect>>", self.on_song_select)
        
        self.root.mainloop()
    
    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.music_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".mp3")]
            if self.music_files:
                self.folder_label.config(text=f"Folder: {folder_path}")
                self.song_listbox.delete(0, "end")
                for file in self.music_files:
                    self.song_listbox.insert("end", os.path.basename(file))
                self.play_button.config(state="normal")
                self.next_button.config(state="normal")
                self.current_index = 0
            else:
                self.folder_label.config(text="No music files found in the selected folder.")
    
    def toggle_play(self):
        if not self.is_playing:
            self.play_music()
        elif not self.is_paused:
            self.pause_music()
        else:
            self.resume_music()
    
    def play_music(self):
        if self.music_files:
            pygame.mixer.music.load(self.music_files[self.current_index])
            pygame.mixer.music.play()
            self.is_playing = True
            self.play_button.config(text="Pause")
            self.next_button.config(state="normal")
            self.previous_button.config(state="normal")
    
    def pause_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_button.config(text="Resume")
    
    def resume_music(self):
        pygame.mixer.music.unpause()
        self.is_paused = False
        self.play_button.config(text="Pause")
    
    def stop_music(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.play_button.config(text="Play")
            self.next_button.config(state="disabled")
            self.previous_button.config(state="disabled")
    
    def play_next(self):
        if self.music_files:
            self.current_index = (self.current_index + 1) % len(self.music_files)
            self.play_music()

    def play_previous(self):
        if self.music_files:
            self.current_index = (self.current_index - 1) % len(self.music_files)
            self.play_music()

    def on_song_select(self, event):
        if self.music_files:
            selected_index = self.song_listbox.curselection()
            if selected_index:
                self.current_index = selected_index[0]
                self.stop_music()
                self.play_music()

if __name__ == "__main__":
    MusicPlayer()
