from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
import time
import os
import VoucherClass
# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(), options=options)

# Load the webpage
driver.get("https://promo.highlandscoffee.com.vn/uudai4?utm_campaign=300_ADTC_MEDIA&utm_term=702627&utm_content=cdnvZ30eHLqAbusgqYJ6DSI0qyOVSANPxY3H9m1749634642&utm_id=accesstrade&utm_source=PAFFAT&utm_medium=DCPM&aff_sid=cdnvZ30eHLqAbusgqYJ6DSI0qyOVSANPxY3H9m1749634642")
time.sleep(2)  # Wait for JS to load

# Get HTML content
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Extract JSON from the __NEXT_DATA__ script tag
script = soup.find("script", {"id": "__NEXT_DATA__"})
if script:
    data = json.loads(script.string)
    # print(json.dumps(data, indent=2))
    with open("json.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
else:
    print("Couldn't find __NEXT_DATA__.")

driver.quit()
start = '"templateData": ['
os.remove("voucher.txt") if os.path.exists("voucher.txt") else None
os.remove("extracted_voucher.txt") if os.path.exists("extracted_voucher.txt") else None

with open("json.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        if start == lines[i].strip():
            with open("voucher.txt", "a", encoding="utf-8") as f:
                while lines[i + 1].strip() != "],":               
                    f.write(lines[i + 1].strip() + "\n")
                    i += 1
    f.close()

def split_tag_and_value(line):
    parts = line.split(":")
    tag = parts[0].strip().replace('"', '')
    value = ":".join(parts[1:]).strip().replace(",","").replace('"', '')
    return tag, value
with open("voucher.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    t = 1
    for line in lines:
        if line.strip() == "{":
            with open("extracted_voucher.txt", "a", encoding="utf-8") as f:
                f.write("New_Voucher " + str(t) + "\n")
                t = t + 1
        if line.strip() not in ["{", "},","}"]:
            tag, value = split_tag_and_value(line.strip())
            tags_to_add = ["id","saleCode","voucherStartDate","voucherEndDate"]
            with open("extracted_voucher.txt", "a", encoding="utf-8") as f:
                if tag in tags_to_add:
                    if tag == "voucherStartDate" or tag == "voucherEndDate":
                        value = value.split("T")[0]  # Keep only the date part
                    f.write(f"{tag}:{value}\n")
                    
# Read the extracted voucher data and create Voucher objects
vouchers = []
with open("extracted_voucher.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        if lines[i].startswith("New_Voucher"):
            current_voucher = VoucherClass.Voucher(
                id = lines[i + 1].split(":")[1].strip(),
                type = lines[i + 4].split(":")[1].strip(),
                start_date = lines[i + 2].split(":")[1].strip(),
                end_date = lines[i + 3].split(":")[1].strip(),
            ) 
            vouchers.append(current_voucher)
            i = min(i + 4, len(lines) - 1)
# Print the total number of vouchers captured
num_vouchers = len(vouchers)
print(f"Total number of vouchers captured: {num_vouchers}")
for voucher in vouchers:
    voucher.print_details()  # Call the method to print details of each voucher
#Print the details of each voucher
