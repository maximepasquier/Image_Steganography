import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct
from ctypes import *
import os


def hide_secret(cover, secret, stego):
    if cover.shape != secret.shape:
        raise ValueError("Images of different size !")
    for i in range(cover.shape[0]):
        for j in range(cover.shape[1]):
            for k in range(cover.shape[2]):
                cover_value = cast(
                    pointer(c_float(cover[i, j, k])), POINTER(c_int64)
                ).contents.value
                # print(cover[i,j,k])
                secret_value = secret[i, j, k]
                cover_value = (
                    cover_value
                    & 0b1111111111111111111111111111111111111111111111111111111100000000
                )
                # secret_value = secret_value >> 4
                secret_value = cover_value | secret_value
                stego[i, j, k] = cast(
                    pointer(c_int64(secret_value)), POINTER(c_float)
                ).contents.value
    return stego


def recover_image(stego):
    stego_dct = dct(stego, norm="ortho")
    reconstruct = stego.copy()
    for i in range(stego.shape[0]):
        for j in range(stego.shape[1]):
            for k in range(stego.shape[2]):
                stego_value = cast(
                    pointer(c_float(stego_dct[i, j, k])), POINTER(c_int64)
                ).contents.value
                recon_value = stego_value & 0b11111111
                reconstruct[i, j, k] = recon_value
    return reconstruct.astype("uint8")


# * Open images
cover_image_path = os.getcwd() + "/Images/cover.png"
secret_image_path = os.getcwd() + "/Images/secret.png"
cover_image_PIL = Image.open(cover_image_path, "r")
cover_image = np.asarray(cover_image_PIL)
secret_image_PIL = Image.open(secret_image_path, "r")
secret_image = np.asarray(secret_image_PIL)

cover_image_dct = dct(cover_image, norm="ortho")

# * Encrypte
stego_image_dct = cover_image_dct.copy()
stego_image_dct = hide_secret(cover_image_dct, secret_image, stego_image_dct)
stego_image = idct(stego_image_dct, norm="ortho").astype("uint8")

stego_image_path = os.getcwd() + "/Images/stego_DCT.png"
stego_image_PIL = Image.fromarray(stego_image, "RGB")
stego_image_PIL.save(stego_image_path)


# * Decrypte
reconstructed_image = recover_image(stego_image)

# s = dct(stego_image, norm="ortho")
# d = idct(s, norm="ortho").astype("uint8")

# print(reconstructed_image)

reconstructed_image_path = os.getcwd() + "/Images/reconstructed_DCT.png"
reconstructed_image_PIL = Image.fromarray(reconstructed_image, "RGB")
reconstructed_image_PIL.save(reconstructed_image_path)
