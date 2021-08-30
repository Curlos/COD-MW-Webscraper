from bs4 import BeautifulSoup
import requests
import shutil
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_driver_path = "/Users/curlos/Desktop/Development/chromedriver"


def get_all_killstreaks(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    killstreak_img_elems = soup.select('.blog-image img')
    save_dir = 'Killstreaks'

    for killstreak_img_elem in killstreak_img_elems:
        filename = killstreak_img_elem['src'].split('-')[-1].strip()
        img_link = 'https://blog.activision.com' + killstreak_img_elem['src']
        get_one_file(filename, img_link, save_dir)


def get_all_weapons(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    weapon_link_elems = soup.select('.item-image a')
    save_dir = 'Guns'

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(
        options=options, executable_path=chrome_driver_path)

    i = 1
    for weapon_link_elem in weapon_link_elems:
        weapon_url = 'https://www.gamesatlas.com' + weapon_link_elem['href']
        driver.get(weapon_url)
        weapon_img_elem = driver.find_elements_by_css_selector(
            '.item-image img')[0]
        get_one_file(f'{str(i).zfill(3)}.jpg',
                     weapon_img_elem.get_attribute('src'), 'Weapons')

        i += 1


def get_one_file(filename, img_link, save_dir):

    print(f"Downloading {filename}...", end="")

    r = requests.get(img_link, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        shutil.move(filename, save_dir)
        print(f"Success!")
    else:
        print(f"Failed!")


get_all_killstreaks(
    'https://blog.activision.com/call-of-duty/2019-10/The-Basics-of-Call-of-Duty-Modern-Warfare-Killstreaks')

get_all_weapons('https://www.gamesatlas.com/cod-modern-warfare/weapons/')
