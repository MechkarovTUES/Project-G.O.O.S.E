import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
# Define the Reset Pin

#test git configuration comment
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 5

# Use for I2C.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# oled.fill(0)
# oled.show()
# image = Image.open('imageLibrary/Mladshi_128x64.ppm').convert('1')
# # Display image
# oled.image(image)
# oled.show()


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
        selected_option_y = (self.index - start_index) * 20
        print(selected_option_y, start_index, end_index, self.index)
        self.draw.rectangle((0, selected_option_y, self.oled.width - 1, selected_option_y + 20), outline=255, fill=0)
        
        for i in range(start_index, end_index):
            y = (i - start_index) * 20 + 5
            self.draw.text((5, y), self.options[i], font=self.font, fill=255)
        
        # Draw rectangle around selected option
        

        self.oled.image(self.image)
        self.oled.show()

    # def scroll_down(self):
    #     if self.index < len(self.options) - 1:
    #         self.index += 1
    #         self.display_menu()

    # def scroll_up(self):
    #     if self.index > 0:
    #         self.index -= 1
    #         self.display_menu()


# Create a Menu object
menu = Menu(oled)

# Add some options to the menu
menu.add_option("Config")
menu.add_option("NFC Module")
menu.add_option("Bluetooth")
menu.add_option("Option 4")
menu.add_option("Option 5")
menu.add_option("Option 6")
menu.add_option("Option 7")
menu.add_option("Option 8")

# Display the menu
menu.display_menu()

# Test scrolling
time.sleep(1)
for index in range(len(menu.options)-1):
    menu.index += 1
    menu.display_menu()
    time.sleep(1)
