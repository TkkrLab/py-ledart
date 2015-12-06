from PIL import Image
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("use:\npython2.7 %s %s" % (sys.argv[0], "file.png newfilename"))
        sys.exit(1)

    imfile = sys.argv[1]
    im = Image.open(imfile)
    bg = Image.new("RGBA", im.size, (255, 255, 255))
    bg.paste(im, im)
    bg.save(sys.argv[2] + ".jpg")
