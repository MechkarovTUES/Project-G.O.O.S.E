import subprocess
import os

home_dir = os.path.expanduser("~")
print(home_dir)

# Change directory to the home directory
os.chdir(home_dir)

cmd = "sudo raspi-config"
output = subprocess.check_output(cmd, shell=True).decode("utf-8")
print(output)

#subprocess.run(cmd, shell=True)
# files = output.split("\n")

# for file in files:
#     print(file)
