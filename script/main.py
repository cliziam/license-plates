from PIL import Image
import os,sys

path = "/home/clizia/Scrivania/img"
path2 = "/home/clizia/Scrivania/img2"
dirs = os.listdir(path)

for item in dirs:
    print('f')
  #  if os.path.isfile(path+item):
    pf=os.path.join(path,item)
    im = Image.open(pf)
    f, e = os.path.splitext(pf)
    imResize = im.resize((100,50), Image.ANTIALIAS)
    imResize.save(os.path.join(path2,item), 'PNG', quality=90)

