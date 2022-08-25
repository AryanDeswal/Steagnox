from django.shortcuts import render
from .forms import ImageForm
from importlib.metadata import metadata
import cv2
import os

# ------------------------------------------------------
# Functions


def clean_dir(dir_path):
    res = img_names(dir_path)

    for i in range(0, len(res)):
        os.remove(dir_path + res[i])


def img_names(dir_path):
    res = []
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(path)
    return res


def create_data_file(data):
    path = 'media\data.txt'
    file_handle = open(path, 'w')
    file_handle.write(data)
    file_handle.close
    return path


def spiltbyte(by):  # 011 000 01
    first_three_bits = by >> 5
    mid_three_bits = (by >> 2) & 7
    last_two_bits = by & 3
    return first_three_bits, mid_three_bits, last_two_bits


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


def embed(vessel_image, target_image, src_file, passcode):
    # load the vessel_image into memory
    mem_image = cv2.imread(vessel_image)
    # print(type(mem_image))
    # print(mem_image.shape)

    # form the metadata
    header = getMetaData(src_file)
    if header is None:
        print(header)
        print('Embedding not possible: File too big or not found')
        return None

    # know the total embedding size
    total_embedding_size = os.path.getsize(src_file) + len(header)

    # check: is embedding possible
    embedding_capacity = mem_image.shape[0] * mem_image.shape[1]

    if total_embedding_size > embedding_capacity:
        print('Embedding not possible: File too big')
        return None

    # embed...

    # encryt the header
    header = crypt(header, passcode)

    # fetch the data to embed
    file_handle = open(src_file, 'rb')
    buffer = file_handle.read()
    file_handle.close()

    indx = 0
    width = mem_image.shape[1]
    # embedding loop
    while indx < total_embedding_size:
        r = indx // width
        c = indx % width
        if indx < 30:  # len(header)
            bits = spiltbyte(ord(header[indx]))
        else:
            bits = spiltbyte(buffer[indx - 30])

        # Free 2,3,3 bits of the pixel
        mem_image[r, c, 0] &= 252  # blue band
        mem_image[r, c, 1] &= 248  # green band
        mem_image[r, c, 2] &= 248  # red band

        # Merge the bits into the bands
        mem_image[r, c, 0] |= bits[2]  # blue band
        mem_image[r, c, 1] |= bits[1]  # green band
        mem_image[r, c, 2] |= bits[0]  # red band

        # next val to embed
        indx += 1

    # save back the image
    cv2.imwrite(target_image, mem_image)

# ------------------------------------------------------


def embed_image(request):
    """Process images uploaded by users"""
    dir_path = r'.//media//images//'
    clean_dir(dir_path)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Encrypting raw image
            raw_img_path = dir_path+img_names(dir_path)[0]
            enc_img_path = "encrypted_img.png"       #png is necessary for decryption to work
            data = form.cleaned_data['Data']
            data_file_path = create_data_file(data)
            password = form.cleaned_data['Password']

            embed(raw_img_path, enc_img_path, data_file_path, password)

            # Removing user information from server
            os.remove(data_file_path)
            clean_dir(dir_path)
            form = ImageForm()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'embed_image.html', {'img_obj': img_obj, 'data': data, 'form': form})
    else:
        form = ImageForm()
        
    return render(request, 'embed_image.html', {'form': form})








