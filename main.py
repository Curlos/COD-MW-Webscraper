from bs4 import BeautifulSoup
import requests
import shutil
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from pprint import pprint

chrome_driver_path = "/Users/curlos/Desktop/Development/chromedriver"


def get_all_weapons(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    weapon_link_elems = soup.select('.item-image a')
    save_dir = 'Weapons'

    weapons = {'Assault Rifles': [], 'SMGs': [], 'Shotguns': [], 'LMGs': [
    ], 'Marksman Rifles': [], 'Sniper Rifles': [], 'Handguns': [], 'Launchers': [], 'Melee': []}

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

        weapon_data = get_one_weapon_data(weapon_url, driver)
        weapons[weapon_data['class']].append(weapon_data)

        pprint(weapon_data)
        print('\n')
        save_to_json(weapons, 'weapons.json')
        # download_file(f'{str(i).zfill(3)}.jpg',
        #                weapon_img_elem.get_attribute('src'), save_dir)

        i += 1
    
    print('Finished getting all weapons!')


def get_one_weapon_data(url, driver):
    weapon_name = driver.find_element_by_css_selector(
        'h1.contentheading').get_attribute("textContent").strip()

    weapon_img_elem_link = driver.find_elements_by_css_selector(
        '.item-image img')[0].get_attribute('src')

    weapon_class = driver.find_element_by_css_selector(
        'a[title^="Weapon Class"]').get_attribute("textContent").strip()

    weapon_accuracy = int(driver.find_element_by_css_selector(
        '.field-entry.accuracy .field-value').get_attribute("textContent").strip())

    weapon_damage = int(driver.find_element_by_css_selector(
        '.field-entry.damage .field-value').get_attribute("textContent").strip())

    range_mobility_control = driver.find_elements_by_css_selector(
        '.field-entry.range .field-value')

    weapon_range = int(
        range_mobility_control[0].get_attribute("textContent").strip())

    weapon_fire_rate = int(driver.find_element_by_css_selector(
        '.field-entry.fire-rate .field-value').get_attribute("textContent").strip())

    weapon_mobility = int(
        range_mobility_control[1].get_attribute("textContent").strip())

    weapon_control = int(
        range_mobility_control[2].get_attribute("textContent").strip())

    weapon_overall = (weapon_accuracy + weapon_damage + weapon_range +
                      weapon_fire_rate + weapon_mobility + weapon_control) / 6

    rounded_overall = round(weapon_overall, 2)

    weapon_description = driver.find_element_by_css_selector(
        '.article-content p').get_attribute("textContent").strip()

    weapon = {
        'name': weapon_name,
        'description': weapon_description,
        'image': weapon_img_elem_link,
        'class': weapon_class,
        'accuracy': int(weapon_accuracy),
        'damage': int(weapon_damage),
        'range': int(weapon_range),
        'fire_rate': int(weapon_fire_rate),
        'mobility': int(weapon_mobility),
        'control': int(weapon_control),
        'overall': rounded_overall,
    }

    return weapon

def save_to_json(dictionary, filename):
    print('Exporting dictionary to JSON file...')

    try:
        with open(filename, "w") as outputFile:
            json.dump(dictionary, outputFile, indent=4)
    except:
        print('Error occured!')

    print('JSON file created!')


def get_all_killstreaks(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    killstreak_img_elems = soup.select('.blog-image img')
    save_dir = 'Killstreaks'

    for killstreak_img_elem in killstreak_img_elems:
        filename = killstreak_img_elem['src'].split('-')[-1].strip()
        img_link = 'https://blog.activision.com' + killstreak_img_elem['src']
        download_file(filename, img_link, save_dir)

def download_file(filename, img_link, save_dir):

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


# get_all_killstreaks('https://blog.activision.com/call-of-duty/2019-10/The-Basics-of-Call-of-Duty-Modern-Warfare-Killstreaks')

get_all_weapons('https://www.gamesatlas.com/cod-modern-warfare/weapons/')
