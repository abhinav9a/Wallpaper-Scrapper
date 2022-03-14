import ctypes
import os
import time
import random

# Path of wallpapers folder
image_dir = os.path.abspath('.\\images')
# Time after which wallpaper changes
time_limit = 30
SPI_SETDESKTOPWALLPAPER = 20

while True:
    images_path = [os.path.join(image_dir, image) for image in os.listdir(image_dir)]
    # print(images_path)
    random.shuffle(images_path)
    for image in images_path:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKTOPWALLPAPER, 0, image, 3)
        time.sleep(time_limit)
