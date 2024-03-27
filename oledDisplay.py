import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time

#test git configuration comment

WIDTH = 128
HEIGHT = 64 

#i2c configuration
i2c = board.I2C() 
oled_reset = digitalio.DigitalInOut(board.D4)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)



class Menu:
    def __init__(self, oled):
        self.oled = oled
        self.options = []
        self.image = Image.new('1', (oled.width, oled.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()  # List to hold menu options
        self.index = 0  # Current index of the displayed options

    def add_option(self, option):
        self.options.append(option)

    def clear(self):
        self.image = Image.new('1', (oled.width, oled.height))
        self.draw = ImageDraw.Draw(self.image)
        self.oled.fill(0)

    def display_menu(self):
        self.clear()
        
        start_index = self.index
        end_index = min(start_index + 3, len(self.options))
        print(start_index, end_index, self.index) #check the index status

        self.draw.rectangle((0, 0, self.oled.width - 1, 20), outline=255, fill=0) # draw rectangle around selected option
        
        for i in range(start_index, end_index):
            y = (i - start_index) * 20 + 5
            self.draw.text((5, y), self.options[i], font=self.font, fill=255)
        
        
        

        self.oled.image(self.image)
        self.oled.show()

# create a Menu object
menu = Menu(oled)

# add some options to the menu
menu.add_option("Config")
menu.add_option("NFC Module")
menu.add_option("Bluetooth")
menu.add_option("Option 4")
menu.add_option("Option 5")
menu.add_option("Option 6")
menu.add_option("Option 7")
menu.add_option("Option 8")

# display the menu
menu.display_menu()

# test scrolling
time.sleep(1)
for index in range(len(menu.options)-1):
    menu.index += 1
    menu.display_menu()
    time.sleep(1)
