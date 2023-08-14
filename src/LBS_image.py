import numpy as np
from PIL import Image
import os

def hide_secret(cover,secret,stego):
    if(cover.shape != secret.shape):
        raise ValueError("Images of different size !")
    for i in range(cover.shape[0]):
        for j in range(cover.shape[1]):
            for k in range(cover.shape[2]):
                cover_value = cover[i,j,k]
                secret_value = secret[i,j,k]
                cover_value = cover_value & 0b11000000
                secret_value = secret_value >> 2
                stego[i,j,k] = cover_value | secret_value
                
def recover_image(reconstruct,stego):
    for i in range(stego.shape[0]):
        for j in range(stego.shape[1]):
            for k in range(stego.shape[2]):
                reconstruct[i,j,k] = (stego[i,j,k] & 0b00111111) << 2
                

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

#print(secret_image)

'''
img = Image.fromarray(secret_image[:,:,0:3], "RGB")
image_filename = "i.png"
img.save(image_filename)
'''

#* Encrypte
stego_image = cover_image.copy()
hide_secret(cover_image,secret_image,stego_image)

stego_image_path = (
    os.getcwd()
    + "/Images/stego_LSB_6.png"
)
stego_image_PIL = Image.fromarray(stego_image,"RGB")
stego_image_PIL.save(stego_image_path)


#* Decrypte
reconstructed_image = stego_image.copy()
recover_image(reconstructed_image,stego_image)

reconstructed_image_path = (
    os.getcwd()
    + "/Images/reconstructed_LSB_6.png"
)
reconstructed_image_PIL = Image.fromarray(reconstructed_image,"RGB")
reconstructed_image_PIL.save(reconstructed_image_path)













