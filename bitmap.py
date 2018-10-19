from struct import pack
import numpy as np

class Bitmap():
    def __init__(s, width, height):
        s._bfType = 19778 # Bitmap signature
        s._bfReserved1 = 0
        s._bfReserved2 = 0
        s._bcPlanes = 1
        s._bcSize = 12
        s._bcBitCount = 24
        s._bfOffBits = 26
        s._bcWidth = width
        s._bcHeight = height
        s._bfSize = 26+s._bcWidth*3*s._bcHeight
        s.clear()

    def clear(s):
        s._graphics = [(0,0,0)]*s._bcWidth*s._bcHeight

    def setPixel(s, image):
        for x in range(s._bcWidth):
            for y in range(s._bcHeight):
                s._graphics[y * 512 + x] = (image[s._bcHeight-1-y, x], image[s._bcHeight-1-y, x]
                                            , image[s._bcHeight-1-y, x])

    def write(s, file):
        with open(file, 'wb') as f:
            f.write(pack('<HLHHL',
                        s._bfType,
                        s._bfSize,
                        s._bfReserved1,
                        s._bfReserved2,
                        s._bfOffBits)) # Writing BITMAPFILEHEADER
            f.write(pack('<LHHHH',
                        s._bcSize,
                        s._bcWidth,
                        s._bcHeight,
                        s._bcPlanes,
                        s._bcBitCount)) # Writing BITMAPINFO
            for px in s._graphics:
                f.write(pack('<BBB', *px))
            for i in range (0, (s._bcWidth*3) % 4):
                f.write(pack('B', 0))

if __name__ == '__main__':
    side = 512
    b = Bitmap(side, side)
    im_lena = np.fromfile('lena.raw', dtype=np.uint8).reshape((512, 512))
    b.setPixel(im_lena)
    b.write('file.bmp')