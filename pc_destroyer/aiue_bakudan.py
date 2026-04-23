import time
import sys

sys.setrecursionlimit(20000)


end_time = time.time() + 10
chunk = "あいうえお" * 100 + "\n"  # まとまった塊を作る

while time.time() < end_time:
    # 1回の呼び出しで大量に出力
    print(chunk * 50, end="")