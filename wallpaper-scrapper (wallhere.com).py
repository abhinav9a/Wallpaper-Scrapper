from selenium import webdriver
from selenium.webdriver import ChromeOptions
from clint.textui import progress
import os
import time
import requests

# Download location
image_dir = os.path.abspath('.\\images')
# Creates a list of all the files in image_dir
file_list = os.listdir(image_dir)

start_page = 1
max_pages = 2

# Login details
email_id = 'your email-id'
password = 'your password'

# Search query
query = 'anime'
url = 'https://wallhere.com/en/wallpapers?q=' + query + '&NSFW=off&page='


def login():
    chrome_options = ChromeOptions()
    # Run chrome webdriver in headless mode
    chrome_options.add_argument('headless')
    chrome_options.add_argument('--log-level=3')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://wallhere.com/en/login')
    # Wait for cloudfare redirect
    time.sleep(2)

    # Find login form elements
    email = driver.find_element_by_name('email')
    passwd = driver.find_element_by_name('password')
    login = driver.find_element_by_tag_name('button')

    # Submit login details
    email.send_keys(email_id)
    passwd.send_keys(password)
    login.click()

    return driver


# Check if image already exists
def is_file_exists(filename):
    if filename in file_list:
        return True
    return False


# Download wallpaper
def download_wallpaper(start_page, max_pages):
    driver = login()

    try:
        while start_page <= max_pages:
            driver.get(url + str(start_page))
            time.sleep(1)
            print(f'Loading page: {start_page}/{max_pages}')
            start_page += 1
            # Find image thumbnail element
            elements = driver.find_elements_by_class_name('item')
            print(f'Number of images: {len(elements)}')

            # Extract image page links from thumbnail element
            image_links = [element.find_element_by_tag_name('a').get_attribute('href') for element in elements]
            # print(image_links)

            for image in image_links:
                driver.get(image)
                # Extract the download link of image
                download = driver.find_element_by_xpath('/html/body/section/div[2]/div[1]/div/div/div[1]/div[2]/a')\
                    .get_attribute('href')

                # Extract image name from the links "https://get.wallhere.com/photo/anime-1581485.png"
                filename = download.split('/')[-1]
                file_path = os.path.join(image_dir, filename)

                if not is_file_exists(filename):
                    print(f'Downloading image: {filename} ...')
                    r = requests.get(download, stream=True)
                    # Save image
                    with open(file_path, 'wb') as f:
                        # Extract size of the file
                        total_length = int(r.headers.get('content-length'))
                        # Shows progress bar while downloading the image
                        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024)+1):
                            if chunk:
                                f.write(chunk)
                                f.flush()
                    print(f'Download complete: {filename}')
                else:
                    print('Already exists!')

    finally:
        # Close the webdriver
        driver.quit()


if __name__ == "__main__":
    download_wallpaper(start_page, max_pages)
