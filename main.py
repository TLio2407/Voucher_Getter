from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os

def download_voucher_images():
    # Set up headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Create output folder
        os.makedirs("voucher_images", exist_ok=True)

        # Load website
        driver.get("https://promo.highlandscoffee.com.vn/uudai4?utm_campaign=300_ADTC_MEDIA&utm_term=702627&utm_content=cdnvZ30eHLqAbusgqYJ6DSI0qyOVSANPxY3H9m1749634642&utm_id=accesstrade&utm_source=PAFFAT&utm_medium=DCPM&aff_sid=cdnvZ30eHLqAbusgqYJ6DSI0qyOVSANPxY3H9m1749634642")
        driver.implicitly_wait(5)

        # Find all image elements inside the target <div>
        img_elements = driver.find_elements(By.CSS_SELECTOR, 'div.emblaCarousel_embla__slide__gdevc img')

        print(f"Found {len(img_elements)} images")

        for idx, img in enumerate(img_elements):
            img_url = img.get_attribute("src")
            if not img_url:
                continue

            try:
                response = requests.get(img_url)
                if response.status_code == 200:
                    filename = f"voucher_images/image_{idx}.jpg"
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print(f"✅ Downloaded: {filename}")
                else:
                    print(f"❌ Failed to download image at {img_url} (Status {response.status_code})")
            except Exception as e:
                print(f"❌ Error downloading {img_url}: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    download_voucher_images()
