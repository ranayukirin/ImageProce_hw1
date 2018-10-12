import numpy as np
import tkinter
import matplotlib.pyplot as plt
import random
from my_imfilter import my_imfilter
from gauss2D import gauss2D

def GaussianNoise(image, means, sigma):
    height = image.shape[0]
    width = image.shape[1]
    for i in range(height):
        for j in range(width):
            image[i, j] = image[i, j] + random.gauss(means, sigma)
            if image[i, j] < 0:
                image[i, j] = 0
            elif image[i, j] > 255:
                image[i, j] = 255
    return image


# A. Reading RAW Image File
# read image with fromfile function
im_lena = np.fromfile('lena.raw', dtype=np.uint8).reshape((512, 512))
im_babo = np.fromfile('BABOON.raw', dtype=np.uint8).reshape((512, 512))
# plt.imshow(im_lena, cmap = 'gray')
# plt.imshow(im_babo, cmap = 'gray')
# plt.show()

# B. Spatial filtering
# Sobel
sobel_filter = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]])
im_sobel = np.squeeze(my_imfilter(im_lena, sobel_filter), axis=2)
# Laplacian
laplacian_filter = np.array([[0, 1, 0],
                             [1, -4, 1],
                             [0, 1, 0]])
im_lap = np.squeeze(my_imfilter(im_lena, laplacian_filter), axis=2)
# Averaging
avg_filter = (1 / 9) * np.array([[1, 1, 1],
                                 [1, 1, 1],
                                 [1, 1, 1]])
im_avg = np.squeeze(my_imfilter(im_lena, avg_filter), axis=2)
# Gaussian
gauss_filter = gauss2D(shape=(25, 25), sigma=10)
im_gauss = np.squeeze(my_imfilter(im_lena, gauss_filter), axis=2)

# C. Denoise
gaunoise_1 = GaussianNoise(im_lena, 0, 1)
gaunoise_2 = GaussianNoise(im_lena, 0, 5)
gaunoise_3 = GaussianNoise(im_lena, 0, 10)
gaunoise_avg1 = np.squeeze(my_imfilter(gaunoise_1, avg_filter), axis=2)
gaunoise_avg2 = np.squeeze(my_imfilter(gaunoise_2, avg_filter), axis=2)
gaunoise_avg3 = np.squeeze(my_imfilter(gaunoise_3, avg_filter), axis=2)

image100 = np.zeros((512, 512, 100))
for depth in range(100):
    image100[:, :, depth] = GaussianNoise(im_lena, 0, 0.5)
image100_avg = np.zeros(im_lena.shape)
for times in range(100):
    image100_avg += image100[:, :, times]
image100_avg = 0.01 * image100_avg
plt.imshow(image100_avg, cmap = 'gray')
plt.show()
