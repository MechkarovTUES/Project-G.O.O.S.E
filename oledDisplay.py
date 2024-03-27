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
        self.font = ImageFont.load_default()
        self.index = 0  # Current selection index
        self.start_index = 0  # Start index of the visible options

    def add_option(self, option):
        self.options.append(option)

    def clear(self):
        self.image = Image.new('1', (oled.width, oled.height))
        self.draw = ImageDraw.Draw(self.image)
        self.oled.fill(0)

    def display_menu(self):
        self.clear()
        visible_count = 3  # Number of options visible at once
        end_index = min(self.start_index + visible_count, len(self.options))

        for i in range(self.start_index, end_index):
            y = (i - self.start_index) * 20 + 5
            if i == self.index:
                self.draw.rectangle((0, y - 5, self.oled.width - 1, y + 15), outline=255, fill=0)  # Highlight selected option
            self.draw.text((5, y), self.options[i], font=self.font, fill=255)

        self.oled.image(self.image)
        self.oled.show()

    def scroll_down(self):
        if self.index < len(self.options) - 1:
            self.index += 1
            if self.index >= self.start_index + 3:  # If the selection moves beyond the visible options
                self.start_index += 1  # Scroll options down

    def scroll_up(self):
        if self.index > 0:
            self.index -= 1
            if self.index < self.start_index:  # If the selection moves before the visible options
                self.start_index -= 1  # Scroll options up
    def calcSize(self):
        print(self.font.getsize(self.options[2])[0])

# create a Menu object
menu = Menu(oled)

# add some options to the menu
menu.add_option("Config")
menu.add_option("NFC Module")
menu.add_option("Pair with Bluetooth")
menu.add_option("Option 4")
menu.add_option("Option 5")
menu.add_option("Option 6")
menu.add_option("Option 7")
menu.add_option("Option 8")

# display the menu
menu.display_menu()

# test scrolling
time.sleep(1)
for i in range(3):
    menu.scroll_down()
    menu.display_menu()
    time.sleep(1)

# menu.calcSize()

time.sleep(1)
for i in range(5):
    menu.scroll_up()
    menu.display_menu()
    time.sleep(1)
