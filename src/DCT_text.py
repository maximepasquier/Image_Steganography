import numpy as np
import skimage
from PIL import Image
from scipy.fftpack import fft, dct, idct, ifft
import os
import cv2
import scipy.signal
from ctypes import *
import random
import math
import matplotlib.pyplot as plt

def BinaryToDecimal(binary):
    string = int(binary, 2)
    return string

def hide_data(img,data):
    binary_data = ''.join(format(ord(i), '08b') for i in data)
    str_len = len(binary_data)
    iterator = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3): # for 3 channels
                bits = cast(pointer(c_float(img[i,j,k])), POINTER(c_int64)).contents.value
                if binary_data[iterator] == '0':
                    bits = bits & 0b1111111111111111111111111111111111111111111111111111111111111110
                else:
                    bits = bits | 0b0000000000000000000000000000000000000000000000000000000000000001
                img[i,j,k] = cast(pointer(c_int64(bits)), POINTER(c_float)).contents.value
                iterator += 1
                if iterator == str_len:
                    return
                
def recover_data(img,data):
    binary_data = ''
    str_data = ''
    iterator = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3): # for 3 channels
                bits = cast(pointer(c_float(img[i,j,k])), POINTER(c_int64)).contents.value
                if(bits & 1 == 1): # detected in LSB
                    binary_data += '1'
                else:
                    binary_data += '0'
                iterator += 1
                if(iterator == 2**9):
                    for i in range(0, len(binary_data), 8):
                        temp_data = binary_data[i:i + 8]
                        decimal_data = BinaryToDecimal(temp_data)
                        str_data = str_data + chr(decimal_data)
                    return str_data

#* Open image
image_path = (
    os.getcwd()
    + "/Images/img.png"
)
image_PIL = Image.open(image_path, "r")
image = np.asarray(image_PIL)

image_dct = dct(image,norm = 'ortho')
image_fft = fft(image)


image_idct = idct(image_dct,norm = 'ortho').astype("int")
image_ifft = ifft(image_fft).astype("int")

#* Encrypte
image_with_hidden_data_dct = image_dct.copy()
hide_data(image_with_hidden_data_dct,"Ceci est du texte caché dans les coefficients du cosinus.")
image_with_hidden_data_idct = idct(image_with_hidden_data_dct,norm = 'ortho')

#* Decrypte
data = ''
data = recover_data(dct(image_with_hidden_data_idct,norm = 'ortho'),data)
print("Decrypted data is : " + data)

#print(np.linalg.norm(image_with_hidden_data_dct))norm = 'ortho'
#print(np.linalg.norm(image_dct))


'''
plt.figure()
plt.imshow(image_with_hidden_data_idct)
#plt.imshow(image_ifft)
plt.show()
'''
