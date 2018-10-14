import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from PIL import ImageTk, Image # just for showing picture on GUI, NOT use for image loading or processing
from my_imfilter import my_imfilter
from gauss2D import gauss2D

window = tk.Tk()
window.title('HW1')
window.geometry('900x700')
starty = 0.5 * (700 - 512)

def Add_gaunoise(image, means, sigma):
    height, width = image.shape
    gauss_noise = np.random.normal(means, sigma, (height, width)).reshape(height, width)
    image += np.uint8(gauss_noise)
    return image

# A. Reading RAW Image File
# read image with fromfile function
def Lena():
    global im_lena, im_choose, imtk, lb2
    im_lena = np.fromfile('lena.raw', dtype=np.uint8).reshape((512, 512))
    im_choose = im_lena
    Show_im()
def Babo():
    global im_babo, im_choose, imtk, lb2
    im_babo = np.fromfile('BABOON.raw', dtype=np.uint8).reshape((512, 512))
    im_choose = im_babo
    Show_im()

# B. Spatial filtering
# Sobel
def Sobel():
    global im_choose, imtk, lb2
    sobel_filter = np.array([[-1, 0, 1],
                             [-2, 0, 2],
                             [-1, 0, 1]])
    im_choose = np.squeeze(my_imfilter(im_choose, sobel_filter), axis=2)
    Show_im()

# Laplacian
def Laplacian():
    global im_choose, imtk, lb2
    laplacian_filter = np.array([[0, 1, 0],
                                 [1, -4, 1],
                                 [0, 1, 0]])
    im_choose = np.squeeze(my_imfilter(im_choose, laplacian_filter), axis=2)
    Show_im()

# Averaging
avg_filter = (1 / 9) * np.array([[1, 1, 1],
                                [1, 1, 1],
                                [1, 1, 1]])
def Averaging():
    global  avg_filter, im_choose, imtk, lb2
    im_choose = np.squeeze(my_imfilter(im_choose, avg_filter), axis=2)
    Show_im()

# Gaussian
def Gaussian():
    global im_choose, imtk, lb2
    gauss_filter = gauss2D(shape=(25, 25), sigma=10)
    im_choose = np.squeeze(my_imfilter(im_choose, gauss_filter), axis=2)
    Show_im()

# C. Denoise
ety = tk.Entry(window, width = 15, show = None)
ety.place(x = 180, y = starty + 245)
# Apply gaussian noise
def Apply_gaunoise():
    global im_choose, imtk, lb2
    sigma = float(ety.get())
    im_choose = Add_gaunoise(im_choose, 0, sigma)
    Show_im()
# Denoise with smoothing filter
def Denoise():
    global im_choose, imtk, lb2, avg_filter
    im_choose = np.squeeze(my_imfilter(im_choose, avg_filter), axis=2)
    Show_im()

# Gaussian 100
click = 0
def Gaussian100():
    global im_choose, imtk, lb2, avg_filter, click
    image100 = np.zeros((512, 512, 100))
    for depth in range(100):
        image100[:, :, depth] = Add_gaunoise(im_choose, 0, 1)
    image100_avg = np.zeros(im_choose.shape)
    for times in range(100):
        image100_avg += image100[:, :, times]
    click += 1
    im_choose = 0.01 * image100_avg
    Show_im()

def Show_im():
    global im_choose, starty, imtk, lb2
    im_array = Image.fromarray(im_choose)
    imtk = ImageTk.PhotoImage(im_array, master=window)
    lb2 = tk.Label(window, image=imtk).place(x=350, y = starty)

btn1 = tk.Button(window, text='Choose Lena', width=15, height=2,
                command = Lena).place(x = 50, y = starty)
btn2 = tk.Button(window, text='Choose Boba', width=15, height=2,
                command = Babo).place(x = 180, y = starty)
btn3 = tk.Button(window, text='Sobel', width=15, height=2,
                command = Sobel).place(x = 50, y = starty + 45)
btn4 = tk.Button(window, text='Laplacian', width=15, height=2,
                command = Laplacian).place(x = 50, y = starty + 90)
btn5 = tk.Button(window, text='Averaing', width=15, height=2,
                command = Averaging).place(x = 50, y = starty + 135)
btn6 = tk.Button(window, text='Gaussian', width=15, height=2,
                command = Gaussian).place(x = 50, y = starty + 180)
lb1 = tk.Label(window, text='Please type 1,5,10',
               width=18, height=1).place(x = 170, y = starty + 225)
btn7 = tk.Button(window, text='Apply_gaussian', width=15, height=2,
                command = Apply_gaunoise).place(x = 50, y = starty + 225)
btn8 = tk.Button(window, text='Denoise', width=15, height=2,
                command = Denoise).place(x = 50, y = starty + 270)
btn9 = tk.Button(window, text='Gaussian100', width=15, height=2,
                command = Gaussian100).place(x = 50, y = starty + 315)

window.mainloop()