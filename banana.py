import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- シミュレーション・制御ロジック（基本はそのまま） ---
def run_simulation(kp, kd):
    target_position = 10
    mass = 1
    mu = 0.25
    g = 9.81
    t_span = (0, 10)
    t_eval = np.linspace(0, 10, 500)

    def control_law(x, dx):
        error = target_position - x
        return kp * error + kd * (-dx)

    def v_system(t, y):
        x, dx = y[0], y[1]
        force = control_law(x, dx)
        ddx = (force - mu * mass * g * np.tanh(100 * dx)) / mass
        return [dx, ddx]

    sol = solve_ivp(v_system, t_span, [0.0, 0.0], t_eval=t_eval)
    return sol.t, sol.y[0]

# --- GUIの更新処理 ---
def update(val):
    # スライダーから値を取得
    kp = float(kp_slider.get())
    kd = float(kd_slider.get())
    
    # 再計算
    t, pos = run_simulation(kp, kd)
    
    # グラフの更新
    line.set_data(t, pos)
    ax.set_title(f"PD Control: Kp={kp}, Kd={kd}")
    canvas.draw()

# --- TkinterによるGUI構築 ---
root = tk.Tk()
root.title("PID Controller Tuner")

# Matplotlibの図を作成
fig, ax = plt.subplots(figsize=(6, 4))
t, pos = run_simulation(2.0, 0.5)
line, = ax.plot(t, pos)
ax.axhline(10, color='r', linestyle='--')
ax.set_ylim(-2, 15)
ax.set_xlabel("Time [s]")
ax.set_ylabel("Position [m]")

# TkinterにMatplotlibを埋め込む
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# スライダーの配置
kp_slider = tk.Scale(root, from_=0, to=20, resolution=0.1, orient=tk.HORIZONTAL, 
                     label="Kp (Proportional)", command=update)
kp_slider.set(2.0)
kp_slider.pack(fill=tk.X, padx=20)

kd_slider = tk.Scale(root, from_=0, to=10, resolution=0.1, orient=tk.HORIZONTAL, 
                     label="Kd (Derivative)", command=update)
kd_slider.set(0.5)
kd_slider.pack(fill=tk.X, padx=20)

root.mainloop()