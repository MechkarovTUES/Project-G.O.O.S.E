import subprocess
from PIL import Image, ImageDraw, ImageFont
import os

home_dir = os.path.expanduser("~")
print(home_dir)

# Change directory to the home directory
os.chdir(home_dir)

# Run raspi-config and capture its output
cmd = "sudo raspi-config"
output = subprocess.check_output(cmd, shell=True).decode("utf-8")

# Convert the output text to an image
image = Image.new("RGB", (800, 600), color="white")
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Split the output into lines and draw each line on the image
y = 0
for line in output.split("\n"):
    draw.text((10, y), line, fill="black", font=font)
    y += 10  # Increase y-coordinate for the next line

# Save or display the image
image.show()  # Display the image
# image.save("raspi_config_output.png")  # Save the image to a file
