import pyautogui
import keyboard
from PIL import ImageGrab

def left_shift(image, center_x, center_y):
    max_brightness = 255 * 3
    half_max_brightness = max_brightness / 2
    count = 0

    for x in range(int(center_x), -1, -1):
        pixel_brightness = sum(image.getpixel((x, int(center_y))))
        if pixel_brightness < half_max_brightness:
            return count
        count += 1

    return count

def up_shift(image, center_x, center_y):
    max_brightness = 255 * 3
    half_max_brightness = max_brightness / 2
    count = 0

    for y in range(int(center_y), -1, -1):
        pixel_brightness = sum(image.getpixel((int(center_x), y)))
        if pixel_brightness < half_max_brightness:
            return count
        count += 1

    return count

def right_shift(image, center_x, center_y):
    max_brightness = 255 * 3
    half_max_brightness = max_brightness / 2
    count = 0

    for x in range(int(center_x), image.width):
        pixel_brightness = sum(image.getpixel((x, int(center_y))))
        if pixel_brightness < half_max_brightness:
            return count
        count += 1

    return count

def down_shift(image, center_x, center_y):
    max_brightness = 255 * 3
    half_max_brightness = max_brightness / 2
    count = 0

    for y in range(int(center_y), image.height):
        pixel_brightness = sum(image.getpixel((int(center_x), y)))
        if pixel_brightness < half_max_brightness:
            return count
        count += 1

    return count

def get_points():
    print("Move the mouse cursor to the first point and press Enter...")
    keyboard.wait('enter')
    point1 = pyautogui.position()
    print("First point:", point1)

    print("Move the mouse cursor to the second point and press Enter...")
    keyboard.wait('enter')
    point2 = pyautogui.position()
    print("Second point:", point2)

    return point1, point2

def take_screenshot(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height))
    return screenshot

def find_center_of_brightness(image):
    total_brightness = 0
    weighted_x_sum = 0
    weighted_y_sum = 0

    for x in range(image.width):
        for y in range(image.height):
            pixel_brightness = sum(image.getpixel((x, y))) / 3
            total_brightness += pixel_brightness
            weighted_x_sum += x * pixel_brightness
            weighted_y_sum += y * pixel_brightness

    center_x = weighted_x_sum / total_brightness
    center_y = weighted_y_sum / total_brightness

    return center_x, center_y

if __name__ == "__main__":
    running = True
    while running:
        point1, point2 = get_points()
        screenshot = take_screenshot(point1, point2)
        center_x, center_y = find_center_of_brightness(screenshot)
        print("Center of brightness: ({}, {})".format(center_x, center_y))
        
        print("Selecting object...")
        new_x = point1[0] + center_x
        new_y = point1[1] + center_y

        left_offset = left_shift(screenshot, center_x, center_y)
        right_offset = right_shift(screenshot, center_x, center_y)
        up_offset = up_shift(screenshot, center_x, center_y)
        down_offset = down_shift(screenshot, center_x, center_y)

        if left_offset >= right_offset:
            x1 = new_x - left_offset - 5
        else:
            x1 = new_x + right_offset + 5

        if up_offset >= down_offset:
            y1 = new_y - up_offset - 5
        else:
            y1 = new_y + down_offset + 5

        y2 = y1 + (new_y - y1) * 2
        x2 = x1

        x3 = x2 + (new_x - x2) * 2
        y3 = y2
        
        pyautogui.moveTo(x1, y1)
        pyautogui.click()
        pyautogui.moveTo(x2, y2)
        pyautogui.click()
        pyautogui.moveTo(x3, y3)
        pyautogui.click()
        print("Object selected.")

        print("Press Enter to start again...\n")
        keyboard.wait('enter')
