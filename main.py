# Thumby main.py- quick initialization to display the TinyCircuits logo before menu.py is called

from machine import mem32, freq
#Address of watchdog timer scratch register
WATCHDOG_BASE=0x40058000
SCRATCH0_ADDR=WATCHDOG_BASE+0x0C

if(mem32[SCRATCH0_ADDR]==1):
    mem32[SCRATCH0_ADDR]=0
    gamePath=''
    conf = open("thumby.cfg", "r").read().split(',')
    for k in range(len(conf)):
        if(conf[k] == "lastgame"):
            gamePath = conf[k+1]
    freq(125000000)
    try:
        __import__(gamePath)
    except ImportError:
        print("Thumby error: Couldn't load "+gamePath)



from machine import Pin, Timer, I2C, PWM, SPI, freq, WDT
from time import sleep_ms, ticks_ms, sleep_us, ticks_us
import ssd1306


brightnessSetting=2
try:
    conf = open("thumby.cfg", "r").read().split(',')
    print(conf)
    for k in range(len(conf)):
        if(conf[k] == "brightness"):
            brightnessSetting = int(conf[k+1])
except OSError:
    pass

brightnessVals=[0,28,127]

HWID = 0


i2c = None
spi = None
display=None
if(HWID==0):
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=200000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c, res=Pin(29))
if(HWID>=1):
    spi = SPI(0, sck=Pin(18), mosi=Pin(19))#possible assignment of miso to 4 or 16?
    display = ssd1306.SSD1306_SPI(72, 40, spi, dc=Pin(17), res=Pin(20), cs=Pin(16))

display.init_display()
display.contrast(brightnessVals[brightnessSetting])

f=open('lib/TClogo.bin')
f.readinto(display.buffer)
f.close()
display.show()




import menu

machine.reset()