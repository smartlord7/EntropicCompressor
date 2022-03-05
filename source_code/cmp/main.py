"""------------COMPRESSAO DE IMAGEM------------
Universidade de Coimbra
Licenciatura em Engenharia Informatica
Multimedia
Terceiro ano, segundo semestre
Authors:
Rui Bernardo Lopes Rodrigues
Sancho Amaral Simões, 2019217590, uc2019217590@student.uc.pt
Tiago Filipe Santa Ventura, 2019243695, uc2019243695@student.uc.pt
19/12/2020
---------------------------------------------------------------------------"""

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as clr


def show_images(images):
    """
      Given one or more images,this function will show them in order
      :param images: the image(s) to show.
      :return:
    """
    t = type(images)

    if t == dict:
        for image_name in images:
            plt.figure()
            plt.title(image_name)
            plt.imshow(images[image_name])
            plt.show()
    elif t == list:
        for image in images:
            plt.figure()
            plt.imshow(image)
            plt.show()
    else:
        plt.figure()
        plt.imshow(images)
        plt.show()


def read_images(directory, ext):
    """
          Given one directory and a file extension,this function will create a dictionary of the images in the directory.
          :param directory: the image(s) directory.
          :param ext: the image(s) extension.
          :return: dictionary with the images.
    """
    images = dict()

    for image_name in os.listdir(directory):
        if image_name.endswith(ext):
            image = plt.imread(directory + image_name)
            print("Read %s - shape: %s, type: %s" % (image_name, image.shape, image.dtype))
            images[image_name] = image

    return images


def read_images2(directory, ext):
    """
             Given one directory and a file extension,this function will create a dictionary of the images in the directory.
             :param directory: the image(s) directory.
             :param ext: the image(s) extension.
             :return: dictionary with the images.
    """
    images = dict()

    for image_name in os.listdir(directory):
        if image_name.endswith(ext):
            image = Image.open(directory + image_name)
            images[image_name] = image

    return images


def separate_rgb(img, show_plots=False):
    """
             Separates the rgb channels of an image.
             :param img: the image.
             :param show_plots: flag that toggles if it plots the channels.
             :return: RGB channels matrix.
    """
    r, g, b = img.copy(), img.copy(), img.copy()
    r[:, :, (1, 2)] = 0
    g[:, :, (0, 2)] = 0
    b[:, :, (0, 1)] = 0

    if show_plots:
        img_rgb = np.concatenate((r, g, b))
        plt.figure()
        plt.imshow(img_rgb)
        plt.show()

    return img[:, :, 0], img[:, :, 1], img[:, :, 2]


def join_channels(c1, c2, c3):
    """
             Function that joins the RGB channels in one.
             :param c1: RGB Channel 1.
             :param c2: RGB Channel 2.
             :param c3: RGB Channel 3.
             :return: image that results in the of the 3 channels.
    """
    shape = (c1.shape[0], c2.shape[1], 3)
    image = np.zeros(shape)
    image[:, :, 0] = c1
    image[:, :, 1] = c2
    image[:, :, 2] = c3

    return image


def float_to_uint8(matrix):
    """
                Converts float to uint8.
                :param matrix: Matrix with the floats.
                :return: UINT8 converted matrix.
    """
    matrix = matrix.round()
    matrix[matrix > 255] = 255
    matrix[matrix < 0] = 0
    matrix = matrix.astype(np.uint8)

    return matrix


def rgb_to_y_cb_cr(rgb, y_cb_cr_matrix, show_plots=False):
    """
                Converts RGB to YCBCR.
                :param rgb: RGB matrix.
                :param y_cb_cr_matrix: YCBCR default values matrix.
                :param show_plots: flag that enables plotting.
                :return: YCBCR converted matrix.
    """
    y_cb_cr = rgb.dot(y_cb_cr_matrix.T)
    y_cb_cr[:, :, [1, 2]] += 128

    if show_plots:
        plt.figure()
        plt.imshow(np.concatenate((y_cb_cr[:, :, 0], y_cb_cr[:, :, 1], y_cb_cr[:, :, 2])))
        plt.show()

    return y_cb_cr


def y_cb_cr_to_rgb(y_cb_cr, y_cb_cr_inverse_matrix, show_plots=False):
    """
                    Converts RGB to YCBCR.
                    :param y_cb_cr: YCBCR matrix.
                    :param y_cb_cr_inverse_matrix: YCBCR inverse default values matrix.
                    :param show_plots: flag that enables plotting.
                    :return: RGB converted matrix.
    """
    y_cb_cr[:, :, [1, 2]] -= 128
    rgb = y_cb_cr.dot(y_cb_cr_inverse_matrix.T)
    rgb = float_to_uint8(rgb)

    if show_plots:
        plt.figure()
        plt.imshow(rgb)
        plt.show()

    return rgb


def jpeg_compress_images(directory, ext, out_dir, quality_rates):
    """
                        Compresses images.
                        :param directory: images directory.
                        :param ext: images extension.
                        :param out_dir: output directory.
                        :param quality_rates: the quality rates of the compression.
                        :return:
    """
    images = read_images2(directory, ext)
    fig, axis = plt.subplots(len(images), len(quality_rates))
    i = 0

    for image_name in images.keys():
        j = 0
        for quality_rate in quality_rates:
            compressed_image_name = image_name.replace(ext, "") + str(quality_rate) + ".jpg"
            compress_image_path = out_dir + "/" + compressed_image_name
            images[image_name].save(compress_image_path, quality=quality_rate)
            image = plt.imread(compress_image_path)
            axis[i, j].imshow(image)
            axis[i, j].set_title(compressed_image_name, fontsize=10)

            j += 1

        i += 1

    plt.show()


def generate_linear_colormap(color_list):
    """
                            Generates the colormap.
                           :param color_list: list of colors.
                           :return: the colormap.
    """
    colormap = clr.LinearSegmentedColormap.from_list('cmap', color_list, N=256)

    return colormap


def plot_image_colormap(image_channel, colormap):
    """
                               Plot the images with the colormap.
                              :param image_channel: the channel to use in the colormap.
                              :return:
    """
    plt.figure()
    plt.imshow(image_channel, colormap)
    plt.show()


def apply_padding(image, wanted_rows, wanted_cols):
    """
                            Applies padding to the image.
                            :param image: the image to pad.
                            :param wanted_rows: number of rows to pad.
                            :param wanted_cols: number of columns to pad.
                            :return: the image with padding.
    """
    n_rows = image.shape[0]
    n_cols = image.shape[1]

    remaining = n_rows % wanted_rows

    if remaining != 0:
        remaining = wanted_rows - remaining
        last_row = image[n_rows - 1]
        rows_to_add = np.repeat([last_row], remaining, axis=0)
        image = np.vstack((image, rows_to_add))

    remaining = n_cols % wanted_cols

    if remaining != 0:
        remaining = wanted_cols - remaining
        last_col = image[:, [-1]]
        image = np.hstack((image, np.tile(last_col, (remaining, 1))))

    return image


def reverse_padding(padded_image, original_rows, original_cols):
    """
                                Reverses the padding.
                                :param padded_image: the padded image to unpad.
                                :param original_rows: number of original rows.
                                :param original_cols: number of original columns.
                                :return: the original image.
    """
    n_rows = padded_image.shape[0]
    n_cols = padded_image.shape[1]

    rows_to_delete = n_rows - original_rows
    rows_to_delete = [i for i in range(n_rows - rows_to_delete - 1, n_rows - 1)]

    if rows_to_delete != 0:
        padded_image = np.delete(padded_image, rows_to_delete, axis=0)

    cols_to_delete = n_cols - original_cols
    cols_to_delete = [i for i in range(n_cols - cols_to_delete - 1, n_cols - 1)]

    if cols_to_delete != 0:
        padded_image = np.delete(padded_image, cols_to_delete, axis=1)

    return padded_image


def down_sample(cb, cr, variant, f):
    """
                                    Function to down sample.
                                    :param cb: CB channel.
                                    :param cr: CR channel.
                                    :param variant: downsampling variant.
                                    :param f: downsampling factor.
                                    :return: the downsampled channels.
    """
    if variant == 1:
        cb_down_sampled = cb[:, 0::f]
        cr_down_sampled = cr[:, 0::f]
    elif variant == 2:
        cb_down_sampled = cb[0::f, 0::f]
        cr_down_sampled = cr[0::f, 0::f]
    else:
        return cb, cr

    return cb_down_sampled, cr_down_sampled


def up_sample(cb, cr, variant, f):
    """
                                       Function to up sample.
                                       :param cb: CB channel.
                                       :param cr: CR channel.
                                       :param variant: downsampling variant.
                                       :param f: downsampling factor.
                                       :return: the upsampled channels.
    """
    if variant == 1:
        cb_up_sampled = np.repeat(cb, f, axis=1)
        cr_up_sampled = np.repeat(cr, f, axis=1)
    elif variant == 2:
        cb_up_sampled = np.repeat(cb, f, axis=1)
        cr_up_sampled = np.repeat(cr, f, axis=1)
        cb_up_sampled = np.repeat(cb_up_sampled, f, axis=0)
        cr_up_sampled = np.repeat(cr_up_sampled, f, axis=0)
    else:
        return cb, cr

    return cb_up_sampled, cr_up_sampled


def encoder(image_data, show_plots=False):
    """
                                       Enconder function.
                                       :param image_data: the image to encode.
                                       :param show_plots: flag that enables plotting.
                                       :return: the encoded image.
    """
    image_name = image_data[0]
    image_matrix = image_data[1]

    Y_CB_CR_MATRIX = np.array([[0.299, 0.587, 0.114], [-0.168736, -0.331264, 0.5], [0.5, -0.418688, -0.081312]])
    GREY_CMAP_LIST = [(0, 0, 0), (1, 1, 1)]
    RED_CMAP_LIST = [(0, 0, 0), (1, 0, 0)]
    GREEN_CMAP_LIST = [(0, 0, 0), (0, 1, 0)]
    BLUE_CMAP_LIST = [(0, 0, 0), (0, 0, 1)]

    grey_cmap = generate_linear_colormap(GREY_CMAP_LIST)
    red_cmap = generate_linear_colormap(RED_CMAP_LIST)
    green_cmap = generate_linear_colormap(GREEN_CMAP_LIST)
    blue_cmap = generate_linear_colormap(BLUE_CMAP_LIST)
    n_rows = image_matrix.shape[0]
    n_cols = image_matrix.shape[1]

    padded_image = apply_padding(image_matrix, 32, 32)
    if show_plots:
        show_images(padded_image)

    r, g, b = separate_rgb(padded_image, show_plots)
    if show_plots:
        plot_image_colormap(r, red_cmap)
        plot_image_colormap(g, green_cmap)
        plot_image_colormap(b, blue_cmap)

    y_cb_cr_image = rgb_to_y_cb_cr(padded_image, Y_CB_CR_MATRIX, show_plots)

    y = y_cb_cr_image[:, :, 0]
    cb = y_cb_cr_image[:, :, 1]
    cr = y_cb_cr_image[:, :, 2]

    if show_plots:
        plot_image_colormap(y, grey_cmap)
        plot_image_colormap(cb, grey_cmap)
        plot_image_colormap(cr, grey_cmap)

    cb, cr = down_sample(cb, cr, 1, 2)

    return (y, cb, cr), n_rows, n_cols


def decoder(encoded_image_data):
    """
                                           Decode function.
                                           :param encoded_image_data: the image to decode.
                                           :return: the decoded image.
    """
    encoded_image_name = encoded_image_data[0]
    encoded_image = encoded_image_data[1]
    original_rows = encoded_image_data[2]
    original_cols = encoded_image_data[3]

    Y_CB_CR_MATRIX = np.array([[0.299, 0.587, 0.114], [-0.168736, -0.331264, 0.5], [0.5, -0.418688, -0.081312]])
    Y_CB_CR_MATRIX_INVERSE = np.linalg.inv(Y_CB_CR_MATRIX)

    y = encoded_image[0]
    cb = encoded_image[1]
    cr = encoded_image[2]
    cb_up_sampled, cr_up_sampled = up_sample(cb, cr, 1, 2)
    joined_channels_img = join_channels(y, cb_up_sampled, cr_up_sampled)
    rgb_image = y_cb_cr_to_rgb(joined_channels_img, Y_CB_CR_MATRIX_INVERSE)
    unpadded_image = reverse_padding(rgb_image, original_rows, original_cols)
    show_images(unpadded_image)

    decoded_image = unpadded_image

    return decoded_image


def image_equals(original_image, decoded_image):
    """
                                           Verifies if the images are equal.
                                           :param original_image: original image.
                                           :param decoded_image: decoded image.
                                           :return: if the image is equal or no.
    """
    return np.allclose(original_image, decoded_image)


def main():
    """
    Main function
    """
    CWD = os.getcwd()
    ORIGINAL_IMAGE_DIRECTORY = CWD + '/original_img/'
    ORIGINAL_IMAGE_EXTENSION = '.bmp'
    COMPRESSED_IMAGE_DIRECTORY = CWD + '\\jpeg_compressed_img'
    JPEG_QUALITY_RATES = [25, 50, 75]

    original_images = read_images(ORIGINAL_IMAGE_DIRECTORY, ORIGINAL_IMAGE_EXTENSION)
    #show_images(original_images)
    #jpeg_compress_images(ORIGINAL_IMAGE_DIRECTORY, ORIGINAL_IMAGE_EXTENSION, COMPRESSED_IMAGE_DIRECTORY, JPEG_QUALITY_RATES)

    encoded_images = dict()

    for image_name in original_images.keys():
        result = encoder((image_name, original_images[image_name]), False)
        encoded_images[image_name] = (result[0], result[1], result[2])

    decoded_images = dict()
    for encoded_image_name in encoded_images.keys():
        data = encoded_images[encoded_image_name]
        result = decoder((encoded_image_name, data[0], data[1], data[2]))
        decoded_images[encoded_image_name] = result

        if image_equals(original_images[encoded_image_name], result):
            print("No diff")
        else:
            print("Diff")


if __name__ == '__main__':
    main()