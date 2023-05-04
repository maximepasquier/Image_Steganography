from PIL import Image
import os


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

    # print(image.size)

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


def hide_data(image_with_hidden_data, data_to_hide):
    w = image_with_hidden_data.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(image_with_hidden_data.getdata(), data_to_hide):
        # Putting modified pixels in the new image
        image_with_hidden_data.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1


def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        # Extracting 3 pixels at a time
        pix = [
            value
            for value in imdata.__next__()[:3]
            + imdata.__next__()[:3]
            + imdata.__next__()[:3]
        ]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if datalist[i][j] == "0" and pix[j] % 2 != 0:
                pix[j] -= 1

            elif datalist[i][j] == "1" and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if i == lendata - 1:
            if pix[-1] % 2 == 0:
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def genData(data):
    # list of binary codes
    # of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), "08b"))
    return newd


def decode():
    img = (
        os.getcwd()
        + "/Images/"
        + input("Entrez le nom de l'image du dossier Images avec son extension : ")
    )
    image = Image.open(img, "r")

    data = ""
    imgdata = iter(image.getdata())

    while True:
        pixels = [
            value
            for value in imgdata.__next__()[:3]
            + imgdata.__next__()[:3]
            + imgdata.__next__()[:3]
        ]

        # string of binary data
        binstr = ""

        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += "0"
            else:
                binstr += "1"
        data += chr(int(binstr, 2))
        print(pixels[-1])
        if pixels[-1] % 2 != 0:
            return data


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
