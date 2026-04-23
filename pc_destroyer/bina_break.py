import sys
import time


sys.setrecursionlimit(20000)
# 出力するバイト列を定義 (b"..." でバイナリ指定)
payload = (b"STORM" * 2000 + b"\n")
# 標準出力をバイナリモードで取得
out = sys.stdout.buffer

end_time = time.time() + 10
while time.time() < end_time:
    out.write(payload)