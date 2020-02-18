from PIL import Image
import sys
import os



class Pish:

    def __init__(self):

        self.image = None
        self.temp = None
        self.tempRGB = None
        self.gif = False
        self.ext = ('.jpg', '.png', '.jpeg', '.j2p', '.jpx', '.j2k', '.bmp', '.dib', '.gif')
        self.history = []
        self.counter = -1
        self.g = False

    def helpme(self):
        print("Here's a list of available functions and what each of them does:\n\n"
              ""
              "resize <image> <width> <height> - Resizes the image to the given width and height.\n"
              "                                  Height will automatically be adjusted if your only input is width\n"
              "                                  Example: resize image.jpg 1920 1080\n\n"
              ""
              "rotate <image> <deg> - Rotates the image by <deg> degrees clockwise. "
              "To rotate counter clockwise, type negative degrees.\n"
              "                       If you don't type a degree amount, the image will be rotated by 90° clockwise.\n"
              "                       Examples: rotate image.jpg 180 | rotate image.jpg -70 | rotate image.jpg\n\n"
              ""
              "crop <image> <x1> <x2> <y1> <y2> - Crops the image by length from <x1> to <x2> pixels and height from <y1> to <y2> pixels.\n"
              "                                   Example: crop image.jpg 200 800 400 900\n\n"
              ""
              "colors <image> <palette> - Choose between RGB, grayscale or an indexed color palette.\n"
              "                           Examples: colors image.jpg RGB | colors image.jpg grayscale | colors image.jpg indexed\n\n"
              ""
              "export <image> - Change file name and/or format. Example: export image.png\n\n"
              ""
              ""
              "list - Displays a list of all the files in the current directory.\n\n"
              ""
              ""
              "formats - Display all supported image formats.\n")

    def resize(self, inp):

        if self.image is None:
            print("No image is currently selected.")
            return

        if len(inp) == 2:
            print("No image size parameters given. Resize needs at least one size parameter.")
            exit()

        if len(inp) > 4:
            print("Too many parameters given. Resize needs a maximum of 2 parameters.")
            exit()



        if len(inp) == 3:

            if not inp[2].isdigit():
                print("Given parameter is not a number.")
                exit()

            try:
                img = self.temp
                basewidth = int(inp[2])
                wpercent = (basewidth / float(self.temp.size[0]))
                hsize = int((float(self.temp.size[1]) * float(wpercent)))
                img = img.resize((basewidth, hsize), Image.BILINEAR)
                self.temp = img

                if self.g:
                    img = self.tempRGB
                    basewidth = int(inp[1])
                    wpercent = (basewidth / float(self.tempRGB.size[0]))
                    hsize = int((float(self.tempRGB.size[1]) * float(wpercent)))
                    img = img.resize((basewidth, hsize), Image.BILINEAR)
                    self.tempRGB = img

            except Exception as e:
                print(e)

        elif len(inp) == 4:

            if not inp[2].isdigit() or not inp[3].isdigit():
                print("One or both of the given parameters is not a number.")
                exit()

            try:
                img = self.temp
                img = img.resize((int(inp[2]), int(inp[3])), Image.BILINEAR)
                self.temp = img

                if self.g:
                    img = self.tempRGB
                    img = img.resize((int(inp[2]), int(inp[3])), Image.BILINEAR)
                    self.tempRGB = img

            except Exception as e:
                print(e)
                return

        self.history.append((self.temp, self.tempRGB))
        self.counter += 1

    def save(self):

        if self.image is None:
            print("No image is currently selected.")
            return

        if self.temp is None:
            print("No image to save.")
            return

        name = input("Please type a name for the new image. Leaving this blank will override the original image:\n>")
        if name == "":
            name = self.image.filename.split(".")[0]
        newFormat = input('Keep current file format ({})? Y/N\n>'.format(self.image.format.lower()))

        try:
            if newFormat == "y":
                self.temp.save('{}.{}'.format(name, self.image.format.lower()))
            else:
                newFormat = input("Please enter a new format (like .png). If you do not know the available formats, type formats.\n>")
                if newFormat == "formats":
                    self.formats()
                    while True:
                        newFormat = input("Please select a format:\n>")
                        if newFormat in self.ext:
                            self.temp.save('{}{}'.format(name, newFormat))
                            break
                else:
                    if newFormat in self.ext:
                        self.temp.save('{}{}'.format(name, newFormat))
                    else:
                        print("Unsupported file format.")
                        exit()
        except Exception as e:
            print("and here we are")
            print(e)

    def export(self):

        if self.image is None:
            print("No image is currently selected.")
            return

        if self.temp is None:
            print("No image to save.")
            return

        name = input("Please type a name for the new image:\n>")
        newFormat = "n"

        try:
            if newFormat == "y":
                self.temp.save('{}.{}'.format(name, self.image.format.lower()))
            else:
                print('Current format: .{}'.format(self.image.format.lower()))
                newFormat = input("Please enter a new format (like .png). If you do not know the available formats, type formats.\n>")
                if newFormat == "formats":
                    self.formats()
                    while True:
                        newFormat = input("Please select a format:\n>")
                        if newFormat in self.ext:
                            if newFormat == ("." + self.image.format.lower()):
                                print("Image is already in this format.")
                                exit()
                            self.temp.save('{}{}'.format(name, newFormat))
                            break
                else:
                    if newFormat in self.ext:
                        if newFormat in self.ext:
                            if newFormat == ("." + self.image.format.lower()):
                                print("Image is already in this format.")
                                exit()
                        self.temp.save('{}{}'.format(name, newFormat))
                    else:
                        print("Unsupported file format.")
                        exit()
        except Exception as e:
            print("and here we are")
            print(e)

    def crop(self, c):

        # c = [x1 x2 y1 y2]

        if self.image is None:
            print("No image is currently selected.")
            return

        for i in c:
            if not i.isdigit():
                print('Given parameter is not a number: {}'.format(i))
                exit()

        img = self.temp
        img = img.crop((int(c[0]), int(c[2]), int(c[1]), int(c[3])))
        self.temp = img

        if self.g:
            img = self.tempRGB
            img = img.crop((int(c[0]), int(c[2]), int(c[1]), int(c[3])))
            self.tempRGB = img

        self.history.append((self.temp, self.tempRGB))
        self.counter += 1

    def rotate(self, deg):

        if self.image is None:
            print("No image is currently selected.")
            exit()

        if not deg.isdigit():
            print("Given argument is not a number.")
            exit()

        deg = int(deg)

        if deg < 0:
            deg = 360 + deg
        elif deg > 360:
            deg = deg // 360

        self.temp = self.temp.rotate(360-deg)

        if self.g:
            self.tempRGB = self.tempRGB.rotate(360-deg)

        self.history.append((self.temp, self.tempRGB))
        self.counter += 1

    def list(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(self.ext)]
        for f in files:
            print(f)

    def pick(self, t):

        if len(t) == 1:
            print("No image file selected, please type the image name after the pick command (pick image).")
            return

        if not os.path.isfile(t[1]):
            print("No such file.")
            exit()

        elif len(t) == 2:
            if ("." + t[1].split('.')[1]) not in self.ext:
                print('Unsupported file format: {}\nFor a list of supported formats, type formats'.format(t[1][-4:]))
                exit()
            self.gif = False
            self.temp = Image.open(t[1])
            self.image = Image.open(t[1])
            self.history = []
            self.history.append((self.temp, self.temp))

            temp = Image.open(t[1])

    def curr(self):
        if self.image is None:
            print("No image is currently selected. You can select an image by using the pick command")
            return
        print(self.image)

    def formats(self):
        print("Supported formats:")
        print('{}\n'.format(self.ext).replace("'", ""))

    def colors(self, t):
        if self.image is None:
            print("No image file selected.")
            return

        if len(t) == 2:
            print("No palette chosen. Available palettes are: RGB, grayscale, indexed")
            exit()

        palette = t[2].lower()

        if palette == "grayscale":
            self.g = True
            self.tempRGB = self.temp
            self.temp = self.temp.convert("L")
        elif palette == "indexed":

            if self.g:
                self.temp = self.tempRGB

            self.g = True

            newPal = int(input("Enter number of colors that you want in the new palette (number must be between 0 and 255):\n>"))
            if newPal > 256 or newPal < 0:
                while True:
                    newPal = int(input("The number is either too big or too small. Please enter a number between 0 and 255:\n>"))
                    if 0 < newPal < 256:
                        break
            self.tempRGB = self.temp
            self.temp = self.temp.quantize(newPal).convert('RGB')
        elif palette == "rgb":
            self.temp = self.temp.convert("RGB")
        else:
            print("Invalid palette name. Available palettes are: RGB, grayscale, indexed")
            exit()
        self.history.append((self.temp, self.tempRGB))
        self.counter += 1



new = True
edit = Pish()
print()

inp = sys.argv[1:]

if inp[0] == "help":
    edit.helpme()

elif inp[0] == "list":
    edit.list()

elif inp[0] == "formats":
    edit.formats()

elif inp[0] == "resize":
    if(len(inp) == 1):
        print("No image selected.")
        exit()
    edit.pick([0, inp[1]])
    edit.resize(inp)
    edit.save()

elif inp[0] == "export":
    if (len(inp) == 1):
        print("No image selected.")
        exit()
    edit.pick([0, inp[1]])
    edit.export()

elif inp[0] == "crop":
    if (len(inp) == 1):
        print("No image selected.")
        exit()
    edit.pick([0, inp[1]])
    if len(inp) < 6:
        print('Not enough cropping parameters. Required 4, received {}'.format(len(inp)-2))
        exit()
    elif len(inp) > 6:
        print('Too many cropping parameters. Required 4, received {}'.format(len(inp)-2))
        exit()
    edit.crop(inp[2:])
    edit.save()

elif inp[0] == "rotate":
    if (len(inp) == 1):
        print("No image selected.")
        exit()
    if len(inp) == 2:
        edit.pick([0, inp[1]])
        edit.rotate("90")

    if len(inp) > 3:
        print('Too many arguments. Required 1 or 0, received {}'.format(len(inp) - 1))
        exit()

    if len(inp) == 3:
        edit.pick([0, inp[1]])
        edit.rotate(inp[2])
    edit.save()

elif inp[0] == "colors":
    if (len(inp) == 1):
        print("No image selected.")
        exit()
    edit.pick([0, inp[1]])
    edit.colors(inp)
    edit.save()

else:
        print("Unrecognized command. Type help to see a list of available commands.")
