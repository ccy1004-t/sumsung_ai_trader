import time
import subprocess
import sys

while True:
    print("\n==============================")
    print("Auto Signal Loop")
    print("==============================")

    subprocess.run([sys.executable, "reports/16_make_5min_bars.py"])
    subprocess.run([sys.executable, "reports/17_live_features.py"])
    subprocess.run([sys.executable, "reports/20_ai_signal.py"])
    
    print("\n等60秒后再次刷新信号...")
    time.sleep(60)