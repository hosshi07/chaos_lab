#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox          
import datetime

class CountdownTimer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("カウントダウンタイマー")

        # ---------- UI ----------
        # 入力欄（秒数）
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="カウントダウン秒数:").grid(row=0, column=0, padx=5)
        self.seconds_entry = ttk.Entry(input_frame, width=10)
        self.seconds_entry.grid(row=0, column=1, padx=5)
        self.seconds_entry.insert(0, "60")   # デフォルト 60 秒

        # 時間表示
        self.time_var = tk.StringVar(value="00:00:00")
        self.time_label = ttk.Label(self, textvariable=self.time_var,
                                    font=("Helvetica", 36))
        self.time_label.pack(pady=20)

        # ボタン
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="▶︎ 開始", command=self.start)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.pause_btn = ttk.Button(btn_frame, text="⏸️ 一時停止",
                                    command=self.pause, state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = ttk.Button(btn_frame, text="🔄 リセット",
                                    command=self.reset, state="disabled")
        self.reset_btn.grid(row=0, column=2, padx=5)

        # ---------- タイマー状態 ----------
        self.total_seconds = 0
        self.remaining = 0
        self.running = False
        self._after_id = None

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------- タイマーロジック ----------
    def tick(self):
        if not self.running:
            return

        self.remaining -= 1
        self.update_display()

        if self.remaining <= 0:
            self.stop()                  # 時間切れで停止
            return

        # 1 秒後に再度 tick() を呼び出す
        self._after_id = self.after(1000, self.tick)

    def update_display(self):
        td = datetime.timedelta(seconds=self.remaining)
        h, m, s = td.days * 24 + td.seconds // 3600, \
                  (td.seconds % 3600) // 60, \
                  td.seconds % 60
        self.time_var.set(f"{h:02d}:{m:02d}:{s:02d}")

    # ---------- ボタン ----------
    def start(self):
        if self.running:
            return

        # 入力値取得＆検証
        try:
            self.total_seconds = int(self.seconds_entry.get())
            if self.total_seconds <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("入力エラー", "正の整数を入力してください")
            return

        self.remaining = self.total_seconds
        self.update_display()

        self.running = True
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.reset_btn.config(state="normal")

        self.tick()

    def pause(self):
        if not self.running:
            return
        self.running = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")

    def reset(self):
        self.pause()
        self.remaining = self.total_seconds
        self.update_display()

    def stop(self):
        """時間切れ時に呼ばれる"""
        self.pause()
        messagebox.showinfo("完了", "カウントダウン終了です！")

    # ---------- クリーンアップ ----------
    def on_close(self):
        if self._after_id:
            self.after_cancel(self._after_id)
        self.destroy()

# ---------- アプリ起動 ----------
if __name__ == "__main__":
    app = CountdownTimer()
    app.mainloop()
