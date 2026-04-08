import os
import tkinter as tk
from tkinter import filedialog, ttk
import pygame
from mutagen.mp3 import MP3

class UltimateMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Music Library")
        self.root.geometry("600x450")

        pygame.mixer.init()

        # 変数管理
        self.track_list = []
        self.current_index = 0
        self.music_length = 0
        self.current_start_time = 0
        self.is_paused = False
        self.is_dragging = False

        # --- UI設計 ---
        # 上部：フォルダ選択
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)
        tk.Button(top_frame, text="フォルダを選択", command=self.load_folder).pack()

        # 中央：リストボックスとスクロールバー
        list_frame = tk.Frame(root)
        list_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(list_frame, yscrollcommand=self.scrollbar.set, selectmode=tk.SINGLE)
        self.scrollbar.config(command=self.listbox.yview)
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # リスト内のアイテムをダブルクリックで再生
        self.listbox.bind('<Double-1>', lambda x: self.play_from_list())

        # 下部：コントロール
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        self.lbl_track = tk.Label(control_frame, text="曲を選択してください", font=("Arial", 10, "bold"))
        self.lbl_track.pack()

        self.lbl_time = tk.Label(control_frame, text="00:00 / 00:00")
        self.lbl_time.pack()

        self.seek_bar = ttk.Scale(control_frame, from_=0, to=100, orient="horizontal", length=400, command=self.on_slider_move)
        self.seek_bar.pack(pady=5)
        self.seek_bar.bind("<ButtonPress-1>", self.on_slider_press)
        self.seek_bar.bind("<ButtonRelease-1>", self.on_slider_release)

        btn_frame = tk.Frame(control_frame)
        btn_frame.pack()
        tk.Button(btn_frame, text="⏮", command=self.prev_track, width=5).grid(row=0, column=0, padx=5)
        self.btn_play = tk.Button(btn_frame, text="▶ 再生", command=self.toggle_play, width=10)
        self.btn_play.grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="⏭", command=self.next_track, width=5).grid(row=0, column=2, padx=5)

        self.update_ui()

    def load_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            self.track_list = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')]
            self.listbox.delete(0, tk.END) # リストをクリア
            
            for path in self.track_list:
                filename = os.path.basename(path)
                self.listbox.insert(tk.END, filename) # リストボックスにファイル名を追加
            
            if self.track_list:
                self.current_index = 0
                self.listbox.select_set(0) # 最初の曲を選択状態にする

    def play_from_list(self):
        """リストで選択された曲を再生"""
        selection = self.listbox.curselection()
        if selection:
            self.current_index = selection[0]
            self.load_track()

    def load_track(self):
        path = self.track_list[self.current_index]
        pygame.mixer.music.load(path)
        
        audio = MP3(path)
        self.music_length = audio.info.length
        self.seek_bar.config(to=self.music_length)
        
        self.current_start_time = 0
        self.lbl_track.config(text=os.path.basename(path))
        
        # リストボックスの選択状態を更新
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.current_index)
        self.listbox.see(self.current_index) # 選択中の曲までスクロール
        
        self.play_music()

    def toggle_play(self):
        if not self.track_list: return
        # 何も再生されていない状態で再生ボタンが押された場合、選択中の曲をロード
        if not pygame.mixer.music.get_busy() and not self.is_paused:
            self.play_from_list()
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.btn_play.config(text="⏸ 一時停止")
        else:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.btn_play.grid()
            self.btn_play.config(text="▶ 再生")

    def play_music(self):
        pygame.mixer.music.play()
        self.is_paused = False
        self.btn_play.config(text="⏸ 一時停止")

    def next_track(self):
        if self.track_list:
            self.current_index = (self.current_index + 1) % len(self.track_list)
            self.load_track()

    def prev_track(self):
        if self.track_list:
            self.current_index = (self.current_index - 1) % len(self.track_list)
            self.load_track()

    def on_slider_press(self, event):
        self.is_dragging = True

    def on_slider_release(self, event):
        self.current_start_time = self.seek_bar.get()
        pygame.mixer.music.play(start=self.current_start_time)
        self.is_dragging = False

    def on_slider_move(self, val):
        pass

    def update_ui(self):
        if pygame.mixer.music.get_busy() and not self.is_paused and not self.is_dragging:
            actual_pos = self.current_start_time + (pygame.mixer.music.get_pos() / 1000)
            self.seek_bar.set(actual_pos)
            self.lbl_time.config(text=f"{self.format_time(actual_pos)} / {self.format_time(self.music_length)}")

        # 曲が終了したら次へ
        if not pygame.mixer.music.get_busy() and not self.is_paused and self.track_list:
            if self.seek_bar.get() >= self.music_length - 1:
                self.next_track()

        self.root.after(500, self.update_ui)

    def format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateMusicPlayer(root)
    root.mainloop()