import sys
import os
from PIL import Image, ImageOps


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python shirt.py input_image output_image")

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    valid_ext = (".jpg", ".jpeg", ".png")
    input_ext = os.path.splitext(input_path)[1].lower()
    output_ext = os.path.splitext(output_path)[1].lower()

    if input_ext not in valid_ext or output_ext not in valid_ext:
        sys.exit("Invalid input")

    if input_ext != output_ext:
        sys.exit("Input and output have different extensions")

    try:
        input_image = Image.open(input_path)
        shirt = Image.open("shirt.png")
    except FileNotFoundError:
        sys.exit("File not found")

    fitted_image = ImageOps.fit(input_image, shirt.size)
    fitted_image.paste(shirt, shirt)
    fitted_image.save(output_path)


if __name__ == "__main__":
    main()

