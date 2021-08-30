from bs4 import BeautifulSoup
import requests
import shutil
import os


def get_all_killstreaks(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    killstreak_img_elems = soup.select('.blog-image img')
    save_dir = 'Killstreaks'

    for killstreak_img_elem in killstreak_img_elems:
        filename = killstreak_img_elem['src'].split('-')[-1].strip()
        img_link = 'https://blog.activision.com' + killstreak_img_elem['src']
        get_one_killstreak(filename, img_link, save_dir)


def get_one_killstreak(filename, img_link, save_dir):

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
