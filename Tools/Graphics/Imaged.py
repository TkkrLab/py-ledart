from PIL import Image
from Surface import Surface

class ImageSurface(Surface):
    def __init__(self, width, height, fname, thumbnail=False):
        self.image = Image.open(fname)
        self.imtype = self.determine_type(fname)
        if self.imtype is None:
            raise(Exception("Couldn't load image."))

        if (self.image.width > width) or (self.image.height > height):
            if thumbnail:
                self.image.thumbnail((width, height))
            else:
                self.image = self.image.resize((width, height))

        # create the surface to draw the image on.
        Surface.__init__(self, width=self.image.width,
                         height=self.image.height)

        if self.imtype == "png":
            self.load_png(self.image)
        elif self.imtype == "jpg":
            self.load_jpg(self.image)

    def determine_type(self, image):
        png = ["png"]
        jpg = ["jpg", "jpeg"]

        imtype = None
        for n in png:
            if n in image.lower():
                imtype = "png"
        for n in jpg:
            if n in image.lower():
                imtype = "jpg"
        return imtype

    def load_jpg(self, image, invert=False):
        imdata = self.image.getdata()

        for i, point in enumerate(self.get_points()):
            if len(imdata[i]) == 3:
                color = imdata[i]
            else:
                raise(Exception("No valid image data found"))
            self[point] = color

    def load_png(self, image, invert=False):
        imdata = self.image.getdata()
        p = 0
        for y in range(0, self.image.height):
            for x in range(0, self.image.width):
                point = (x, y)
                if len(imdata[p]) == 3:
                    color = imdata[p]
                elif len(imdata[p]) == 4:
                    pass
                    r, g, b, alpha = imdata[p]
                    color = [alpha, alpha, alpha]
                if invert:
                    r, g, b = color
                    color = [0xff - r, 0xff - g, 0xff - b]
                self[point] = color
                p += 1