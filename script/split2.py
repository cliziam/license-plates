import h5py
import matplotlib.pyplot as plt

hf = h5py.File('/home/clizia/Scrivania/out.hdf5', 'r')
images = hf['images']
plt.subplots(3,4,figsize = (20,20))

for i in range(12):
    img_np = images[i]
    plt.subplot(3,4,1+i)
    plt.imshow(img_np)

plt.show()
