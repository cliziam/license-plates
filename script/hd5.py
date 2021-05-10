import sys
import h5py
import numpy as np
import os
from PIL import Image
import argparse
import re
import string
import matplotlib.pyplot as plt

# in writer.py
# DATA_IMAGES = "images"
# DATA_LENGTH_LABELS = "length_labels"
# DATA_CHAR_LABELS = "char_labels"
# DATA_LICENSE_NUMBERS = "license_numbers"
# DATA_SCALING_TARGET_WIDTHS = "scaling_target_widths"
# DATA_NOISE_SNRS_DB = "noise_SNRs_db"


# --> REQUIRED_DATA_SETS = [DATA_IMAGES,
#                           DATA_LENGTH_LABELS,
#                           DATA_CHAR_LABELS,
#                           DATA_LICENSE_NUMBERS,
#                           DATA_SCALING_TARGET_WIDTHS,
#                           DATA_NOISE_SNRS_DB]

def convert_dir(input_dir, output_file_name, dimension1, dimension2):
    h5f = h5py.File(output_file_name + ".hdf5", 'w')
    arr = os.listdir(input_dir)

    listchar = list()
    listlen = list()
    listres = list()
    listnoise=list()
    listln=list()

    for i in arr:

        # Extract license number, resolution, and noise level from filename
        match = re.search("license_number_([A-Z0-9]+)_resolution_([0-9]+)_noise_SNR_db_([-+]?[0-9]*\.?[0-9]+)", i)
        if match is not None:
            license_number = match.group(1)
            resolution = int(match.group(2))
            noise_SNR_db = float(match.group(3))

            # Convert license number extracted from filename to one-hot encoded label vector
            char_labels = np.zeros((7, 37))

            all_chars = string.ascii_uppercase + string.digits + "_"
            # One-hot encode characters
            for i in range(len(license_number)):
                char_labels[i, all_chars.index(license_number[i])] = 1


            # For the remaining positions set the `no char` label
            for i in range(len(license_number), 7):
                char_labels[i, 36] = 1

            listchar.append(char_labels)
            listlen.append(len(char_labels))
            listnoise.append(noise_SNR_db)
            listres.append(resolution)
            listln.append(license_number)


        #   print("noise", noise_SNR_db)
        #   print("plate "+license_number)
        #   print("res", resolution)
        #   print("char_labels ", char_labels)


    #print(listchar)
    #print(listlen)
    #print(listres)
    #print(listnoise)

    result_arr = np.empty([len(arr), dimension1, dimension2, 3], dtype='int16')

    for i in range(0, len(arr)):
        f_path = input_dir + '/' + arr[i]
        image = Image.open(f_path)
        image_arr = np.array(image)
        result_arr[i] = image_arr

    h5f.create_dataset('images', data=result_arr)
    h5f.create_dataset('length_labels', data=listlen)
    h5f.create_dataset('char_labels', data=listchar)
    h5f.create_dataset('license_numbers', data=listln)
    h5f.create_dataset('scaling_target_widths', data=listres)
    h5f.create_dataset('noise_SNRs_db', data=listnoise)




def get_params():
    input_dir = ''
    output_file = ''

    # handling argument error exceptions

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input_dir', dest='input_dir', type=str,
                        help='Input directory containing .jpg images')
    parser.add_argument('--output_dir', dest='output_dir', type=str,
                        help='Output directory containing .h5 images')
    args = parser.parse_args()
    if args.input_dir is None:
        raise Exception('Please declare an INPUT directory. Script Syntax: h5Converter input_dir_name output_file_name')
    if args.output_dir is None:
        raise Exception(
            'Please declare an OUTPUT directory. Script Syntax: h5Converter input_dir_name output_file_name')

    print('Input directory is "', input_dir)
    print('Output file is "', output_file)

    return (args.input_dir, args.output_dir)



def get_params2():
    if len(sys.argv) > 3:
        print('You have specified too many arguments')
        sys.exit()

    if len(sys.argv) < 2:
        print('You need to specify the input dir path and output file path to be listed')
        sys.exit()

    input_dir = sys.argv[1]
    output_file = sys.argv[2]

    return input_dir, output_file


if __name__ == "__main__":
    input_dir, output_file = get_params2()

    convert_dir(input_dir, output_file, 50, 100)
    print('Conversion successful. Output: ', output_file)

    # Load h5py file
    hf = h5py.File('/home/clizia/Scrivania/out.hdf5', 'r')
    print(hf.keys())
    images = hf['images']
    length_labels=hf['length_labels']
    char_labels = hf['char_labels']
    license_number = hf['license_numbers']
    scaling_target_widths=hf['scaling_target_widths']
    noise_SNRs_db=hf['noise_SNRs_db']

    print(images)
    print(length_labels)
    print(char_labels)
    print(license_number)
    print(scaling_target_widths)
    print(noise_SNRs_db)
    plt.subplots(3, 4, figsize=(20, 20))

    for i in range(12):
        img_np = images[i]
        plt.subplot(3, 4, 1 + i)
        plt.imshow(img_np)

    plt.show()
