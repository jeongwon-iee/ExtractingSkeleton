from PIL import Image


def convert_rgb(pixel):
    if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
        return 0
    return 1


class ImageConverter:
    def __init__(self, filename):
        path = "../image/crows/"
        self.image = Image.open(path + filename)
        self.width, self.height = self.image.size
        self.pixels = [[0] * self.width for row in range(self.height)]
        self.initialize_pixels()

    def initialize_pixels(self):
        self.image = self.image.convert('RGBA')
        for row in range(0, self.height):
            for column in range(0, self.width):
                self.pixels[row][column] = self.image.getpixel((column, row))
                self.pixels[row][column] = convert_rgb(self.pixels[row][column])
          #     self.pixels[row][column] = convert_into_binary(self.pixels[row][column])
                # print(self.pixels[row][column], end=' ')
            # print()