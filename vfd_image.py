import spidev
import time
import random
from PIL import Image, ImageEnhance
import numpy as np


GP1294AI_CMD_RESET = 0xAA
GP1294AI_CMD_FRAME_SYNC = 0x08
GP1294AI_CMD_BRIGHTNESS = 0xA0
GP1294AI_CMD_DISPLAY_MODE = 0x80
GP1294AI_CMD_WRITE_GRAM = 0xF0
GP1294AI_CMD_DISPLAY_OFFSET = 0xC0
GP1294AI_CMD_VFD_MODE = 0xCC
GP1294AI_CMD_OSC_SETTING = 0x78
GP1294AI_CMD_EXIT_STANDBY = 0x6D
GP1294AI_CMD_ENTER_STANDBY = 0x61

GP1294AI_MAX_FREQ = 4167000
GP1294AI_DEFAULT_BRIGHTNESS = 300

cmd_reset = [GP1294AI_CMD_RESET]
cmd_init = [GP1294AI_CMD_VFD_MODE, 0x01, 0x01F, 0x00, 0xFF, 0x2F, 0x00, 0x20]
cmd_brightness = [GP1294AI_CMD_BRIGHTNESS, GP1294AI_DEFAULT_BRIGHTNESS & 0xFF, (GP1294AI_DEFAULT_BRIGHTNESS >> 8) & 0xFF]
cmd_offset = [GP1294AI_CMD_DISPLAY_OFFSET, 0x00, 0x00]
cmd_mode = [GP1294AI_CMD_DISPLAY_MODE, 0x00]
cmd_init_osc = [GP1294AI_CMD_OSC_SETTING, 0x08]

# We only have SPI bus 0 available to us on the Pi
bus = 0

#Device is the chip select pin. Set to 0 or 1, depending on the connections
device = 1

# Enable SPI
spi = spidev.SpiDev()

# Open a connection to a specific bus and device (chip select pin)
spi.open(bus, device)

# Set SPI speed and mode
spi.max_speed_hz = 1000000
spi.mode = 3
#spi.lsbfirst

# Sets up LSB FIRST
def reverse(array):
    for index, value in enumerate(array):
        #print(array[index])
        array[index] = int('{:08b}'.format(value)[::-1], 2) 
    return array

def spi_transfer(array):
    spi.xfer2(reverse(array))

def clear():
    empty_frame = [0x00] * (256*8)
    payload = [0xF0, 0, 0, 48] + empty_frame
    print(len(payload))
    spi_transfer(payload)

def fill():
    empty_frame = [0xA0] * (256*8)
    payload = [0xF0, 0, 0, 48] + empty_frame
    print(len(payload))
    spi_transfer(payload)

def draw(image_array):

    i = 0
    x_bit = 0
    binary = [0x00] * 1536
    # Translates images into byte array
    for b in bytes(image_array.tobytes()):
        x_bit = i % 32
        # print(x_bit)
        while ((i % 32) >= 30 ) and (i <= 1534):
            binary[i] = (int('{:08b}'.format(0x00)[::-1], 2)  )
            i+=1
        binary[i] = (int('{:08b}'.format(b)[::-1], 2)  )
        i+=1
        if i >= 1536:
            break

    frame = [0x00] * (1536)
    pixel = 0
    #Transposes image into format VFD will display
    for b in range(len(frame)):
        for i in range(0,8):
            bitmapPixNum = ((pixel % 48) * 256) + int(pixel / 48)
            bitmapByteNum = int(bitmapPixNum / 8)
            bitmapBitNum = bitmapPixNum % 8
            if (binary[bitmapByteNum] & (1 << bitmapBitNum) != 0) :
                frame[b] += 1<<i
            pixel += 1

    # 47 actually means 48, counting 0 as 1 :-/
    payload = [0xF0, 0, 0, 0x2F] + frame
    print(len(payload))
    spi_transfer(payload)

def randomGen(startPos):
    random.seed(a=None, version=2)
    frame =[0] * (256*9)
    randVal = random.randint(0,255)
    for i in range(len(frame)):
        #print(i)
        #randVal = random.randint(0,255)
        if i % 100 <= 25:
            frame[i] =  randVal
        else:
            randVal = random.randint(0,255)
            frame[i] = randVal

    payload = [0xF0, randVal, 0, 48] + frame
    print(len(payload))
    spi_transfer(payload)



def init():
    spi_transfer(cmd_reset)
    #spi_transfer([0x6D])
    time.sleep(0.1)
    spi_transfer(cmd_init)
    spi_transfer(cmd_brightness)
    time.sleep(0.02)
    spi_transfer(cmd_offset)
    spi_transfer(cmd_mode)
    spi_transfer(cmd_init_osc)

def init_test():
    #spi_transfer([0x6D])
    #spi_transfer([0xAA])

    spi_transfer([0xCC,0x01,0x1F,0x00,0xFF,0x2F,0x00,0x20])

    spi_transfer([0xA0,0x28,0x04])

    clear()

    time.sleep(0.02)
    
    spi_transfer([0xF0,0x00,0x00])
    
    spi_transfer([0x80,0x00])
    
    spi_transfer([0x78,0x08])

#init()

# spi_transfer([0x6D])
#fill()

    #image.s
    #image.s
    #image.s

image_1 = Image.open('rain.gif')
image_2 = Image.open('cats.png').convert('1')

while 1:
    for i in range(image_1.n_frames):
        image_1.seek(i)
        draw(image_1.convert('1'))
        init()
 

#spi_transfer([GP1294AI_CMD_WRITE_GRAM,0x00,0x00,0x7f])
#spi_transfer([0x6D])


#spi_transfer([0x01,0x02,0x03])
#spi_transfer([0x47])
#spi_transfer([0x48])
