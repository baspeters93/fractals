from PIL import Image
from colorsys import hsv_to_rgb
from math import log10

def get_color(i, depth):

    h = (float(i) / depth)
    r, g, b = hsv_to_rgb(h, 1., 1.)

    return (int(r * 255), int(g * 255), int(b * 255))


def remap(o1, o2, n1, n2):

    old_range = o1 - o2
    new_range = n1 - n2
    ratio = new_range / old_range

    return lambda x: (x - o1) * ratio + n1

def is_in_mandelbrot(c, depth):

    z = 0

    for i in range(0, depth):

        z = z**2 + c

        if abs(z) >= 2:
            i = i + 1 - log10(log10(abs(z))) / log10(2)
            return False, i

    return True, i

def main():

    height = int(raw_input("Height: "))
    width = int(raw_input("Width: "))
    depth = int(raw_input("Depth/iterations: "))

    horiz_map = remap(0, width, -2.0, 1.5)
    vert_map = remap(0, height, -1.5, 1.5)

    image = Image.new("RGB", (width, height), "#FFFFFF")
    pixels = image.load()

    print "Starting..."

    for x in range(0, width):

        real = horiz_map(x)

        for y in range(0, height):

            imaginary = vert_map(y)
            c = complex(real, imaginary)

            inSet, iterations = is_in_mandelbrot(c, depth)
            if inSet:
                pixels[x, y] = (0,0,0)
            else:
                color = get_color(iterations, depth)
                pixels[x, y] = color


    image.save("mandelbrot%dx%dits=%d.bmp" % (height, width, depth))
    print "Done."

if __name__ == "__main__":
    main()