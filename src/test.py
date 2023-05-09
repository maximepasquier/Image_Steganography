import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct
from ctypes import *
import os

#* Open images
cover_image_path = (
    os.getcwd()
    + "/Images/cover.png"
)
secret_image_path = (
    os.getcwd()
    + "/Images/secret.png"
)
cover_image_PIL = Image.open(cover_image_path, "r")
cover_image = np.asarray(cover_image_PIL)
secret_image_PIL = Image.open(secret_image_path, "r")
secret_image = np.asarray(secret_image_PIL)

cover_image_dct = dct(cover_image,norm = 'ortho')
cover_image_idct = idct(cover_image_dct,norm = 'ortho')
cover_image_idct = cover_image_idct.astype('uint8')

image_path = (
    os.getcwd()
    + "/Images/img_test.png"
)
stego_image_PIL = Image.fromarray(cover_image_idct,"RGB")
stego_image_PIL.save(image_path)

print(cover_image.dtype)

print("next")

print(cover_image_idct.dtype)











