from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # 로케이터 유형을 위한 모듈 추가
import requests
import os
import time


def download_images_with_scroll(query, img_name, folder_name, max_retries=1):
    base_url = 'https://www.google.co.kr'
    url = base_url + "/search?q=" + query + "&source=lnms&udm=2"
    
    # Chrome 드라이버 경로 설정
    chrome_options = Options()  # ChromeOptions 객체 생성
    chrome_options.add_argument('--headless')  # headless 모드로 실행
    executable_path = r'C:\Users\TAK\Desktop\Flask\selenium_env\chromedriver.exe'  # Chrome 드라이버 경로
    os.environ["webdriver.chrome.driver"] = executable_path
    
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)
    
    # 이미지 로딩을 위해 충분한 시간을 줍니다.
    time.sleep(2)
    
    # 이미지 가져오기
    images = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # 스크롤 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # 스크롤이 더이상 내려지지 않으면 중지
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        
        last_height = new_height

    # 이미지 가져오기
    image_elements = driver.find_elements(By.CSS_SELECTOR, '.YQ4gaf')  
    for img in image_elements:
        img_url = img.get_attribute('src')
        if img_url and 'http' in img_url and '.zr758c' not in img_url:
            images.append(img_url)

    # 저장 폴더 경로
    save_dir = "C:/Users/TAK/Desktop/Flask/베네딕트"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    
    print(len(images))
    
    
    for i, img_url in enumerate(images):
        retries = 0
        if i < 500:  
            while retries < max_retries:
                try:
                    response = requests.get(img_url, timeout=5)
                    with open(f"{save_dir}/{img_name}_{i}.jpg", 'wb') as file:
                        file.write(response.content)
                    break
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                    print(f"Error downloading image {img_url}: {e}. Retrying...")
                    retries += 1
                    time.sleep(2)   
            else:
                print(f"Failed to download image {img_url} after {max_retries} retries.")
        else:
            break

    driver.quit()

query = '베네딕트 얼굴'
img_name = 'vd'
folder_name = '베네딕트 얼굴'


download_images_with_scroll(query, img_name, folder_name)
 