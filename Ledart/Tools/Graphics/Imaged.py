from PIL import Image
from Surface import Surface

class ImageSurface(Surface):
    def __init__(self, width, height, fname, thumbnail=False):
        image = Image.open(fname)
        self.imtype = self.determine_type(fname)
        if self.imtype is None:
            raise(Exception("Couldn't load image."))

        # if (image.width > width) or (image.height > height):
        #     if thumbnail:
        #         image.thumbnail((width, height))
        #     else:
        image = image.resize((width, height))

        # create the surface to draw the image on.
        Surface.__init__(self, width=width, height=height)

        if self.imtype == "png":
            self.load_png(image)
        elif self.imtype == "jpg":
            self.load_jpg(image)

    def determine_type(self, imname):
        png = ["png"]
        jpg = ["jpg", "jpeg"]

        for n in png:
            if n in imname.lower():
                return "png"
        for n in jpg:
            if n in imname.lower():
                return "jpg"
        return None

    def load_jpg(self, image, invert=False):
        c = [0, 0, 0]

        for point in self.get_points():
            c = list(image.getpixel(point))
            self[point] = c


    def load_png(self, image, invert=False):
        c = [0, 0, 0]

        for point in self.get_points():
            if(image.mode == "RGBA"):
                c = image.getpixel(point)[:-1]
            else:
                c = image.getpixel(point)
            self[point] = list(c)