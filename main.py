import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
def load_image(path):
    """Load and convert image to grayscale numpy array."""
    img = Image.open(path).convert('L')  # grayscale
    return np.array(img)

def compare_images_percentage(path1, path2):
    img1 = load_image(path1)
    img2 = load_image(path2)

    # Resize to match if dimensions differ
    if img1.shape != img2.shape:
        print("Resizing second image to match first image...")
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    ssim_score, _ = ssim(img1, img2, full=True)
    similarity_percentage = ssim_score * 100

    print(f"Similarity: {similarity_percentage:.2f}%")
    return similarity_percentage

def count_captured_images():
    if not os.path.exists(CAPTURE_DIR):
        return 0
    return len([f for f in os.listdir(CAPTURE_DIR) if os.path.isfile(os.path.join(CAPTURE_DIR, f))])


# --- CONFIG ---
URL = "https://promo.highlandscoffee.com.vn/uudai4?utm_campaign=300_ADTC_MEDIA&utm_term=702627&utm_content=cdnvZ30eHLqAbusgqYJ6DSI0qyOVSANPxY3H9m1749634642&utm_id=accesstrade&utm_source=PAFFAT&utm_medium=DCPM&aff_sid=cdnvZ30eHLqAbusgqYJ6DSI0qyOVSANPxY3H9m1749634642"
DRAG_DISTANCE_X = 400
DRAG_DISTANCE_Y = 0
REPEAT = 10

CAPTURE_LEFT = 725       # Start 1/3 from the left
CAPTURE_TOP = 5        # Vertically from where the drinks start
CAPTURE_WIDTH = 450      # 1/3 of 1920
CAPTURE_HEIGHT = 600     # Adjust to include full drink + some text
CAPTURE_DIR = "captures"

if not os.path.exists(CAPTURE_DIR):
    os.makedirs(CAPTURE_DIR)
else:
    # Clear existing captures
    for file in os.listdir(CAPTURE_DIR):
        file_path = os.path.join(CAPTURE_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
# --- SETUP CHROME DRIVER ---
options = Options()
# options.add_argument("--headless=new")  # Uncomment for headless mode
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(), options=options)
driver.get(URL)
time.sleep(5)

# --- SCROLL TO BOTTOM TO LOAD CONTENT ---
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# --- GET CENTER OF THE WINDOW ---
window_size = driver.get_window_size()
center_x = window_size["width"] // 2
center_y = window_size["height"] // 2

actions = ActionChains(driver)
for i in range(1,REPEAT +1):
    # Drag
    actions.move_by_offset(center_x, center_y) \
           .click_and_hold() \
           .move_by_offset(DRAG_DISTANCE_X, DRAG_DISTANCE_Y) \
           .release() \
           .perform()
    
    print(f"Drag #{i} completed.")
    time.sleep(1)

    # Screenshot the whole page
    driver.save_screenshot("full_screenshot.png")

    # Crop specific area
    img = Image.open("full_screenshot.png")
    cropped_img = img.crop((
        CAPTURE_LEFT,
        CAPTURE_TOP,
        CAPTURE_LEFT + CAPTURE_WIDTH,
        CAPTURE_TOP + CAPTURE_HEIGHT
    ))

    path = os.path.join(CAPTURE_DIR, f"capture_{i}.png")
    cropped_img.save(path)
    print(f"Saved capture_{i}.png")
    if i > 1 and compare_images_percentage(f"captures/capture_1.png", f"captures/capture_{i}.png") > 95.0:
        print("No change detected, stopping.")
        num_files = count_captured_images()
        print(f"Number of images in '{CAPTURE_DIR}': {num_files}")
        break
    actions.reset_actions()

# --- DONE ---
driver.quit()
