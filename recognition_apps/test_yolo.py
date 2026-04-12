import cv2
from ultralytics import YOLO

# モデルのロード
model = YOLO("/home/hs/rcj26_dataset/runs/detect/wurzel26/weights/best.pt")

# カメラの設定（0は内蔵カメラ、1以降は外付けUSBカメラ）
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # YOLOで推論を実行
    # conf: 信頼度のしきい値（0.25以上なら表示など）
    results = model(frame, conf=0.5)

    # 推論結果を描画したフレームを取得
    annotated_frame = results[0].plot()

    # 画面に表示
    cv2.imshow("YOLO Real-time Detection", annotated_frame)

    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()