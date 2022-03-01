'''
Author: Kevin Chen
Contact: kchen@bates.edu
Description: A file that contains Netpbm, an image utility class for modifying both .pgm and .ppm images. This project is an
attempt to reach A++ specifications.
'''

#imports
import copy
import random

#class
class Netpbm:

    '''
    Description:
        An Image processing utility class that reads, edits, and writes files of .pgm and .ppm format.
    '''

    __slots__ = ("_header", "_pixels")

    def __init__(self, filename: str):

        '''
        Description:
            A class initializer function that parses a given file to populate the __slots__ structure.

            Args:
                        filename (str): The path to an image file.
        '''

        image_file = open(filename, "r")

        # call method for reading header
        self._header = self.readHeader(image_file)

        # call method for reading pixels
        self._pixels = self.readPixels(image_file)

        image_file.close()

    def readHeader(self, image_file: 'TextIO') -> list:

        '''
        Description:
            A parser function that parses the header of the input file into a list of ints and strings. Note that .pgm and .ppm files have an identical header structure.

            Args:
                        image_file ('TextIO'): A handle to an opened image file.

            Returns:
                        A list populated by the following header elements: magic number (str), comment (str), columns and rows ([int, int]), and max level (int).
        '''

        # code for reading the header

        #magic number
        magic_number = image_file.readline().strip()

        #comment
        comment = image_file.readline().strip()

        #width and height
        columns_rows = [int(val) for val in image_file.readline().strip().split()]

        #max level
        max_gray_level = int(image_file.readline().strip())

        return [magic_number, comment, columns_rows, max_gray_level]

    def readPixels(self, image_file: 'TextIO') -> list:

        '''
        Description:
            A parser function that parses the image pixel data into a list. In the case of .pgm, it returns a one dimensional list of ints. In the case of .ppm, it returns a three dimensional array of rgb values of format [[r],[g],[b]]. This is distinct to the format [[rgb]], where each pixels rgb values are ajacent.

        Args:
                    image_file ('TextIO'): A handle to an opened image file.

        Returns:
                    A list populated by the pixel data. Either in the format [[r],[g],[b]] or [[rgb]].
        '''

        # code for reading the pixels
        columns = self.getNumCols()
        rows = self.getNumRows()

        pixel_line = []
        if self.isPGM():
            for i in range(rows * columns):
                pixel_line.extend([int(i) for i in image_file.readline().strip().split()])
        else:
            temp = []
            for i in range(rows * columns * 3):
                temp.extend([int(i) for i in image_file.readline().strip().split()])
            r = temp[::3]
            g = temp[1::3]
            b = temp[2::3]
            pixel_line = [r, g, b]

        return pixel_line

    '''
    Description:
        Various utility functions

    Functions:
                isPGM:          Returns true if image is .pgm format
                getMagicNumber: Getter for the header magic number.
                getComment:     Getter for the header comment.
                getNumCols:     Getter for the header column number.
                getNumRows:     Getter for the header row number.
                getMaxLevel:    Getter for the header max level.
                getHeader:      Getter for the header data.
                getPixels:      Getter for the pixel data.

    '''

    def getMagicNumber(self) -> str:
        return self._header[0]

    def isPGM(self) -> bool:
        return (True if self.getMagicNumber() == "P2" else False)

    def getComment(self) -> str:
        return self._header[1]

    def getNumCols(self) -> int:
        return self._header[2][0]

    def getNumRows(self) -> int:
        return self._header[2][1]

    def getMaxLevel(self) -> int:
        return self._header[3]

    def getHeader(self) -> list:
        return copy.deepcopy(self._header)

    def getPixels(self) -> list:
        return copy.deepcopy(self._pixels)



    def writeHeader(self, image_file: 'TextIO') -> None:

        '''
        Description:
            A  function that writes the header data to an image file.

        Args:
                    image_file ('TextIO'): A handle to an opened image file.
        '''

        #magic number
        image_file.write(f'{self._header[0]}\n')

        #comment
        image_file.write(f'{self._header[1]}\n')

        #width and height
        image_file.write(f'{self._header[2][0]} {self._header[2][1]}\n')

        #max level
        image_file.write(f'{self._header[3]}\n')



    def writePixels(self, image_file: 'TextIO') -> None:

        '''
        Description:
            A  function that writes pixel data to an image file. Works with both .pgm and .ppm files.

        Args:
                    image_file ('TextIO'): A handle to an opened image file.
        '''

        oldPixels = self.getPixels()

        if self.isPGM():
            for pixel in oldPixels:
                image_file.write(f'{pixel}\n')
        else:
            temp = []
            for i in range(len(oldPixels[0])):
                for rgb in range(3):
                    temp.append(oldPixels[rgb][i])

            for pixel in temp:
                image_file.write(f'{pixel}\n')



    def writeImage(self, filename: str) -> None:

        '''
        Description:
            A  function that writes image data to a file in .pgm or .ppm format.

        Args:
                    image_file ('TextIO'): A handle to an opened image file.
        '''

        image_file = open(filename, "w")

        self.writeHeader(image_file)
        self.writePixels(image_file)

        image_file.close()



    def changeBrightness(self, amount: int) -> None:

        '''
        Description:
            A  function that adjusts the brightness of the image. Works with both .pgm and .ppm files.

        Args:
                    amount (int): Amount of brightness to be added (can be negative).
        '''

        oldPixels = self.getPixels()
        newPixels = self.getPixels()
        maxLevel = self.getMaxLevel()

        #adjusting image brightness, including threshholds
        if self.isPGM():
            for i in range(len(oldPixels)):
                candidate = oldPixels[i] + amount

                if candidate >= 0 and candidate <= maxLevel:
                    newPixels[i] = candidate
                elif candidate <= 0:
                    newPixels[i] = 0
                elif candidate >= maxLevel:
                    newPixels[i] = maxLevel
        else:
            for i in range(len(oldPixels[0])):
                for rgb in range(3):
                    candidate = oldPixels[rgb][i] + amount

                    if candidate >= 0 and candidate <= maxLevel:
                        newPixels[rgb][i] = candidate
                    elif candidate <= 0:
                        newPixels[rgb][i] = 0
                    elif candidate >= maxLevel:
                        newPixels[rgb][i] = maxLevel

        self._pixels = newPixels



    def invert(self) -> None:

        '''
        Description:
            A function that inverts an image. Works with both .pgm and .ppm files.
        '''

        oldPixels = self.getPixels()
        newPixels = self.getPixels()
        maxLevel = self.getMaxLevel()

        #inverting the image by subtracting the pixel value from the max level
        if self.isPGM():
            for i in range(len(oldPixels)):
                newPixels[i] = maxLevel - oldPixels[i]
        else:
            for i in range(len(oldPixels[0])):
                for rgb in range(3):
                    newPixels[rgb][i] = maxLevel - oldPixels[rgb][i]

        self._pixels = newPixels



    def rotate(self, rotate_right: bool = True) -> None:

        '''
        Description:
            A function that rotates an image 90 degrees clockwise or anti-clockwise. Works with both .pgm and .ppm files.

        Args:
                    rotate_right (bool): If true, rotate clockwise, otherwise rotate anti-clockwise.
        '''

        oldPixels = self.getPixels()
        newPixels = self.getPixels()
        columns = self.getNumCols()
        rows = self.getNumRows()

        #simplified x y transforms on a one dimensional array to rotate the image
        if self.isPGM():
            for c in range(columns):
                for r in range(rows):
                    if rotate_right:
                        newPixels[c * rows + r] = oldPixels[(-1 - r + rows) * columns + c]
                    else:
                        newPixels[(c - 1) * -rows + r] = oldPixels[r * columns + c]
        else:
            for c in range(columns):
                for r in range(rows):
                    for rgb in range(3):
                        if rotate_right:
                            newPixels[rgb][c * rows + r] = oldPixels[rgb][(-1 - r + rows) * columns + c]
                        else:
                            newPixels[rgb][(c - 1) * -rows + r] = oldPixels[rgb][r * columns + c]

        self._header[2][0] = rows
        self._header[2][1] = columns
        self._pixels = newPixels



    def flip(self, vertical: bool = True) -> None:

        '''
        Description:
            A function that mirrors the image about the x or y axis. Works with both .pgm and .ppm files.

        Args:
                    vertical (bool): If true, reflect about the x-axis, otherwise reflect about the y-axis.
        '''

        oldPixels = self.getPixels()
        newPixels = self.getPixels()
        columns = self.getNumCols()
        rows = self.getNumRows()

        #simplified x y transforms on a one dimensional array to flip the image
        if self.isPGM():
            for c in range(columns):
                for r in range(rows):
                    if vertical:
                        newPixels[r * columns + c] = oldPixels[((rows - 1 - r) * columns) + c]
                    else:
                        newPixels[r * columns + c] = oldPixels[(r * columns) + (columns - 1 - c)]
        else:
            for c in range(columns):
                for r in range(rows):
                    for rgb in range(3):
                        if vertical:
                            newPixels[rgb][r * columns + c] = oldPixels[rgb][((rows - 1 - r) * columns) + c]
                        else:
                            newPixels[rgb][r * columns + c] = oldPixels[rgb][(r * columns) + (columns - 1 - c)]

        self._pixels = newPixels

    def posterize(self, num_levels: int) -> None:

        '''
        Description:
            A function that applies a posterize effect to the image. Works with both .pgm and .ppm files.

        Args:
                    num_levels (int): The number of bins to be used.
        '''

        oldPixels = self.getPixels()
        newPixels = self.getPixels()
        maxLevel = self.getMaxLevel()

        #binning the pixel levels
        binWidth = (maxLevel + 1) / num_levels

        if self.isPGM():
            for i in range(len(oldPixels)):
                newPixels[i] = int(oldPixels[i] / binWidth)
        else:
            for i in range(len(oldPixels[0])):
                for rgb in range(3):
                    newPixels[rgb][i] = int(oldPixels[rgb][i] / binWidth)

        self._pixels = newPixels
        self._header[3] = num_levels - 1

    def crop(self, upper_left_row: int, upper_left_column: int, lower_right_row: int, lower_right_column: int) -> None:

        '''
        Description:
            A function that crops the image. Works with both .pgm and .ppm files.

        Args:
                    upper_left_row (int):       y value of Upper left corner of selection
                    upper_left_column (int):    x value of Upper left corner of selection
                    lower_right_row (int):      y value of Lower right corner of selection
                    lower_right_column (int):   x value of Lower right corner of selection
        '''

        oldPixels = self.getPixels()
        columns = self.getNumCols()
        rows = self.getNumRows()

        #simplified x y transforms on a one dimensional array to crop the image
        if self.isPGM():
            newPixels = []
            for c in range(upper_left_column, lower_right_column):
                for r in range(upper_left_row, lower_right_row):
                    newPixels.append(oldPixels[r * columns + c])
        else:
            newPixels = [[],[],[]]
            for c in range(upper_left_column, lower_right_column):
                for r in range(upper_left_row, lower_right_row):
                    for rgb in range(3):
                        newPixels[rgb].append(oldPixels[rgb][r * columns + c])

        self._header[2][0] = lower_right_row - upper_left_row
        self._header[2][1] = lower_right_column - upper_left_column
        self._pixels = newPixels

        #extra transforms to fix the coordinates
        self.rotate(True)
        self.flip(False)

    def toGrayscale(self) -> None:

        '''
        Description:
            A function that converts a .ppm file into grayscale (.pgm).
        '''

        oldPixels = self.getPixels()

        #converting the image to grayscale and modifiying the header appropriately
        if self.isPGM():
            pass
        else:
            temp = []
            for i in range(len(oldPixels[0])):
                temp.append(int((0.2126 * oldPixels[0][i]) + (0.7152 * oldPixels[1][i]) + (0.0722 * oldPixels[2][i])))
            self._pixels = temp
            self._header[0] = "P2"

    def glass(self, radius: int) -> None:

        '''
        Description:
           A function that applies a glassy effect to the image. Works with both .pgm and .ppm files.

        Args:
                    radius (int):   The radius of blur (pixel randomization).
        '''

        oldPixels = self.getPixels()
        newPixels = self.getPixels()
        columns = self.getNumCols()
        rows = self.getNumRows()

        #lambda function for wrap algorithm
        wrap = lambda a, b, o : ((a + o) + b) % b

        #applying a glass effect to the image through pixel manipulation, appends original pixel to the new empty lists
        if self.isPGM():
            for c in range(columns):
                for r in range(rows):
                    o1 = random.randint(-radius, radius)
                    o2 = random.randint(-radius, radius)
                    newPixels[r * columns + c] = oldPixels[wrap(r, rows, o1) * columns + wrap(c, columns, o2)]
        else:
            for c in range(columns):
                for r in range(rows):
                    o1 = random.randint(-radius, radius)
                    o2 = random.randint(-radius, radius)
                    for rgb in range(3):
                        newPixels[rgb][r * columns + c] = oldPixels[rgb][wrap(r, rows, o1) * columns + wrap(c, columns, o2)]

        self._pixels = newPixels

    def halve(self) -> None:

        '''
        Description:
           A function that reduces the resolution of the image by half. Works with both .pgm and .ppm files.
        '''

        oldPixels = self.getPixels()
        columns = self.getNumCols()
        rows = self.getNumRows()

        #reducing resolution by half
        if self.isPGM():
            newPixels = []
            for c in range(int(columns / 2)):
                for r in range(int(rows / 2)):
                    newPixels.append(oldPixels[(r * 2) * columns + (c * 2)])
        else:
            newPixels = [[],[],[]]
            for c in range(int(columns / 2)):
                for r in range(int(rows / 2)):
                    for rgb in range(3):
                        newPixels[rgb].append(oldPixels[rgb][(r * 2) * columns + (c * 2)])

        self._header[2][0] = int(rows / 2)
        self._header[2][1] = int(columns / 2)
        self._pixels = newPixels

        #extra transforms to fix the coordinates
        self.rotate(False)
        self.flip(True)

    def double(self) -> None:

        '''
        Description:
           A function that doubles the size of the image. Works with both .pgm and .ppm files.
        '''

        oldPixels = self.getPixels()
        columns = self.getNumCols()
        rows = self.getNumRows()

        #doubling image size
        if self.isPGM():
            newPixels = []
            for c in range(columns * 2):
                for r in range(rows * 2):
                    newPixels.append(oldPixels[int(r / 2) * columns + int(c / 2)])
        else:
            newPixels = [[],[],[]]
            for c in range(columns * 2):
                for r in range(rows * 2):
                    for rgb in range(3):
                        newPixels[rgb].append(oldPixels[rgb][int(r / 2) * columns + int(c / 2)])

        self._header[2][0] = rows * 2
        self._header[2][1] = columns * 2
        self._pixels = newPixels

        #extra transforms to fix the coordinates
        self.rotate(False)
        self.flip(True)
