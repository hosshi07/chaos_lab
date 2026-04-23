import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# --- 設定値 -----------------------------------------------
STUDENT_ID = '3ER1-03'
STUDENT_NAME = 'Toshiki Ishida'

# ロール、ピッチ、ヨー角を設定 (deg)
roll = -90
pitch = 180
yaw = 180

# 角度をラジアンに変換
roll_angle_rad = np.radians(roll)
pitch_angle_rad = np.radians(pitch)
yaw_angle_rad = np.radians(yaw)

# --- 3Dプロットの初期設定 ---------------------------------
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=30, azim=30)

# 背景とグリッドのデザイン
ax.set_facecolor('white')
ax.xaxis.pane.fill = ax.yaxis.pane.fill = ax.zaxis.pane.fill = False
ax.xaxis._axinfo['grid']['linewidth'] = 0.5
ax.yaxis._axinfo['grid']['linewidth'] = 0.5
ax.zaxis._axinfo['grid']['linewidth'] = 0.5

# 軸範囲とラベル
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 軸のガイド線（点線）
ax.plot([-2, 2], [0, 0], [0, 0], color='k', linestyle='--', linewidth=0.5)
ax.plot([0, 0], [-2, 2], [0, 0], color='k', linestyle='--', linewidth=0.5)
ax.plot([0, 0], [0, 0], [-2, 2], color='k', linestyle='--', linewidth=0.5)

# テキスト情報
info_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes, fontsize=10, verticalalignment='top')

# 初期ベクトルの設定（青:X, 赤:Y, 緑:Z）
vectors = np.eye(3)
quiver_colors = ['b', 'r', 'g']
quivers = [ax.quiver(0, 0, 0, 0, 0, 0, color=quiver_colors[i], linewidth=2) for i in range(3)]

# --- 回転行列の定義 ---------------------------------------
def rotate_x(a): return np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
def rotate_y(a): return np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
def rotate_z(a): return np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])

# --- アニメーション更新関数 -------------------------------
def update(frame):
    # アニメーションの進行に合わせて行列を計算
    if frame <= abs(yaw):
        current_yaw = np.radians(frame * np.sign(yaw))
        R = rotate_z(current_yaw)
        phase = "Yawing (Z)"
    elif frame <= abs(yaw) + abs(pitch):
        current_pitch = np.radians((frame - abs(yaw)) * np.sign(pitch))
        R = rotate_z(yaw_angle_rad) @ rotate_y(current_pitch)
        phase = "Pitching (Y)"
    else:
        current_roll = np.radians((frame - abs(yaw) - abs(pitch)) * np.sign(roll))
        R = rotate_z(yaw_angle_rad) @ rotate_y(pitch_angle_rad) @ rotate_x(current_roll)
        phase = "Rolling (X)"

    # ベクトルの回転計算
    rotated = vectors @ R.T

    # 矢印の更新
    global quivers
    for i in range(3):
        quivers[i].remove()
        quivers[i] = ax.quiver(0, 0, 0, rotated[i, 0], rotated[i, 1], rotated[i, 2], 
                               color=quiver_colors[i], arrow_length_ratio=0.15, linewidth=2)
    
    # テキストの更新
    info_text.set_text(f'{STUDENT_ID} {STUDENT_NAME}\nPhase: {phase}\nRoll: {roll} | Pitch: {pitch} | Yaw: {yaw}')
    
    return quivers

# --- 実行 -------------------------------------------------
# アニメーションの作成（aniという変数に入れないと消去されるので注意）
total_frames = abs(yaw) + abs(pitch) + abs(roll)
ani = FuncAnimation(fig, update, frames=np.arange(0, total_frames + 1, 3), 
                    interval=30, blit=False, repeat=True)

print("ウィンドウを表示します。終了するにはウィンドウを閉じてください。")
plt.show()