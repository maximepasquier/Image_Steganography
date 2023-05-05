
'''
from PIL import Image
import os


def hide_data(image_with_hidden_data, data_to_hide):
    lines = image_with_hidden_data.size[0]
    columns = image_with_hidden_data.size[1]
    pixel_list = image_with_hidden_data.getdata()
    data_to_hide_chars = [char for char in data_to_hide]
    pixel_iterator = 0
    for iterator in range(len(data_to_hide_chars)):
        value = ord(data_to_hide_chars[iterator])
        
        print(pixel_list[pixel_iterator][0])

        bit = (value & 0b10000000) >> 7
        if bit == 0:
            image_with_hidden_data.putpixel((pixel_iterator,0), pixel_list[pixel_iterator,0] & 0b11111110)
        else:
            pixel_list[pixel_iterator][0] | 0b00000001

        bit = (value & 0b01000000) >> 6
        if bit == 0:
            pixel_list[pixel_iterator][1] & 0b11111110
        else:
            pixel_list[pixel_iterator][1] | 0b00000001

        bit = (value & 0b00100000) >> 5
        if bit == 0:
            pixel_list[pixel_iterator][2] & 0b11111110
        else:
            pixel_list[pixel_iterator][2] | 0b00000001

        pixel_iterator += 1

        bit = (value & 0b00010000) >> 4
        if bit == 0:
            pixel_list[pixel_iterator][0] & 0b11111110
        else:
            pixel_list[pixel_iterator][0] | 0b00000001

        bit = (value & 0b00001000) >> 3
        if bit == 0:
            pixel_list[pixel_iterator][1] & 0b11111110
        else:
            pixel_list[pixel_iterator][1] | 0b00000001

        bit = (value & 0b00000100) >> 2
        if bit == 0:
            pixel_list[pixel_iterator][2] & 0b11111110
        else:
            pixel_list[pixel_iterator][2] | 0b00000001

        pixel_iterator += 1

        bit = (value & 0b00000010) >> 1
        if bit == 0:
            pixel_list[pixel_iterator][0] & 0b11111110
        else:
            pixel_list[pixel_iterator][0] | 0b00000001

        bit = (value & 0b00000001) >> 0
        if bit == 0:
            pixel_list[pixel_iterator][1] & 0b11111110
        else:
            pixel_list[pixel_iterator][1] | 0b00000001

        pixel_iterator += 1


def encode():
    image_path = (
        os.getcwd()
        + "/Images/"
        + input("Entrez le nom de l'image du dossier Images avec son extension : ")
    )
    image = Image.open(image_path, "r")
    data_to_hide = input("Entrez le texte à cacher dans l'image : ")
    if len(data_to_hide) == 0:
        raise ValueError("Texte vide !")

    image_with_hidden_data = image.copy()
    hide_data(image_with_hidden_data, data_to_hide)
    image_with_hidden_data_name = (
        os.getcwd()
        + "/Images/"
        + input("Entrez le nom de la nouvelle image avec son extension : ")
    )
    image_with_hidden_data.save(
        image_with_hidden_data_name,
        str(image_with_hidden_data_name.split(".")[1].upper()),
    )


def recover_data(image, data):
    lines = image.size[0]
    columns = image.size[1]
    pixel_list = image.getdata()
    pixel_iterator = 0
    for i in range(10):
        character = 0

        value = pixel_list[pixel_iterator][0] & 0b00000001
        character = character | (value << 7)

        value = pixel_list[pixel_iterator][1] & 0b00000001
        character = character | (value << 6)

        value = pixel_list[pixel_iterator][2] & 0b00000001
        character = character | (value << 5)

        pixel_iterator += 1

        value = pixel_list[pixel_iterator][0] & 0b00000001
        character = character | (value << 4)

        value = pixel_list[pixel_iterator][1] & 0b00000001
        character = character | (value << 3)

        value = pixel_list[pixel_iterator][2] & 0b00000001
        character = character | (value << 2)

        pixel_iterator += 1

        value = pixel_list[pixel_iterator][0] & 0b00000001
        character = character | (value << 1)

        value = pixel_list[pixel_iterator][1] & 0b00000001
        character = character | (value << 0)

        print(character)

        pixel_iterator += 1


def decode():
    img = (
        os.getcwd()
        + "/Images/"
        + input("Entrez le nom de l'image du dossier Images avec son extension : ")
    )
    image = Image.open(img, "r")

    data = ""

    recover_data(image, data)


def main():
    user_input = int(
        input(
            "Least Significant Bit (LSB) \n"
            "Entrez 1 pour encoder. \n"
            "Entrez 2 pour décoder. \n"
        )
    )
    if user_input == 1:
        encode()
    elif user_input == 2:
        print("Le texte décodé est : " + decode())
    else:
        raise Exception("Input invalide !")


if __name__ == "__main__":
    main()
'''

import numpy as np
from PIL import Image
import os

def hide_data(img,data):
    binary_data = ''.join(format(ord(i), '08b') for i in data)
    str_len = len(binary_data)
    iterator = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3): # for 3 channels
                if binary_data[iterator] == '0':
                    img[i,j,k] = img[i,j,k] & 0b11111110
                else:
                    img[i,j,k] = img[i,j,k] | 0b00000001
                iterator += 1
                if iterator == str_len:
                    return
    

def encode():
    #* Open image
    image_path = (
        os.getcwd()
        + "/Images/"
        + input("Entrez le nom de l'image du dossier Images avec son extension : ")
    )
    image_PIL = Image.open(image_path, "r")
    image = np.asarray(image_PIL)
    
    #* Get text to hide in cover image
    data_to_hide = input("Entrez le texte à cacher dans l'image : ")
    if len(data_to_hide) == 0:
        raise ValueError("Texte vide !")
    
    #* Hide text data into cover image
    image_with_hidden_data = image.copy()
    hide_data(image_with_hidden_data, data_to_hide)
    
    #* Numpy array back to PIL Image
    image_with_hidden_data_PIL = Image.fromarray(image_with_hidden_data)
    
    #* Save stego image
    image_with_hidden_data_name = (
        os.getcwd()
        + "/Images/"
        + input("Entrez le nom de la nouvelle image avec son extension : ")
    )
    image_with_hidden_data_PIL.save(
        image_with_hidden_data_name,
        str(image_with_hidden_data_name.split(".")[1].upper()),
    )
    
def BinaryToDecimal(binary):
     
    # Using int function to convert to
    # string  
    string = int(binary, 2)
     
    return string
    
def recover_data(img,data):
    binary_data = ''
    str_data = ''
    iterator = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3): # for 3 channels
                if(img[i,j,k] & 0b00000001 == 1): # detected in LSB
                    binary_data += '1'
                else:
                    binary_data += '0'
                iterator += 1
                if(iterator == 2**7):
                    print(binary_data)
                    for i in range(0, len(binary_data), 8):
                        temp_data = binary_data[i:i + 8]
                        print(temp_data)
                        decimal_data = BinaryToDecimal(temp_data)
                        str_data = str_data + chr(decimal_data)
                    return str_data
    

def decode():
    img = (
        os.getcwd()
        + "/Images/"
        + input("Entrez le nom de l'image du dossier Images avec son extension : ")
    )
    image_PIL = Image.open(img, "r")
    image = np.asarray(image_PIL)

    data = ""

    return recover_data(image, data)


def main():
    user_input = int(
        input(
            "Least Significant Bit (LSB) \n"
            "Entrez 1 pour encoder. \n"
            "Entrez 2 pour décoder. \n"
        )
    )
    if user_input == 1:
        encode()
    elif user_input == 2:
        print("Le texte décodé est : " + decode())
    else:
        raise Exception("Input invalide !")

if __name__ == "__main__":
    main()






































