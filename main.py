"""at the first start in the terminal, go to the folder with the mine.py file
 and execute the command "venv\Scripts\activate".
 Then you need to install the modules used by the command
 pip install undetected_chromedriver
 pip install selenium
 pip install googletrans==3.1.0a0

 Script link example - https://www.readwn.com/novel/ancient-fiend-dragon-emperor.html
 """

import shutil
import time
import os
import unicodedata
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from googletrans import Translator


def main():
    url = input("Enter The Novel link: ")
    start_chapter = input("Enter start chapter: ")
    directory = input("Enter the novel name: ")
    chapter_directory = input("Enter the name of the chapter directory: ")
    language = input("What language do you want to translate into, such as en, uk or any other: ")

    translator = Translator()

    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)

    driver.get(url)

    chapters_list = []
    flag = True
    while flag:
        try:
            page_load = driver.find_element(By.CSS_SELECTOR, ".chapter-list").find_elements(By.CSS_SELECTOR,'li [href]')

            for ele in page_load:
                chapters_list.append(ele.get_attribute('href'))

            driver.find_element(By.CSS_SELECTOR, '.heading').find_element(By.LINK_TEXT, '>').click()
            time.sleep(1)
        except NoSuchElementException:
            flag = False

    time.sleep(2)

    for link in chapters_list:
        cutted_chap_num = link.split('_')[-1].replace('.html', '')
        if int(cutted_chap_num) >= int(start_chapter):
            driver.get(link)
            page_load = EC.presence_of_element_located((By.CSS_SELECTOR, ".chapter-content"))
            WebDriverWait(driver, 10).until(page_load)

            novel_text = driver.find_element(By.CSS_SELECTOR, ".chapter-content").text
            chunks_for_translate = [novel_text[i:i + 4500] for i in range(0, len(novel_text), 4500)]

            if not os.path.exists(fr'{directory}\{chapter_directory} {cutted_chap_num}'):
                os.makedirs(fr'{directory}\{chapter_directory} {cutted_chap_num}', exist_ok=True)

            for line in chunks_for_translate:
                translate_result = translator.translate(line, dest=language).text
                text = unicodedata.normalize('NFKD', translate_result)

                with open(fr"{directory}\{chapter_directory} {cutted_chap_num}\{cutted_chap_num}.txt", mode='a',
                          encoding='utf-8') as f:
                    f.write(text)

            time.sleep(1)

    driver.quit()

    try:
        shutil.make_archive(rf'{directory}', 'zip', directory)
    except Exception as e:
        print(e)
    finally:
        print("Zip success!")


if __name__ == '__main__':
    main()