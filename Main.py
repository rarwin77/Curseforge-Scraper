from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import shutil
import requests
import os
import time

def download_preferences_setter(download_directory):
    global driver
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.dir", download_directory)
    fp.set_preference("browser.helperApps.neverAsk.openFile","application/x-amz-json-1.0, application/java-archive, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-amz-json-1.0, application/java-archive, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.helperApps.alwaysAsk.force", False);
    fp.set_preference("browser.download.useDownloadDir", True)
    driver = webdriver.Firefox(firefox_profile = fp)

download_preferences_setter(f'C:\CurseforgeScraperProject\Mods')

def name_getter():
    mod_name = (driver.find_element(By.CLASS_NAME, "break-all").text).replace(':',' ')
    return mod_name

def folder_creator(modname, downloaddirectory):
    try:
        os.mkdir(downloaddirectory+f'\{modname}')
    except:
        print(modname + ' folder already exists')
        pass

def png_getter(modname, downloaddirectory):
    image_elements = driver.find_elements(By.CLASS_NAME, "bg-white")
    for image_element in image_elements:
        if str(image_element.get_attribute('data-featherlight')) != 'None':
            try:
                r = requests.get(image_element.get_attribute('data-featherlight'),stream = True)
            except:
                pass
            else:
                with open(downloaddirectory+f'\{modname}\{modname}'+'.png','wb') as f:
                    shutil.copyfileobj(r.raw, f)

def png_to_icon(modname,downloaddirectory):
    pngname = downloaddirectory + f'\{modname}\{modname}'+'.png'
    try:
        img = Image.open(pngname)
    except:
        pass  
    else:
        img.save(downloaddirectory + f'\{modname}\{modname}.ico',format = 'ICO', sizes=[(48,48)])

def desktopini_creator(modname, downloaddirectory):
    desktopini = open(downloaddirectory + f'\{modname}\desktop.ini', 'w')
    desktopini.write(f"[.ShellClassInfo]\nIconFile=.\{modname}.ico\nIconIndex=0\nIconResource=.\{modname}.ico,0")
    desktopini.close()
    os.system("attrib +s "+ '"' + downloaddirectory + f'\{modname}"')

def infohtml_creator(modname, downloaddirectory):
    description = '<h2>Description:</h2>\n' + driver.find_element(By.CLASS_NAME, "project-detail__content").get_attribute('innerHTML')
    categories = '<h2>Categories:</h2>\n' + driver.find_elements(By.CSS_SELECTOR, "div.flex.-mx-1")[1].get_attribute('innerHTML')
    member_elements = driver.find_elements(By.CSS_SELECTOR, "div.flex.mb-2")
    members = '<h2>Members:</h2>\n'
    for member_element in member_elements[1:len(member_elements)]:
        members = members + member_element.get_attribute('innerHTML')
    infohtml = open(downloaddirectory + f'\{modname}\info.html', 'w')
    try:
        infohtml.write(categories + description + members)
    except:
        infohtml.write(categories + members)
        infohtml.close()
    else:
        infohtml.close()

def download_preferences_setter(download_directory):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.dir", download_directory)
    fp.set_preference("browser.helperApps.neverAsk.openFile","application/x-amz-json-1.0, application/java-archive, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-amz-json-1.0, application/java-archive, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.helperApps.alwaysAsk.force", False);
    fp.set_preference("browser.download.useDownloadDir", True)
    driver = webdriver.Firefox(firefox_profile = fp)

def file_detector(modname, downloaddirectory, version):
    file_moved = 0
    while True:
        for file in os.listdir(downloaddirectory):
            if file.endswith(".jar")or file.endswith(".zip"):
                file_name = file
                try:
                    os.mkdir(downloaddirectory + f"\{modname}\{version}")
                except:
                    print(modname + version + " folder already exists")
                if len(os.listdir(downloaddirectory + f"\{modname}\{version}")) > 0:
                    print(f"deleting {file}")
                    os.remove(downloaddirectory + f"\{file}")
                else:
                    shutil.move(downloaddirectory + f"\{file_name}", downloaddirectory + f"\{modname}\{version}")
                file_moved = 1
                break
        time.sleep(1.5)
        if file_moved == 1:
            break

all_versions = ['1.18.1','1.18','1.17.1','1.16.5',
                '1.16.4,','1.16.3','1.16.2','1.16.1',
                '1.15.2','1.15.1','1.14.4','1.14.3',
                '1.14.2','1.13.2','1.12.2','1.12.1',
                '1.12','1.11.2','1.11','1.10.2',
                '1.10','1.9.4','1.9','1.8.9',
                '1.8.8','1.8','1.7.10','1.7.2',
                '1.6.4']
version_link_parts = ['2020709689%3A8857','2020709689%3A8830','2020709689%3A8516','2020709689%3A8203',
                      '2020709689%3A8134','2020709689%3A8056','2020709689%3A8010','2020709689%3A7892',
                      '2020709689%3A7722','2020709689%3A7675','2020709689%3A7469','2020709689%3A7413',
                      '2020709689%3A7361','2020709689%3A7132','2020709689%3A6756','2020709689%3A6711',
                      '2020709689%3A6580','2020709689%3A6452','2020709689%3A6317','2020709689%3A6170',
                      '2020709689%3A6144','2020709689%3A6084','2020709689%3A5946','2020709689%3A5806',
                      '2020709689%3A5703','2020709689%3A4455','2020709689%3A4449','2020709689%3A361',
                      '2020709689%3A361']
def downloader(modname, downloaddirectory):
    baseurl = driver.current_url
    driver.get(driver.current_url + '/files/all?filter-game-version=')
    dropdown_versions = driver.find_element(By.ID,'filter-game-version').find_elements(By.TAG_NAME, "option")
    version_list = []
    for dropdown_version in dropdown_versions:
        if ((dropdown_version.text).strip())[0] == '1':
            version_list.append((dropdown_version.text).strip())
    for version in version_list:
        vlpcounter = 0
        for aversion in all_versions:
            if version == aversion:
                driver.get(baseurl + '/files/all?filter-game-version=' + version_link_parts[vlpcounter])
                download_button = driver.find_element(By.CLASS_NAME,"icon-fixed-width")
                driver.execute_script("return arguments[0].scrollIntoView(true);", download_button)
                download_button.click()
                time.sleep(1)
                file_detector(modname, downloaddirectory, version)
                time.sleep(2)
            vlpcounter += 1

def cfscraper_single(url, download_directory):
    driver.get(url)
    mod_name = name_getter()
    folder_creator(mod_name, download_directory)
    png_getter(mod_name, download_directory)
    png_to_icon(mod_name, download_directory)
    desktopini_creator(mod_name, download_directory)
    infohtml_creator(mod_name,  download_directory)
    downloader(mod_name, download_directory)

    
#cfscraper_single('https://www.curseforge.com/minecraft/mc-mods/farlands-forge',f'C:\CurseforgeScraperProject\Mods')

def page_links_getter(url):
    links = []
    driver.get(url)
    link_elements = driver.find_elements(By.CLASS_NAME, "my-auto")
    for link in link_elements:
        if str(link.get_attribute('href'))[0:36] == 'https://www.curseforge.com/minecraft':
            links.append(str(link.get_attribute('href')))
    return links

def cfscraper_multi(url, start_page, end_page, download_directory):
    next_link = url + f'&page={start_page}'
    driver.get(url + f'&page={start_page}')
    print(f'Page {start_page}')
    start_page = start_page + 1
    links = page_links_getter(next_link)
    for link in links:
        driver.get(link)
        driver.implicitly_wait(2)
        mod_name = name_getter()
        folder_creator(mod_name, download_directory)
        png_getter(mod_name, download_directory)
        png_to_icon(mod_name, download_directory)
        desktopini_creator(mod_name, download_directory)
        infohtml_creator(mod_name, download_directory)
        downloader(mod_name, download_directory)
    if start_page < end_page:
        cfscraper_multi(url, start_page, end_page, download_directory)

cfscraper_multi('https://www.curseforge.com/minecraft/mc-mods?filter-sort=1',1,2,f'C:\CurseforgeScraperProject\Mods')
