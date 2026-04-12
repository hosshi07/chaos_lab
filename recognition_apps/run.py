from ultralytics import YOLO
import argparse



# 事前学習済みモデルをロード（例: yolov8n.pt）
model = YOLO('YOLO26m.pt')

data_path = 'data.yaml'

try:
    runs = int(input("学習データ量："))
    name = input("名前：")
except:
    runs = 300
    name = 'learn_yolov8m'
    
if name == '':
    name = 'learn_yolov8m'
    
# ファインチューニング開始
model.train(
    data=data_path,
    epochs=runs,        # 多めに設定してEarly Stoppingに任せる
    patience=50,       # 50エポック改善がなければ終了
    imgsz=640,
    batch=-1,          # 重要：RTX 5080のメモリに合わせて自動で最大値を計算
    name=name,
    resume=False,
    amp=True,          # RTX 5080(Ada Lovelace/Blackwell世代)なら基本Trueで高速化
    workers=8          # Core Ultra 7 265Kなら8〜12程度が効率的
)
