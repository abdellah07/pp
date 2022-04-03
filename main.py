import sys

import PIL.Image
from PIL import Image
import numpy as np


# creates gaussian kernel with side length `l` and a sigma of `sig`
def initKernet(size=5, sig=1.):
    ax = np.linspace(-(size - 1) / 2., (size - 1) / 2., size)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel)


def processPixel(img, newImage, xp, yp, kernel, color):
    colorValue = 0
    for x in range(0, len(kernel)):
        for y in range(0, len(kernel)):
            padding = int((len(kernel) / 2))
            if 0 <= xp + x - padding < len(img[0]) and 0 <= yp + y - padding < len(img):
                colorValue += img[yp + y - padding][xp + x - padding][color] * kernel[x][y]
            else:
                colorValue += img[yp][xp][0] * kernel[x][y]
    newImage[yp][xp][color] = np.uint8(colorValue)


def processGauss(img, newImg, size=5, sig=1.):
    matrix = initKernet(size, sig)
    for y in range(0, len(img)):
        for x in range(0, len(img[0])):
            for c in range(0, 3):
                processPixel(img, newImg, x, y, matrix, c)
    return newImg


def generatePic(newImgArray, output):
    newImgArray = np.asarray(newImgArray)
    newImage = PIL.Image.fromarray(newImgArray)
    newImage.save(output)


def process(input, output, size=5, sig=1.):
    img = Image.open(input)
    newImgArray = np.asarray(img)
    processGauss(np.asarray(img), newImgArray, size, sig)
    generatePic(newImgArray, output)


def decodeOptions(options):
    tx = "--tx"
    ty = "--ty"
    gsize = "--gsize"
    gsigma = "--gsigma"

    txValue = 0
    tyValue = 0
    gsizeValue = 5
    gsigmaValue = 1.

    for i in range(0, len(options)):
        option = options[i]
        if option == tx:
            txValue = int(options[i + 1])
        elif option == ty:
            tyValue = int(options[i + 1])
        elif option == gsize:
            gsizeValue = int(options[i + 1])
        elif option == gsigma:
            gsigmaValue = int(options[i + 1])

    return txValue, tyValue, gsizeValue, gsigmaValue;


def runGauss():
    inputFile = sys.argv[len(sys.argv) - 2]
    outputFile = sys.argv[len(sys.argv) - 1]
    # TODO python3 yourSurname.py --tx 16 --ty 8 --gsize 7 --gsigma 100  monaLisa.jpg monaLisaBlurry.jpg
    txValue, tyValue, gsizeValue, gsigmaValue = decodeOptions(sys.argv)
    process(inputFile, outputFile, gsizeValue, gsigmaValue)


if __name__ == '__main__':
    runGauss()
