import os

# Function to rename multiple files
def main():
    path= "/home/clizia/Scrivania/dataset_split/test/"
    for count, filename in enumerate(os.listdir(path)):
        name=os.path.splitext(filename)[0]
        print(name)
        dst ="italy_license_number_" + name + "_resolution_12_noise_SNR_db_20.png"
        #print(dst)
        src =path+ filename
        dst =path + dst

        # rename() function will
        # rename all the files
        os.rename(src, dst)

# Driver Code
if __name__ == '__main__':

    # Calling main() function
    main()
