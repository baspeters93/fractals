from PIL import Image
from colorsys import hsv_to_rgb

def getColor(i, depth):

    h = (float(i) / depth) * 360
    r, g, b = hsv_to_rgb(h/360, 1., 1.)

    return (int(r * 255), int(g * 255), int(b * 255))


def remap(o1, o2, n1, n2):

    oldRange = o1 - o2
    newRange = n1 - n2
    ratio = newRange / oldRange

    return lambda x : (x - o1) * ratio + n1

def isInMandelbrot(c, depth):

    z = 0

    for i in range(0, depth):

        z = z**2 + c
        if abs(z) >= 2:
            return False, i

    return True, i

def main():

    height = 1000 #int(raw_input("Height: "))
    width = 1000 #int(raw_input("Width: "))
    depth = 25 #int(raw_input("Depth/iterations: "))

    horizontalMap = remap(0, width, -2.0, 1.5)
    verticalMap = remap(0, height, -1.5, 1.5)

    image = Image.new("RGB", (width, height), "#FFFFFF")
    pixels = image.load()

    print "Starting..."

    for x in range(0, width):

        real = horizontalMap(x)

        for y in range(0, height):

            imaginary = verticalMap(y)
            c = complex(real, imaginary)

            inSet, iterations = isInMandelbrot(c, depth)
            if inSet:
                pixels[x, y] = (0,0,0)
            else:
                color = getColor(iterations, depth)
                pixels[x, y] = color


    image.save("mandelbrot%dx%dits=%d.bmp" % (height, width, depth))
    print "Done."

if __name__ == "__main__":
    main()