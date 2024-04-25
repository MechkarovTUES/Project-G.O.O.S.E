import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
import RPi.GPIO as GPIO


#test git configuration comment

WIDTH = 128
HEIGHT = 64

#i2c configuration
i2c = board.I2C() 
oled_reset = digitalio.DigitalInOut(board.D4)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)



def Scroll(prev_CLK_state, CLK_state, counter, direction, button_pressed, prev_button_state):
 # Read the current state of the rotary encoder's CLK pin
    CLK_state = GPIO.input(CLK_PIN)

    # If the state of CLK is changed, then pulse occurred
    # React to only the rising edge (from LOW to HIGH) to avoid double count
    if CLK_state != prev_CLK_state and CLK_state == GPIO.HIGH:
        # If the DT state is HIGH, the encoder is rotating in counter-clockwise direction
        # Decrease the counter
        if GPIO.input(DT_PIN) == GPIO.HIGH:
            counter -= 1
            direction = DIRECTION_CCW
            menu.scroll_up()
        else:
            # The encoder is rotating in clockwise direction => increase the counter
            counter += 1
            direction = DIRECTION_CW
            menu.scroll_down()

        #print("Rotary Encoder:: direction:", "CLOCKWISE" if direction == DIRECTION_CW else "ANTICLOCKWISE","- count:", counter)

    # Save last CLK state
    prev_CLK_state = CLK_state
    return counter

def button(prev_button_state, button_pressed):
    button_state = GPIO.input(SW_PIN)
    if button_state != prev_button_state:
        time.sleep(0.01)  # Add a small delay to debounce
        if button_state == GPIO.LOW:
            print("The button is pressed")
            button_pressed = True
        else:
            button_pressed = False

    prev_button_state = button_state
    return button_pressed

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
            y = (i - self.start_index) * (self.oled.height / int(((self.oled.height/32)+1))) + 5
            if i == self.index:
                self.draw.rectangle((0, y - 5, self.oled.width - 1, y + 10), outline=255, fill=0)  # Highlight selected option
            self.draw.text((5, y - int(((self.oled.height/32)+ 1))), self.options[i], font=self.font, fill=255)

        self.oled.image(self.image)
        self.oled.show()

    def scroll_down(self):
        if self.index < len(self.options) - 1:
            self.index += 1
            if self.index >= self.start_index + int(((self.oled.height/32)+1)):  # If the selection moves beyond the visible options
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
# Pin numbers on Raspberry Pi
CLK_PIN = 22   # GPIO7 connected to the rotary encoder's CLK pin
DT_PIN = 23  # GPIO8 connected to the rotary encoder's DT pin
SW_PIN = 25   # GPIO25 connected to the rotary encoder's SW pin

DIRECTION_CW = 0
DIRECTION_CCW = 1

counter = 0
direction = DIRECTION_CW
CLK_state = 0
prev_CLK_state = 0

button_pressed = False
prev_button_state = GPIO.HIGH

# Configure GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# test scrolling
try:
    while True:
        #Scroll(prev_CLK_state, CLK_state, counter, direction, button_pressed, prev_button_state)
        #button(prev_button_state, button_pressed)
        CLK_state = GPIO.input(CLK_PIN)

        # If the state of CLK is changed, then pulse occurred
        # React to only the rising edge (from LOW to HIGH) to avoid double count
        if CLK_state != prev_CLK_state and CLK_state == GPIO.HIGH:
            # If the DT state is HIGH, the encoder is rotating in counter-clockwise direction
            # Decrease the counter
            if GPIO.input(DT_PIN) == GPIO.HIGH:
                counter -= 1
                direction = DIRECTION_CCW
                menu.scroll_up()
                menu.display_menu()
            else:
                # The encoder is rotating in clockwise direction => increase the counter
                counter += 1
                direction = DIRECTION_CW
                menu.scroll_down()
                menu.display_menu()

            print("Rotary Encoder:: direction:", "CLOCKWISE" if direction == DIRECTION_CW else "ANTICLOCKWISE","- count:", counter)

        # Save last CLK state
        prev_CLK_state = CLK_state
        

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on program exit