import numpy as np
import sounddevice as sd
from openwakeword.model import Model
from faster_whisper import WhisperModel
from silero_vad import load_silero_vad, get_speech_timestamps
import time # 追加


# --- 設定 ---
# 最初に一度だけダウンロードが必要ですが、以降は物理的にLANを抜いても動きます
MODEL_SIZE = "large-v3-turbo"
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280 # openWakeWordの推奨バッファサイズ

print("モデルを読み込み中 (完全ローカル動作)...")
stt_model = WhisperModel(MODEL_SIZE, device="cuda", compute_type="float16")
vad_model = load_silero_vad()
# 'hey_jarvis' をウェイクワードに設定
oww_model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")

def listen_and_transcribe():
    print("\n[音声認識中...] 話し終えると自動で確定します。")
    audio_buffer = []
    silent_chunks = 0
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32') as stream:
        # 少し長めに待ってから録音を開始する、または録音直後のデータを捨てる等の処理
        while True:
            chunk, _ = stream.read(8000)
            audio_buffer.extend(chunk.flatten())
            
            speech_timestamps = get_speech_timestamps(chunk.flatten(), vad_model, sampling_rate=SAMPLE_RATE)
            
            if len(speech_timestamps) == 0:
                silent_chunks += 1
            else:
                silent_chunks = 0
            
            if silent_chunks > 2:
                break

    segments, _ = stt_model.transcribe(np.array(audio_buffer), beam_size=1, language="ja")
    for segment in segments:
        print(f"認識結果: {segment.text}")

# --- メインループ ---
print("\n[待機中] 'Hey Jarvis' と呼んでください...")
# 入力ストリームを外に出して、一貫した管理をします
with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16') as stream:
    while True:
        audio_data, _ = stream.read(CHUNK_SIZE)
        audio_numpy = audio_data.flatten()

        prediction = oww_model.predict(audio_numpy)
        
        if prediction["hey_jarvis"] > 0.5:
            print(f"\n[!] ウェイクワード検知！ 判定：{prediction['hey_jarvis']:.4f}")
            
            # --- 修正ポイント：STT実行 ---
            listen_and_transcribe()
            
            # --- 修正ポイント：クールダウン ---
            print("...クールダウン中（2秒間入力を無視します）...")
            # STT終了直後のマイクバッファに溜まっている古い音を読み飛ばす
            # stream.stop() / stream.start() を挟むのが最も確実です
            stream.stop()
            time.sleep(1.0) # 1〜2秒ほど待つ
            stream.start()
            
            # openWakeWordの内部状態もリセット（念のため）
            oww_model.reset() 
            
            print("\n[待機中] 'Hey Jarvis' ...")