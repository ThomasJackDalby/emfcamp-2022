from PIL import Image

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", " "]
a = ''

def convert(file_path, target_width):
    image = Image.open(file_path)
    resized_image = resize(image, target_width)
    grayscale_image = convert_to_grayscale(resized_image)

    pixels = grayscale_image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25]*2 for pixel in pixels])

    pixel_count = len(characters)
    
    return "\n".join([characters[index:index+2*target_width] for index in range(0, pixel_count, 2*target_width)])

def resize(image, target_width):
    width, height = image.size
    ratio = height / width
    new_height = int(target_width * ratio)
    return image.resize((target_width, new_height))

def convert_to_grayscale(image):
    return image.convert("L")

if __name__ == "__main__":

    print(convert("images/axe2.jpg", 15))