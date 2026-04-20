import sys
import random
from pyfiglet import Figlet

if len(sys.argv) not in [1, 3]:
    sys.exit("Invalid usage")

figlet = Figlet()

if len(sys.argv) == 3:
    if  sys.argv[1] not in ["-f", "--font"]:
        sys.exit("Invalid usage")
    if  sys.argv[2] not in figlet.getFonts():
        sys.exit("Invalid usage")
    figlet.setFont(font=sys.argv[2])

else:
    random_font = random.choice(figlet.getFonts())
    figlet.setFont(font=random_font)

text = input("input: ")
print(figlet.renderText(text))
