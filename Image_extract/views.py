from fileinput import filename
from django.shortcuts import render
from .forms import ExtImageForm
from importlib.metadata import metadata
import cv2
import os

# Create your views here.

def clean_dir(dir_path):
    res = file_names(dir_path)

    for i in range(0, len(res)):
        if (res[i] != 'test.txt'):
            os.remove(dir_path + res[i])


def file_names(dir_path):
    res = []
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(path)
    return res


def spiltbyte(by):  # 011 000 01
    first_three_bits = by >> 5
    mid_three_bits = (by >> 2) & 7
    last_two_bits = by & 3
    return first_three_bits, mid_three_bits, last_two_bits


def merge_bits(bits):  # [3,0, 1] => 97
    return (((bits[0] << 3) | bits[1]) << 2) | bits[2]


def getMetaData(file_to_embed):
    if os.path.exists(file_to_embed):  # check that the file exists
        # know the file size in bytes
        file_size = os.path.getsize(file_to_embed)
        if file_size > 9999999999:
            return None  # More than the max support
        # Pad * at the RHS to make it of length : 10
        file_size = str(file_size).ljust(10, '*')
        file_name = os.path.basename(file_to_embed)  # exclude the parent path
        # Pad * at the RHS to make it of len 20, doesnt pad is len is already > 20
        file_name = file_name.ljust(20, '*')
        # reduce the len to 20 by slicing
        file_name = file_name[len(file_name)-20:]
        return file_size+file_name

    else:
        return None


def crypt(src, key):
    crypted = ''
    i = 0
    l = len(key)
    for s in src:
        crypted += chr(ord(s) ^ ord(key[i]))
        i = (i+1) % l
    return crypted

def read(file_name):
    file_handle = open(file_name, 'r')
    text=file_handle.read()
    file_handle.close()
    return text

def extract_data(emb_image, passcode):
    #load the image in memory
    mem_img = cv2.imread(emb_image)
    qty_to_extract = 30 #of header

    width = mem_img.shape[1]
    indx =0
    buffer = ''
    temp = []
    while indx < qty_to_extract:
        r = indx //width
        c = indx % width
        temp.clear()
        for i in range(3): #0,1,2
            temp.append(mem_img[r,c,2-i] & 2 ** (3 - (i+1) // 3) - 1)

        buffer += chr(merge_bits(temp))
        indx+=1


    buffer = crypt(buffer, passcode)

    try:
        qty_to_extract = int(buffer[:10].strip('*')) +30
    except:
        return "Wrong Answer"
    file_name = buffer[10:].strip('*')

    indx =30
    temp = []

    
    file_handle = open(file_name, 'wb')
    


    while indx < qty_to_extract:
        r = indx //width
        c = indx % width
        temp.clear()
        for i in range(3): #0,1,2
            temp.append(mem_img[r,c,2-i] & 2 ** (3 - (i+1) // 3) - 1)

        x = int(merge_bits(temp))

        file_handle.write(int.to_bytes(x,1,"big"))
        indx+=1
    file_handle.close()

    return read(file_name)




def extract_image(request):
    dir_path = r'.//media//images//'
    clean_dir(dir_path)
    form2 = ExtImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form2.is_valid():
            form2.save()
            
            #--------------------------------------------
            enc_img_path = ""
            if (file_names(dir_path)[0] == 'test.txt'):
                enc_img_path = dir_path+file_names(dir_path)[1]
            else:
                enc_img_path = dir_path+file_names(dir_path)[0]   #png is necessary for decryption to work
            password = form2.cleaned_data['Password']

            text=extract_data(enc_img_path,password)
            # Removing user information from server
            os.remove('data.txt')
            clean_dir(dir_path)
            
            #--------------------------------------------
            img_obj = form2.instance
            return render(request, 'extract_image.html', { 'img_obj': img_obj,'password':password})

    return render(request, 'extract_image.html', {'form2': form2})