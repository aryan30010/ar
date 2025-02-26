import cv2
import os

image = cv2.imread("mypic.jpg")

secret_message = input("Enter the secret message:")
passcode = input("Enter a passcode:")

char_to_num = {}
num_to_char = {}

for i in range(255):
    char_to_num[chr(i)] = i
    num_to_char[i] = chr(i)

binary_message = ''.join(format(char_to_num[char], '08b') for char in secret_message)

row = 0
col = 0
channel = 0
bit_index = 0

for bit in range(len(binary_message)):
    pixel_value = image[row, col, channel]
    image[row, col, channel] = (pixel_value & 0xFE) | int(binary_message[bit_index])
    bit_index += 1
    row += 1
    if row >= image.shape[0]:
        row = 0
        col += 1
    channel = (channel + 1) % 3

cv2.imwrite("encoded_image.jpg", image)
os.system("start encoded_image.jpg")

decrypted_message = ""
row = 0
col = 0
channel = 0

input_passcode = input("Enter the passcode for decryption:")
if passcode == input_passcode:
    extracted_binary = ""
    for bit in range(len(binary_message)):
        pixel_value = image[row, col, channel]
        extracted_binary += str(pixel_value & 1)
        row += 1
        if row >= image.shape[0]:
            row = 0
            col += 1
        channel = (channel + 1) % 3
    
    for i in range(0, len(extracted_binary), 8):
        byte = extracted_binary[i:i+8]
        decrypted_message += num_to_char[int(byte, 2)]
    
    print("Decrypted message:", decrypted_message)
else:
    print("Incorrect passcode! Access denied.")
