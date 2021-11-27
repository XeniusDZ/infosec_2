import numpy
from numpy import asarray
from PIL import Image
import os
import math
import cv2
import random

def PSNR(original, encrypted):
    original = cv2.imread(original)
    contrast = cv2.imread(encrypted, 1)
    mse = numpy.mean((original - contrast) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

def choose():
    encode = int(input("1 ===> изображение\n2 ===> текст или битовую последовательность\n"))
    if encode == 1:
        small_pic = "images.jpeg"
        big_pic = int(input("Выберите изображение 0/1: \n"))
        big_pics = ["test.jpg","test2.jpeg"]
        if big_pic == 0 or big_pic ==1:
            print("Подождите пару секунд")
            hide2(small_pic,big_pics[big_pic])
            find2(small_pic)

        else:
            print("Неверное значение")
    elif encode == 2:
        choice = int(input("Выберите изображение 0/1/2: \n"))

        changes = int(input("Выберите количество закодированных битов: 1/2/4/8\n"))

        message = input("Выбирайте текст\n")

        pictures = ["images.jpeg","test.jpg","test2.jpeg"]
        if changes == 1 or changes == 2 or changes == 4 or changes == 8:
            print(hide(message, pictures[choice], changes))
            print(find("SERCRET.png", changes))
        else:
            print("Неверное значение")
    else:
        print("Неверное значение")
def hide(msg, image_name, bits):
    image = Image.open(image_name)
    data = asarray(image).copy()


    image_bytes = os.stat(image_name).st_size
    possible_encoded_bits = image_bytes * 8

    if image_bytes * bits/8 < len(msg) * 8:
        print("текст слишком длинный")

    final_message = ""
    for letter in msg:
        position_ascii = ord(letter)
        binary = bin(position_ascii)[2:]
        while len(binary) < 8:
            binary = "0" + binary
        final_message += binary
    print("текст в 2-СС :", final_message)


    length = len(final_message)
    length_binary = bin(length,)[2:]
    while len(length_binary) < 16:
        length_binary = "0" + length_binary
    print("Размер для встраивание: :", length_binary)
    result_message = length_binary + final_message


    tour = 0
    y = 0
    for line in data:
        x = 0
        for column in line:
            rgb = 0
            for color in column:
                value = data[y][x][rgb]
                binary = bin(value)[2:]
                binary_list = list(binary)
                del binary_list[-bits:]
                binary_list.append(result_message[tour:tour+bits])
                decimal = int("".join(binary_list), 2)

                data[y][x][rgb] = decimal
                tour += bits
                rgb += 1
                if tour >= len(result_message):
                    break
            x += 1
            if tour >= len(result_message):
                break
        y += 1
        if tour >= len(result_message):

            break
    imagefinal = Image.fromarray(data)
    imagefinal.save("SERCRET.png")
    print("PSNR", PSNR(image_name,"SERCRET.png"))
    ber = len(final_message) / possible_encoded_bits
    print("BER", ber)



def find(image_name, bits):
    image = Image.open(image_name)
    data = asarray(image).copy()
    length = ""
    message = ""
    new_length = 1553544545
    tour = 0
    y = 0
    for line in data:
        x = 0
        for column in line:
            rgb = 0
            for color in column:
                value = data[y][x][rgb]
                binary = bin(value)[2:]
                while len(binary) < 8:
                    binary = "0" + binary
                last = binary[-bits:]
                if tour < 16:
                    length += last
                if tour == 16:
                    new_length = int(length,2)
                if tour - 16 < new_length:
                    message += last
                if tour - 16 > new_length:
                    break
                tour += bits
                rgb += 1
            if tour - 16 > new_length - 1:
                break
            x += 1
        y += 1
        if tour - 16 > new_length - 1:
            break

    message = message[16:]
    octet = []
    for i in range(len(message)//8):
        octet.append(message[i*8:(i+1)*8])
    final_message = ""
    for oct in octet:

        index = int(oct,2)

        letter = chr(index)

        final_message += letter
    print("ваш секретный текст: ", final_message)

def hide2(small_pic,big_pic):
    img1 = cv2.imread(big_pic)
    img2 = cv2.imread(small_pic)

    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            for l in range(3):

                v1 = format(img1[i][j][l], '08b')
                v2 = format(img2[i][j][l], '08b')

                v3 = v1[:4] + v2[:4]

                img1[i][j][l] = int(v3, 2)

    cv2.imwrite('pic3in2.png', img1)

    print("PSNR", PSNR(big_pic,"pic3in2.png"))





def find2(small_pic):

    img = cv2.imread('pic3in2.png')
    width = img.shape[0]
    height = img.shape[1]

    img2 = cv2.imread(small_pic)
    width2 = img2.shape[0]
    height2 = img2.shape[1]


    img1 = numpy.zeros((width, height, 3), numpy.uint8)
    img2 = numpy.zeros((width, height, 3), numpy.uint8)

    for i in range(width):
        for j in range(height):
            for l in range(3):
                v1 = format(img[i][j][l], '08b')
                v2 = v1[:4] + chr(random.randint(0, 1) + 48) * 4
                v3 = v1[4:] + chr(random.randint(0, 1) + 48) * 4


                img1[i][j][l] = int(v2, 2)
                if i >= width2 or j >= height2:
                    pass
                else:
                    img2[i][j][l] = int(v3, 2)



    cv2.imwrite('pic2_re.png', img1)
    cv2.imwrite('pic3_re.png', img2)

    img = cv2.imread("pic3_re.png")
    crop_img = img[0:width2, 0:height2]
    cv2.imwrite("pic3_re.png", crop_img)



if __name__ == '__main__':
    while True:
        choose()