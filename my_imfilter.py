import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
#from gauss2D import gauss2D
import os

#  function can let image to column (actually raw in my code) so that filter can product a matrix directly
def im2col(image, k_height, k_width):
    col_image = []
    for i in range(0, image.shape[0] - k_height + 1):
        for j in range(0, image.shape[1] - k_width + 1):
            col = image[i:i + k_height, j:j + k_width].reshape([-1])
            col_image.append(col)
    col_image = np.array(col_image)

    return col_image

def my_imfilter(image, imfilter):
    if image.ndim == 3:
        channel = 3
    else:
        channel = 1
        image = image[:,:, np.newaxis]

    #  take the width and height of image and calculate the number we should pad later
    im_width = imfilter.shape[1]
    im_height = imfilter.shape[0]
    pad_width = im_width // 2
    pad_height = im_height // 2

    #  let the filter to be column
    col_filter = imfilter.reshape([-1])
    #  pad the image to keep the size of result from input
    image_pad = np.pad(image, ((pad_height, pad_height), (pad_width, pad_width), (0, 0)),  'reflect')
    #  do filtering with two matrix
    im_filted = np.zeros(image.shape)
    for i in range(0, channel):
        col_image = im2col(image_pad[:, :, i], im_height, im_width)
        im_filted[:, :, i] = np.reshape(np.dot(col_image, col_filter), image[:, :, i].shape)

    return im_filted

#  to test my_imfilter by itself
if __name__ == "__main__":
    filt_test = np.array([[1, 2, 3, 4, 5], [4, 5, 6, 7, 8], [7, 8, 9, 10, 11]])
    #filt_test = gauss2D(shape=(29, 29), sigma=7)
    main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image = mpimg.imread(os.path.join(main_path, 'data', 'dog.bmp'))
    image = image.astype(np.float32) / 255
    img = np.ones((28, 28, 3))
    print('Image read and its shape is '+ str(image.shape))
    im_filted = my_imfilter(image, filt_test)
    plt.figure(1)
    plt.imshow(im_filted)
    plt.show()