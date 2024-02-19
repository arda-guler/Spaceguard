from PIL import Image, ImageEnhance
import numpy as np
import os
import imageio
import pyautogui
import keyboard as kbd
from scipy import ndimage

def take_screenshot(x, y, width, height, filename):
    try:
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot.save(filename)
        print('Screenshot saved successfully as "' + filename + '"')
    except Exception as e:
        print(f"Error: {e}")

def open_image_without_alpha(image_path):
    img = Image.open(image_path)
    
    # dsiregard alpha because what the fuck, okay?
    img_without_alpha = img.convert('RGB')
    
    return img_without_alpha

def subtract_and_save_average(image_paths, averaged_image, contrast_center):
    subtracted_images = []

    for image_path in image_paths:
        current_image = open_image_without_alpha(image_path)
        current_array = np.array(current_image, dtype=np.int32)

        # no alpha!
        current_array = current_array[:, :, :3]

        subtracted_array = np.clip(current_array - np.array(averaged_image), 0, 255).astype(np.uint8)

        # do not hard code this next time
        contrast_factor = 2.0
        adjusted_array = (subtracted_array - contrast_center) * contrast_factor + contrast_center
        adjusted_array = np.clip(adjusted_array, 0, 255).astype(np.uint8)

        subtracted_image = Image.fromarray(adjusted_array)
        subtracted_images.append(subtracted_image)

        base_filename, _ = os.path.splitext(os.path.basename(image_path))
        subtracted_image.save(f"{base_filename}_subtracted_average_enhanced.jpg")

    return subtracted_images

def subtract_and_save_previous(image_paths, contrast_center):
    subtracted_images = []

    previous_image = open_image_without_alpha(image_paths[0])
    
    for image_path in image_paths[1:]:
        current_image = open_image_without_alpha(image_path)
        current_array = np.array(current_image, dtype=np.int32)

        # no alpha dammit
        current_array = current_array[:, :, :3]

        subtracted_array = np.clip(current_array - np.array(previous_image), 0, 255).astype(np.uint8)

        contrast_factor = 2.0
        adjusted_array = (subtracted_array - contrast_center) * contrast_factor + contrast_center
        adjusted_array = np.clip(adjusted_array, 0, 255).astype(np.uint8)

        subtracted_image = Image.fromarray(adjusted_array)
        subtracted_images.append(subtracted_image)

        base_filename, _ = os.path.splitext(os.path.basename(image_path))
        subtracted_image.save(f"{base_filename}_subtracted_previous_enhanced.jpg")

        # Update the previous image for the next iteration
        previous_image = current_image

    return subtracted_images

def weighted_average_images(images1, images2, weight1, weight2):
    weighted_images = []

    for img1, img2 in zip(images1, images2):
        weighted_array = (np.array(img1) * weight1 + np.array(img2) * weight2).astype(np.uint8)
        weighted_image = Image.fromarray(weighted_array)
        weighted_images.append(weighted_image)

    return weighted_images

def create_gif(images, output_gif, gif_duration):
    imageio.mimsave(output_gif, [np.array(img) for img in images], duration=gif_duration)

def main():
    image_paths = []

    filenum = 1
    taking_images = True
    print("Ready to take images!\n")
    while taking_images:
        if kbd.is_pressed("Z"):
            take_screenshot(0, 250, 1500, 650, str(filenum) + ".png")
            image_paths.append(str(filenum) + ".png")
            filenum += 1

        elif kbd.is_pressed("X"):
            print("Processing...")
            taking_images = False

    # == == PARAMS == ==
    gif_duration = 0.15 # per frame
    contrast_center = 0.2
    weight_average1 = 0.2  # Weight for average diff.
    weight_average2 = 0.8  # Weight for sequential diff.
    # == == == == == ==

    averaged_image = open_image_without_alpha(image_paths[0])

    subtracted_images_average = subtract_and_save_average(image_paths, averaged_image, contrast_center)
    subtracted_images_previous = subtract_and_save_previous(image_paths, contrast_center)

    weighted_average_subtracted = weighted_average_images(subtracted_images_average, subtracted_images_previous, weight_average1, weight_average2)

    create_gif([open_image_without_alpha(image_path) for image_path in image_paths], "original_images.gif", gif_duration)
    create_gif(weighted_average_subtracted, "weighted_average_subtracted_enhanced.gif", gif_duration) # that's a long filename

main()
