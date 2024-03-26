import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

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

    def add_option(self, option):
        self.options.append(option)
        print(self.options)
    
    def display_menu(self):
        self.oled.fill(0)
        for i in range(len(self.options)):
            print(self.options[i])
            #self.draw.rectangle((0, i*20, self.oled.width - 1, 20), outline=1, fill=0)
            self.draw.text((0, i * 20), self.options[i], font=self.font, fill=255)
        self.oled.image(self.image)
        self.oled.show()



oled_reset = digitalio.DigitalInOut(board.D4)
WIDTH = 128
HEIGHT = 64
BORDER = 5
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Create a Menu object
menu = Menu(oled)

# Add some options to the menu
menu.add_option("Config")
menu.add_option("NFC Module")
menu.add_option("Bluetooth")

# Display the menu
menu.display_menu()
