# 載入需要的函式庫
import RPi.GPIO as GPIO
import time

# 腳位設定
TACH = 24       # 風扇轉速輸出腳位
PULSE = 2       # Noctua 規格為風扇轉一圈有兩次脈衝，大部分風扇也是兩次，少數四次
WAIT_TIME = 1   # 單位為秒，每次更新時間

# GPIO 設定
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TACH, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pull up to 3.3V

# 要用到的全域變數
t = time.time()
rpm = 0

# 計算 RPM 的函數
def fell(n):
    global t
    global rpm 

    dt = time.time() - t    # 取得時間計算出週期
    if dt < 0.005: return   # 無視過短的脈衝（雜訊）

    freq = 1 / dt   # 取得頻率（週期倒數）
    rpm = (freq / PULSE) * 60   # 計算RPM：將頻率除以風扇轉一圈的脈衝數，在乘以60（每分鐘）
    t = time.time() # 更新時間

# 新增監聽器，偵測到波形降下來的時候呼叫 fell() 計算一次 RPM
GPIO.add_event_detect(TACH, GPIO.FALLING, fell)

# 主程式
try:
    # 無限迴圈不斷偵測
    while True:
	    print("%.f RPM" % rpm)   # 輸出轉速到螢幕上
	    rpm = 0 # 歸零
	    time.sleep(WAIT_TIME)   # 每秒偵測一次

except KeyboardInterrupt: # 同上處理 ctrl+c 例外
    GPIO.cleanup()  # 清除本程式用的 GPIO 狀態
