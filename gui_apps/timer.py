import tkinter as tk
from tkinter import ttk
import datetime

class TimerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tkinter タイマー")
        self.geometry("300x150")
        self.resizable(False, False)

        # ---- 1. ウィジェット作成 ----
        self.time_label = ttk.Label(self, text="00:00:00",
                                    font=("Helvetica", 36))
        self.time_label.pack(pady=20)

        btn_frame = ttk.Frame(self)
        btn_frame.pack()

        self.start_btn = ttk.Button(btn_frame, text="▶︎ 開始",
                                    command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.pause_btn = ttk.Button(btn_frame, text="⏸️ 一時停止",
                                    command=self.pause_timer, 
state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = ttk.Button(btn_frame, text="🔄 リセット",
                                    command=self.reset_timer, 
state="disabled")
        self.reset_btn.grid(row=0, column=2, padx=5)

        # ---- 2. タイマー状態 ----
        self.running = False          # タイマー動作中かどうか
        self.elapsed = datetime.timedelta()  # 経過時間
        self._job = None              # after のジョブID

    # ---- 3. タイマー処理 ----
    def tick(self):
        """1秒ごとに呼ばれる関数"""
        if self.running:
            self.elapsed += datetime.timedelta(seconds=1)
            self.update_label()

            # 1 秒後に再度 tick() を呼び出す
            self._job = self.after(1000, self.tick)

    def update_label(self):
        """Label を HH:MM:SS に更新"""
        h, m, s = int(self.elapsed.total_seconds()) // 3600, \
                  (int(self.elapsed.total_seconds()) % 3600) // 60, \
                  int(self.elapsed.total_seconds()) % 60
        self.time_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")

    # ---- 4. ボタンコールバック ----
    def start_timer(self):
        if not self.running:
            self.running = True
            self.tick()                # tick() を呼び出してから 1 秒後
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.reset_btn.config(state="normal")

    def pause_timer(self):
        if self.running:
            self.running = False
            if self._job:
                self.after_cancel(self._job)  # 後で呼び出されるタスクを取り
                self._job = None
            self.start_btn.config(state="normal")
            self.pause_btn.config(state="disabled")

    def reset_timer(self):
        self.pause_timer()
        self.elapsed = datetime.timedelta()
        self.update_label()

    # ---- 5. ウィンドウクローズ時に cleanup ----
    def on_closing(self):
        if self._job:
            self.after_cancel(self._job)
        self.destroy()

if __name__ == "__main__":
    app = TimerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
