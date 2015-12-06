from PIL import Image
import sys
import os
import glob

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("use:\npython2.7 resize.py width height")
        sys.exit(1)

    size = int(sys.argv[1]), int(sys.argv[2])

    for infile in glob.glob("*.png"):
        file, ext = os.path.splitext(infile)
        if "min" not in file.lower():
            im = Image.open(infile)
            im.thumbnail(size)
            im.save(file + "-min" + ext, "PNG")

    # imfile = sys.argv[1]
    # size = int(sys.argv[2]), int(sys.argv[3])

    # im = Image.open(imfile)
    # im.thumbnail(size, Image.ANTIALIAS)
    # im.save(imfile.split('.')[0] + ".thumbnail", "PNG", quality=90)
