from PIL import Image
import os


def encode():
    pass


def decode():
    pass


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
