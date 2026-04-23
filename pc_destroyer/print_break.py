import sys
import time


sys.setrecursionlimit(20000)

end_time = time.time() + 10
# 出力内容を事前にメモリ上に巨大なバッファとして用意
payload = ("DATA_STREAM_" * 1000 + "\n")


while time.time() < end_time:
    sys.stdout.write(payload)