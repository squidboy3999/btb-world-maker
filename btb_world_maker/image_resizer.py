from PIL import Image

def shrink_image_square(image_path,new_name,size):
    image_orig = Image.open(image_path)
    new_image = image_orig.resize((size, size))
    new_image.save(new_name)
