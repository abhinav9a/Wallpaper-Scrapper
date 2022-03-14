from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import os

# Download Location
image_dir = os.path.abspath('.\\images')
# Creates a list of all the files in image_dir
files_list = os.listdir(image_dir)

start_page = 1
max_pages = 25
url = 'https://wall.alphacoders.com/by_category.php?id=3&name=Anime+Wallpapers&page='


# Creates headless Chrome Webdriver instance
chrome_options = Options()
# chrome_options.add_argument('headless')
driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)

try:
    for page_no in range(start_page, max_pages):
        driver.get(url+str(page_no))
        # Find image thumbnail details
        elements = driver.find_elements_by_class_name('boxgrid')

        # Extracts image page links from thumbnail elements
        images = [element.find_element_by_tag_name('a').get_attribute('href') for element in elements]
        print(len(images))
        # print(images)

        for image in images:
            # Navigate to the image page
            driver.get(image)
            # Find image download link
            download = driver.find_element_by_xpath('//*[@id="page_container"]/div[4]/a').get_attribute('href')

            # Extracts image name from download url "https://images.alphacoders.com/605/605592.png"
            filename = download.split('/')[-1]
            file_path = os.path.join(image_dir, filename)

            # Checks if image already exists
            if filename in files_list:
                print('Wallpaper already exists!')
                continue

            print(f'Downloading image: {filename} ...')
            # Save image
            with open(file_path, 'wb') as f:
                f.write(requests.get(download).content)
            print(f'Download complete: {filename}')


finally:
    # Close webdriver
    driver.quit()
