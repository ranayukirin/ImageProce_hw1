import numpy as np
import tkinter as tk
from PIL import ImageTk, Image # just for showing picture on GUI, NOT use for image loading or processing
from my_imfilter import my_imfilter
from gauss2D import gauss2D
from bitmap import Bitmap

window = tk.Tk()
window.title('HW1')
window.geometry('900x700')
starty = 0.5 * (700 - 512)

def Add_gaunoise(image, means, sigma):
    height, width = image.shape
    gauss_noise = np.random.normal(means, sigma, (height, width)).reshape(height, width)
    image += np.uint8(gauss_noise)
    return image
def Reset():
    global im_choose, imtk, lb2, choice
    if choice == 1:
        Lena()
    else:
        Babo()

# A. Reading RAW Image File
# read image with fromfile function
def Lena():
    global im_lena, im_choose, imtk, lb2, lb7, choice, save_str
    im_lena = np.fromfile('lena.raw', dtype=np.uint8).reshape((512, 512))
    im_choose = im_lena
    save_str = 'ori-lena.bmp'
    choice = 1
    lb7 = tk.Label(window, text='- Choose lena -',
                   width=20, height=1).place(x=362, y=60)
    Show_im()
def Babo():
    global im_babo, im_choose, imtk, lb2, lb7, choice, save_str
    im_babo = np.fromfile('BABOON.raw', dtype=np.uint8).reshape((512, 512))
    im_choose = im_babo
    save_str = 'ori-babo.bmp'
    choice = 0
    lb7 = tk.Label(window, text='- Choose baboon -',
                   width=20, height=1).place(x=362, y=60)
    Show_im()

# B. Spatial filtering
# Sobel
def Sobel():
    global im_choose, imtk, lb2, lb7, choice, save_str
    Reset()
    sobel_filterx = np.array([[-1, 0, 1],
                              [-2, 0, 2],
                              [-1, 0, 1]])
    sobel_filtery = np.array([[-1, -2, -1],
                              [0, 0, 0],
                              [1, 2, 1]])
    im_sobelx = np.squeeze(my_imfilter(im_choose, sobel_filterx), axis = 2)
    im_sobely = np.squeeze(my_imfilter(im_choose, sobel_filtery), axis = 2)
    im_choose = np.sqrt((im_sobelx * im_sobelx) + (im_sobely * im_sobely))
    if choice == 1:
        save_str = 'lena_sobel.bmp'
    else:
        save_str = 'babo_sobel.bmp'
    lb7 = tk.Label(window, text='- Contain x, y dir -',
                   width=20, height=1).place(x=362, y=60)
    Show_im()

# Laplacian
def Laplacian():
    global im_choose, imtk, lb2, lb7, choice, save_str
    Reset()
    laplacian_filter = np.array([[0, 1, 0],
                                 [1, -4, 1],
                                 [0, 1, 0]])
    #laplacian_filter = np.array([[0, 1, 1, 2, 2, 2, 1, 1, 0],
    #                             [1, 2, 4, 5, 5, 5, 4, 2, 1],
    #                             [1, 4, 5, 3, 0, 3, 5, 4, 1],
    #                             [2, 5, 3, -12, -24, -12, 3, 5, 2],
    #                             [2, 5, 0, -24, -40, -24, 0, 5, 2],
    #                             [2, 5, 3, -12, -24, -12, 3, 5, 2],
    #                             [1, 4, 5, 3, 0, 3, 5, 4, 1],
    #                             [1, 2, 4, 5, 5, 5, 4, 2, 1],
    #                             [0, 1, 1, 2, 2, 2, 1, 1, 0]])
    im_choose = np.squeeze(my_imfilter(im_choose, laplacian_filter), axis = 2)
    im_choose = np.uint8(255 * (im_choose - im_choose.min()) / (im_choose.max() - im_choose.min()))
    if choice == 1:
        save_str = 'lena_lapla.bmp'
    else:
        save_str = 'babo_lapla.bmp'
    lb7 = tk.Label(window, text='- Done laplacian -',
                   width=20, height=1).place(x=362, y=60)
    Show_im()

# Averaging
avg_filter = (1 / 9) * np.array([[1, 1, 1],
                                 [1, 1, 1],
                                 [1, 1, 1]])
#avg_filter = (1 / 25) * np.array([[1, 1, 1, 1, 1],
#                                  [1, 1, 1, 1, 1],
#                                  [1, 1, 1, 1, 1],
#                                  [1, 1, 1, 1, 1],
#                                  [1, 1, 1, 1, 1]])
def Averaging():
    global  avg_filter, im_choose, imtk, lb2, lb7, choice, save_str
    Reset()
    im_choose = np.squeeze(my_imfilter(im_choose, avg_filter), axis = 2)
    if choice == 1:
        save_str = 'lena_avg.bmp'
    else:
        save_str = 'babo_avg.bmp'
    lb7 = tk.Label(window, text='- Done averaging -',
                   width=20, height=1).place(x=362, y=60)
    Show_im()

# Gaussian
def Gaussian():
    global im_choose, imtk, lb2, lb7, choice, save_str
    Reset()
    gauss_filter = gauss2D(shape = (25, 25), sigma = 10)
    im_choose = np.squeeze(my_imfilter(im_choose, gauss_filter), axis = 2)
    if choice == 1:
        save_str = 'lena_gauss.bmp'
    else:
        save_str = 'babo_gauss.bmp'
    lb7 = tk.Label(window, text='- Done Gaussian -',
                   width=20, height=1).place(x=362, y=60)
    Show_im()

# C. Denoise
ety = tk.Entry(window, width = 15, show = None)
ety.place(x = 180, y = starty + 310)
# Apply gaussian noise
def Apply_gaunoise():
    global im_choose, imtk, lb2, lb7, choice, save_str
    Reset()
    sigma = float(ety.get())
    im_choose = Add_gaunoise(im_choose, 0, sigma)
    if choice == 1:
        save_str = 'lena_applygau.bmp'
    else:
        save_str = 'babo_applygau.bmp'
    lb7 = tk.Label(window, text='- OK, then denoise -',
                   width=20, height=1).place(x=362, y=60)
    Show_im()
# Denoise with smoothing filter
def Denoise():
    global im_choose, imtk, lb2, avg_filter, lb7, choice, save_str
    im_choose = np.squeeze(my_imfilter(im_choose, avg_filter), axis = 2)
    if choice == 1:
        save_str = 'lena_degauss.bmp'
    else:
        save_str = 'babo_degauss.bmp'
    lb7 = tk.Label(window, text='- Done denoise -',
                   width=20, height=1).place(x=362, y=60)
    Show_im()

# Gaussian 100
def Gaussian100():
    global im_choose, imtk, lb2, avg_filter, lb7, choice, save_str
    Reset()
    image100_avg = np.zeros(im_choose.shape)
    for times in range(100):
        image100_avg += Add_gaunoise(im_choose, 0, 1)
    im_choose = 0.01 * image100_avg
    if choice == 1:
        save_str = 'lena_gauss100.bmp'
    else:
        save_str = 'babo_gauss100.bmp'
    lb7 = tk.Label(window, text='- Done Gaussian100 -',
                   width=20, height=1).place(x=362, y=60)
    Show_im()

def Show_im():
    global im_choose, starty, imtk, lb2
    im_array = Image.fromarray(im_choose)
    imtk = ImageTk.PhotoImage(im_array, master=window)
    lb2 = tk.Label(window, image=imtk).place(x=350, y = starty)
def Save_im():
    global im_choose, imtk, lb2, lb7, save_str
    im_save = Bitmap(512, 512)
    im_save.setPixel(np.uint8(im_choose))
    im_save.write(save_str)
    lb7 = tk.Label(window, text = '- Done saving bmp -',
               width=20, height=1).place(x = 362, y = 60)

lb1 = tk.Label(window, text = 'Homework 1', bg = 'white',
               width=15, height=1).place(x = 380, y = 20)
lb3 = tk.Label(window, text = 'A. Reading RAW Image File',
               width=25, height=1).place(x = 26, y = starty)
btn1 = tk.Button(window, text = 'Choose Lena', width=15, height=2,
                command = Lena).place(x = 50, y = starty + 20)
btn2 = tk.Button(window, text = 'Choose Boba', width=15, height=2,
                command = Babo).place(x = 180, y = starty + 20)
lb4 = tk.Label(window, text = 'B. Spatial filtering',
               width=18, height=1).place(x = 22, y = starty + 65)
btn3 = tk.Button(window, text = 'Sobel', width=15, height=2,
                command = Sobel).place(x = 50, y = starty + 90)
btn4 = tk.Button(window, text = 'Laplacian', width=15, height=2,
                command = Laplacian).place(x = 50, y = starty + 135)
btn5 = tk.Button(window, text = 'Averaing', width=15, height=2,
                command = Averaging).place(x = 50, y = starty + 180)
btn6 = tk.Button(window, text = 'Gaussian', width=15, height=2,
                command = Gaussian).place(x = 50, y = starty + 225)
lb5 = tk.Label(window, text = 'C. Donise',
               width=18, height=1).place(x = 1, y = starty + 270)
lb6 = tk.Label(window, text = 'Please type 1,5,10',
               width=18, height=1).place(x = 170, y = starty + 290)
btn7 = tk.Button(window, text = 'Apply_gaussian', width=15, height=2,
                command = Apply_gaunoise).place(x = 50, y = starty + 290)
btn8 = tk.Button(window, text = 'Denoise', width=15, height=2,
                command = Denoise).place(x = 50, y = starty + 335)
btn9 = tk.Button(window, text = 'Gaussian100', width=15, height=2,
                command = Gaussian100).place(x = 50, y = starty + 380)
lb8 = tk.Label(window, text = 'D. Save image',
               width=18, height=1).place(x = 14, y = starty + 425)
btn10 = tk.Button(window, text = 'Save image', width=15, height=2,
                command = Save_im).place(x = 50, y = starty + 445)
lb9 = tk.Label(window, text = '*Every processing will reset to origin picture you choose first',
               width=70, height=1).place(x = 450, y = starty + 550)

window.mainloop()