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
