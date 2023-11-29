import cv2
import numpy as np
import pyautogui
import time as t
template_path = 'img.png'
def find_and_highlight_image(template_path):
    # Load the template image
    template = cv2.imread(template_path)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template_height, template_width = template_gray.shape[::-1]

    # Create a resizable window
    cv2.namedWindow('Image Found', cv2.WINDOW_NORMAL)

    while True:
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Convert the screenshot to grayscale
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Match the template in the screenshot
        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Threshold for template matching
        threshold = 0.50

        if max_val > threshold:
            # Get the center of the bounding box
            top_left = max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)

            # Adjust the center vertically to bring the circle higher by 45 pixels
            center = (center[0] + 15, center[1] - 45)  # Adjust these values as needed

            # Increase circle radius
            radius = min(template_width, template_height) // 2

            # Get the color of the region inside the circle from the screenshot
            region_of_interest = screenshot[center[1] - radius:center[1] + radius,
                                            center[0] - radius:center[0] + radius]
            average_color = np.mean(region_of_interest, axis=(0, 1))

            # Print the real color
            actual_color = average_color.astype(int)
            blue = int(actual_color[0])
            green = int(actual_color[1])
            red = int(actual_color[2])
            cv2.circle(screenshot, center, radius, (blue, green, red), 2)

            # Directly access pixel values
            pixel_values = region_of_interest.flatten()

            # Display the result
            cv2.imshow('Image Found', screenshot)

            # Wait for a short time (1 millisecond) and handle key events
            key = cv2.waitKey(1)
            if key == 27:  # 27 is the ASCII code for the 'Esc' key
                print("Closing Vision")
                break
            
        # Pause for a short duration before taking the next screenshot
        t.sleep(2)

    # Close the OpenCV window
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Specify the path to the template image
    find_and_highlight_image(template_path)