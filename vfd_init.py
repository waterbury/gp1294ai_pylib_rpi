import spidev
import time
import subprocess
#import RPi.GPIO as GPIO

#print (GPIO.VERSION)


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
GP1294AI_DEFAULT_BRIGHTNESS = 0x012C

cmd_reset = [GP1294AI_CMD_RESET]
cmd_init = [GP1294AI_CMD_VFD_MODE, 0x01, 0x01F, 0x00, 0xFF, 0x2F, 0x00, 0x20]
cmd_brightness = [GP1294AI_CMD_BRIGHTNESS, GP1294AI_DEFAULT_BRIGHTNESS & 0xFF, (GP1294AI_DEFAULT_BRIGHTNESS >> 8) & 0xFF]
cmd_offset = [GP1294AI_CMD_DISPLAY_OFFSET, 0x00, 0x00]
cmd_mode = [GP1294AI_CMD_DISPLAY_MODE, 0x00]
cmd_init_osc = [GP1294AI_CMD_OSC_SETTING, 0x08]

fixed_but_fugly = subprocess.run('raspi-gpio set 25 op pn dh',
    shell=True,
    # Probably don't forget these, too
    check=True, text=True)

fixed_but_fugly = subprocess.run('raspi-gpio set 24 op pn dh',
    shell=True,
    # Probably don't forget these, too
    check=True, text=True)

# We only have SPI bus 0 available to us on the Pi
bus = 0

#Device is the chip select pin. Set to 0 or 1, depending on the connections
device = 1

# Enable SPI
spi = spidev.SpiDev()

# Open a connection to a specific bus and device (chip select pin)
spi.open(bus, device)

# Set SPI speed and mode
spi.max_speed_hz = 50000
spi.mode = 3
#spi.lsbfirst

# Sets up LSB FIRST
def reverse(array):
    for index, value in enumerate(array):
        array[index] = int('{:08b}'.format(value)[::-1], 2)
        #print(array[index])
    return array

def spi_transfer(array):
    spi.xfer2(reverse(array))

def clear():
    empty_frame = [0x00] * (256*8)
    payload = [0xF0, 0, 0, 48] + empty_frame
    print(len(payload))
    spi_transfer(payload)

def fill():
    empty_frame = [0xF0] * (896)
    payload = [0xF0, 0, 0, 28] + empty_frame
    print(len(payload))
    spi_transfer(payload)

def init():
    spi_transfer(cmd_reset)
    #spi_transfer([0x6D])
    time.sleep(0.1)
    spi_transfer(cmd_init)
    spi_transfer(cmd_brightness)
    clear()
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

init()

# spi_transfer([0x6D])
#fill()

#clear()

#spi_transfer([GP1294AI_CMD_WRITE_GRAM,0x00,0x00,0x7f])
#spi_transfer([0x6D])


#spi_transfer([0x01,0x02,0x03])
#spi_transfer([0x47])
#spi_transfer([0x48])
