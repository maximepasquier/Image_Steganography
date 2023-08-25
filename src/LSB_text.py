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
    # Open image
    image_path = (
        os.getcwd()
        + "/Images/"
        + input("Entrez le nom de l'image du dossier Images avec son extension : ")
    )
    image_PIL = Image.open(image_path, "r")
    image = np.asarray(image_PIL)
    
    # Get text to hide in cover image
    data_to_hide = input("Entrez le texte à cacher dans l'image : ")
    if len(data_to_hide) == 0:
        raise ValueError("Texte vide !")
    
    # Hide text data into cover image
    image_with_hidden_data = image.copy()
    hide_data(image_with_hidden_data, data_to_hide)
    
    # Numpy array back to PIL Image
    image_with_hidden_data_PIL = Image.fromarray(image_with_hidden_data)
    
    # Save stego image
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
                if(iterator == 2**9):
                    for i in range(0, len(binary_data), 8):
                        temp_data = binary_data[i:i + 8]
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
