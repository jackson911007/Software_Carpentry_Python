#manipulate
images: one to blur the image and one to set the luminance (or brightness) of
the image.

from PIL import Image


def blur(fptr, mask=3):
    '''
    Apply a blur to an image. Saves both the original image and the
    newly-blurred image.

    **Parameters**

        fptr: *str*
            The name of an image file, with its extension
            (ex. spring.jpg, cat.png).
        mask: *int, optional*
            The size of our kernel mask.

    **Returns**

        None

    For extra info:

        *https://www.youtube.com/watch?v=C_zFhWdM4ic
    '''

    # We can open two images seperately, and only change img (thus, keeping
    # the original image unchanged for calculation purposes).
    # Note - we convert to RGB to circumvent some issues with different
    # file formats.
    original_img = Image.open(fptr).convert("RGB")
    img = Image.open(fptr).convert("RGB")

    width, height = img.size
    
    
   
    for x in range(width):
        for y in range(height):
            pxl = img.getpixel((x, y))
# Set up the range
            Leftnum = x - 1
            Rightnum = x + 1
            Uppernum = y - 1
            Bottomnum = y + 1
# Collect r, g, b value as a list
            red = []
            green = []
            blue = []
# Set up the conidtion of borders
            if x - 1 < 0:
                Leftnum = 0
            if y - 1 < 0:
                Uppernum = 0
            if x + 1 > width - 1:
                Rightnum = width - 1
            if y + 1 > height - 1:
                Bottomnum = height - 1
# Collect the data in the borders and put them into the list            
            for xi in range(Leftnum, Rightnum):
                for yi in range(Uppernum, Bottomnum):
                    pixel_value = img.getpixel((xi, yi))
                    red.append(pixel_value[0])
                    green.append(pixel_value[1])
                    blue.append(pixel_value[2])                    
# Get the average of r, g, b value and output them to the picture                        
# raise Exception("Blurred pxl must still be calculated.")
            blur = (sum(red) // len(red), sum(green) // len(green), sum(blue) // len(blue))
            img.putpixel((x, y), blur)           
# Save both images so we can verify if we changed the correct one.
    base_name = '.'.join(fptr.split(".")[0:-1])
    fptr_2 = base_name + "_blurred.png"
    img.save(fptr_2)
    fptr_2 = base_name + "_original.png"
    original_img.save(fptr_2)

def set_luminance(fptr, l_val):
    '''
    Luminance is a method of determining how "bright" the image is. It can
    be easily calculated per pixel with the following formula:

        l_pxl = 0.299 * R + 0.587 * G + 0.114 * B0.114

    Now, for an entire image we can calculate either the total luminance, or
    the average luminance over the whole image:

        l_avg = sum(l_pxl) / N_pxl

    We want to set the luminance of an image to a user specified value,
    allowing us to essentially set how bright our image is. We can use the
    get_pxl_luminance() and get_luminance() functions below to help us.

    **Parameters**

        fptr: *str*
            The name of an image file, with its extension
            (ex. spring.jpg, cat.png).
        l_val: *float*
            The desired luminance to set the image to.

    **Returns**

        None
    '''
### INSERT YOUR CODE HERE
    img = Image.open(fptr).convert("RGB")
    width, height = img.size
# The difference between the pixel value we set and the avg pixel value
    Times = (l_val / get_luminance(img))
    for x in range(width):
        for y in range(height):
            pxl = img.getpixel((x, y))
            il_red = pxl[0] * Times
            il_green = pxl[1] * Times
            il_blue = pxl[2] * Times
            img.putpixel((x, y), (int(il_red), int(il_green), int(il_blue)))
# Save image
    base_name = '.'.join(fptr.split(".")[0:-1])
    fptr_2 = base_name + "_luminance.png"
    img.save(fptr_2)

def get_pxl_luminance(pxl):
    '''
    Given a pixel, this function will calculate its luminance.

    **Parameters**

        pxl: *tuple, int*
            A tuple of integers holding RGB values.

    **Returns**

        l_val: *float*
            The pixel luminance.
    '''

### INSERT YOUR CODE HERE
#function for calculating the pxl
    l_pxl = 0.299 * pxl[0] + 0.587 * pxl[1] + 0.114 * pxl[2]
    return l_pxl

def get_luminance(img):
    '''
    Returns the average luminance of an image.

    **Parameters**

        img: *PIL.Image*
            A PIL image object.

    **Returns**

        l_val: *float*
            The image luminance.
    '''

### INSERT YOUR CODE HERE
    img = Image.open(fptr).convert("RGB")
    width, height = img.size
    N_pxl = width * height
    total = 0
# Run over x, y, and get each R, G, B, Then, calculate the average luminance
    for x in range(width):
        for y in range(height):
            pxl = img.getpixel((x, y))
            l_pxl = get_pxl_luminance(pxl)
            total = total + l_pxl
    l_avg = total / N_pxl
    return l_avg

if __name__ == "__main__":
    fptr = "JHU.jpg"
    blur(fptr)
    print(get_luminance(fptr))
    set_luminance(fptr, 150.0)

