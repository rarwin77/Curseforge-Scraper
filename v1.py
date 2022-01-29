from selenium import webdriver
import time
import os
import shutil
import requests
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support.select import Select


#sets downloading preferences
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.dir", r"C:\CurseforgeScraperProject\Mods")
fp.set_preference("browser.helperApps.neverAsk.openFile","application/x-amz-json-1.0, application/java-archive, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-amz-json-1.0, application/java-archive, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.helperApps.alwaysAsk.force", False);
fp.set_preference("browser.download.useDownloadDir", True)
driver = webdriver.Firefox(firefox_profile = fp, executable_path = r"C:\Users\natha\AppData\Local\Programs\Python\Python39\geckodriver.exe")
#############################


#Creates a list of all mod links on the first page of new mods
modpage_list = []
def mod_link_collector(link):
    driver.get(link)
    elements = driver.find_elements(By.CLASS_NAME, "my-auto")
    for part in elements:
        modpage_link = str(part.get_attribute('href'))
        if modpage_link[0:45] == 'https://www.curseforge.com/minecraft/mc-mods/':
            modpage_list.append(modpage_link)
    return modpage_list
    print(modpage_list)
###############################


#goes to each mod in modpage_list and creates a list of download links
mod_names = []
download_links = []
def download_link_collector():
    minicounter = 0
    for link in modpage_list[0:3]:
        driver.get(link)
        driver.implicitly_wait(1)
        mod_name = driver.find_element(By.CLASS_NAME, "break-all")
        mod_names.append(str(mod_name.text))
        download_buttons = driver.find_elements(By.CLASS_NAME, "button--sidebar")
        for button in download_buttons:
            download_links.append(str(button.get_attribute('href')))
    for mod in mod_names:
        print(mod)
        print(mod_names[0+minicounter])
        mod_names[0+minicounter] = mod.replace(':',' ')
        print(mod_names[0+minicounter])
        minicounter += 1
###############################


#Creates a folder for each mod in the modnames list
def mod_folder_creator():
    for mod in mod_names:
        path = f"C:\CurseforgeScraperProject\Mods\{mod}"
        os.mkdir(path)
###############################


#Sub function for the next download function (actually downloads file and moves to correct folder)
def sub_mod_downloader():
    download_button = driver.find_element(By.CLASS_NAME,"icon-fixed-width")
    download_button.click()
    time.sleep(9)
    for file in os.listdir(f"C:\CurseforgeScraperProject\Mods\\"):
        if file.endswith(".jar"):
            file_name = file
            print(file_name)
    os.mkdir(f"C:\CurseforgeScraperProject\Mods\{mod_names[0+spcounter]}\{mod_vr}")
    shutil.move(f"C:\CurseforgeScraperProject\Mods\{file_name}", f"C:\CurseforgeScraperProject\Mods\{mod_names[0+spcounter]}\{mod_vr}")
    #print(f'file name = {file_name}')
    #print(f"C:\CurseforgeScraperProject\Mods\{file_name+'.jar'}")
    #filepath_to_move = f"C:\CurseforgeScraperProject\Mods\{file_name+'.jar'}"
    #shutil.move(f"C:\CurseforgeScraperProject\Mods\{file_name+'.jar'}", f"C:\CurseforgeScraperProject\Mods\{mod_names[0+spcounter]}")

    
    #for typa in types:
    #    if typa.text == 'A' or typa.text == 'B' or typa.text == 'R':
    #        print(typa.text)
    #file_names = driver.find_elements(By.TAG_NAME, "A")
    #for name in file_names:
    #    print(name.text)
    #    print(name.text[len(name.text)-6:len(name.text)])
    #    if name.text[len(name.text)-5:len(name.text)-1] == '.jar':
    #        file_name = name.text
    #    else:
    #        continue
    #print(file_name)
    #download_button = driver.find_element(By.CLASS_NAME,"icon-fixed-width")
    #download_button.click()
    #time.sleep(6)

#Downloads mod to each mod folder

def mod_downloader():
    global file_name
    global spcounter
    global mod_vr
    spcounter = 0
    for modpage in modpage_list[0:3]:
        mod_versions_list = []
        driver.get(modpage)
        files_tab = driver.find_element(By.ID, "nav-files")
        files_tab.click()

        #file_names = driver.find_elements(By.CLASS_NAME, "text-sm")
        #for name in file_names:
        #    print(name.text[len(name.text)-4:len(name.text)])
        #    if name.text[len(name.text)-4:len(name.text)] == '.jar':
        #        file_name = (name.text[0:len(name.text)-4]).replace(' ','+')
        #        print(f'file name = {file_name}') #need to redo all of this to get accurate names
        
        view_all_button = driver.find_element(By.LINK_TEXT,"View All")
        driver.execute_script("return arguments[0].scrollIntoView(true);", view_all_button)
        view_all_button.click()
        #files_tab_2 = driver.find_elements(By.CLASS_NAME, "text-primary-500 hover:no-underline")
        #driver.get(files_tab_2.get_attribute('href'))
        print(modpage)
        versions_dropdown = driver.find_element(By.ID,'filter-game-version').find_elements(By.TAG_NAME, "option")
        for version in versions_dropdown:
            mod_versions_list.append(version.text)
        basedlurl = driver.current_url
        for mod_version in mod_versions_list:
            mod_vr = mod_version.strip()
            #1.18
            if mod_version == '  1.18.1':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A8857')
                sub_mod_downloader()
            if mod_version == '  1.18':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A8830')
                sub_mod_downloader()
            #1.17
            if mod_version == '  1.17.1':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A8516')
                sub_mod_downloader()
            #1.16
            if mod_version == '  1.16.5':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A8203')
                sub_mod_downloader()
            if mod_version == '  1.16.4':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A8134')
                sub_mod_downloader()
            if mod_version == '  1.16.3':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A8056')
                sub_mod_downloader()
            if mod_version == '  1.16.2':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A8010')
                sub_mod_downloader()
            #1.15
            if mod_version == '  1.15.2':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A7722')
                sub_mod_downloader()
            #1.14
            if mod_version == '  1.14.4':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A7469')
                sub_mod_downloader()
            #1.12
            if mod_version == '  1.12.2':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A6756')
                sub_mod_downloader()
            if mod_version == '  1.12.1':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A6711')
                sub_mod_downloader()
            if mod_version == '  1.12':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A6580')
                sub_mod_downloader()
            #1.11
            if mod_version == '  1.11.2':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A6452')
                sub_mod_downloader()
            if mod_version == '  1.11':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A6317')
                sub_mod_downloader()
            #1.10
            if mod_version == '  1.10.2':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A6170')
                sub_mod_downloader()
            #1.9
            if mod_version == '  1.9.4':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A6084')
                sub_mod_downloader()
            if mod_version == '  1.9':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A5946')
                sub_mod_downloader()
            #1.8
            if mod_version == '  1.8.9':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A5806')
                sub_mod_downloader()
            if mod_version == '  1.8.8':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A5703')
                sub_mod_downloader()
            if mod_version == '  1.8':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A4455')
                sub_mod_downloader()
            #1.7
            if mod_version == '  1.7.10':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A4449')
                sub_mod_downloader()
            if mod_version == '  1.7.2':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A361')
                sub_mod_downloader()
            #1.6
            if mod_version == '  1.6.4':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A326')
                sub_mod_downloader()
            #1.5
            if mod_version == '  1.5.2':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A312')
                sub_mod_downloader()
            #1.4
            if mod_version == '  1.4.7':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A272')
                sub_mod_downloader()
            #1.1
            if mod_version == '  1.1':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A186')
                sub_mod_downloader()
            #1.0
            if mod_version == '  1.0.0':
                driver.get(basedlurl+'?filter-game-version=2020709689%3A180')
                sub_mod_downloader()
        spcounter += 1



             
            #print(version)
            #versionname = version.text
            #print(versionname)
            #if versionname == '  1.18.1':
            #    driver.get(driver.current_url+'?filter-game-version=2020709689%3A8857')
            #    versions_dropdown = driver.find_element(By.ID,'filter-game-version').find_elements(By.TAG_NAME, "option")
            #    time.sleep(2)
            #else:
            #    continue

        
        #for option in versions_dropdown[1:len(versions_dropdown)]:
        #    version_option = Select(driver.find_element_by_id('filter-game-version'))
        #    print(option.text)
        #    version_option.select_by_visible_text(option.text)
        #    print(option.text)
        #    time.sleep(1)
        #versions_dropdown = Select(driver.find_element_by_id('filter-game-version'))
        #versions_dropdown.select_by_visible_text('Java')
        #time.sleep(2)


        
        #driver.get(link)
        #time.sleep(7)
        #shutil.move(f"C:\CurseforgeScraperProject\Mods\{}\", f"C:\CurseforgeScraperProject\Mods\{mod})
        #counter += 1
        #current problems, making a new driver for each download complicates things alot, may be better to move files
        #also need to get a list of all versions of a mod and get list of download links of newest for each version


        
        #fp.set_preference("browser.download.dir", f"C:\CurseforgeScraperProject\Mods\{mod_names[0+counter]}")
        #fp.set_preference("browser.helperApps.neverAsk.openFile","application/x-amz-json-1.0, application/java-archive, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
        #fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-amz-json-1.0, application/java-archive, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
        #fp.set_preference("browser.download.folderList", 2)
        #fp.set_preference("browser.helperApps.alwaysAsk.force", False);
        #fp.set_preference("browser.download.useDownloadDir", True)
        #driver = webdriver.Firefox(firefox_profile = fp, executable_path = r"C:\Users\natha\AppData\Local\Programs\Python\Python39\geckodriver.exe")
        #driver.get(link)
        #counter += 1a
        #time.sleep(7)

#        download_button = driver.find_element(By.CLASS_NAME, "alink")
#        file_link = download_button.get_attribute('href')
#        r = requests.get(file_link,stream = True)
#        with open(f'C:\CurseforgeScraperProject\Mods\{mod_names[0+counter]}\{mod_names[0+counter]}'+'.jar','wb') as f:
#            shutil.copyfileobj(r.raw, f) #downloads jar

#    for mod in mod_names:
#        fp.set_preference("browser.download.dir", f"C:\CurseforgeScraperProject\Mods\{mod}") #This sets download folder to each mod folder
#        driver.get(download_links[0+counter])
#        driver.implicitly_wait(6)

#################################


#Download mod png to each folder and converts to ico, and then creates desktop ini to make it the folder icon
image_links = []
def icon_getter():
    global image_links
    counter = 0
    counter2 = 0
    for modpage in modpage_list[0:3]:
        driver.get(modpage) #Goes to each mod page
        image_elements = driver.find_elements(By.CLASS_NAME, "bg-white") #Gets elements with class of the image
        for image_element in image_elements:
            image_links.append(str(image_element.get_attribute('data-featherlight'))) #converts to links
        print(image_links)
        for link in image_links:
            if link == 'None':
                continue
            else:
                r = requests.get(link,stream = True)
                with open(f'C:\CurseforgeScraperProject\Mods\{mod_names[0+counter2]}\{mod_names[0+counter2]}'+'.png','wb') as f:
                    shutil.copyfileobj(r.raw, f) #downoads image
                pngname = f'C:\CurseforgeScraperProject\Mods\{mod_names[0+counter2]}\{mod_names[0+counter2]}'+'.png'#converting to ico
                img = Image.open(pngname)
                img.save(f'C:\CurseforgeScraperProject\Mods\{mod_names[0+counter2]}\{mod_names[0+counter2]}.ico',format = 'ICO', sizes=[(255,255)])
                image_links = []
                counter2 += 1
#################################


#desktop.ini creator
def desktopini_creator():
    for mod in mod_names:
        desktopini = open(f'C:\CurseforgeScraperProject\Mods\{mod}\desktop.ini', 'w')
        desktopini.write(f"[.ShellClassInfo]\nIconFile=.\{mod}.ico\nIconIndex=0\nIconResource=.\{mod}.ico,0")
        desktopini.close()
        os.system("attrib +s "+f'"C:\CurseforgeScraperProject\Mods\{mod}"')
#################################

#Main function
def main_function():
    mod_link_collector('https://www.curseforge.com/minecraft/mc-mods?filter-game-version=&filter-sort=1')
    download_link_collector()
    print(mod_names)
    mod_folder_creator()
    icon_getter()
    desktopini_creator()
    mod_downloader()
#################################
main_function()

    
    



#for mod in mod_names:
#    counter = 0
#    driver.get(modpage_list[counter])
#    image_links = []
#    images = []
#    path = os.path.join(parent_dir, mod)
#    os.mkdir(path)
#    file_object = open(f'C:/Users/natha/Downloads/mods/{mod}/desktop.ini', 'w')
    #need to change icon file and resource to mod name later
#    file_object.write("[.ShellClassInfo]\nIconFile=.\logo16.ico\nIconIndex=0\nIconResource=.\logo16.ico,0")
#    file_object.close()

#    images = driver.find_elements(By.CLASS_NAME, "bg-white")
    
#    for part in images:
#        image_links.append(str(part.get_attribute('data-featherlight')))
#    print(image_links)
#    for link in image_links:
#        if link == 'None':
#            continue
#        else:
#            res = requests.get(link, stream = True)
#           with open(f'C:/Users/natha/Downloads/mods/{mod}/{mod}'+'.png','wb') as f:
#                shutil.copyfileobj(res.raw, f) 
    
#    cmd = r"attrib +s "+os.path.join('C:','Users','natha','Downloads','mods',str(mod))
#    print(cmd)
#    os.system(cmd)
#    counter += 1


#downloads each mod
#for download_link in download_links:
#    print(download_link)
#    driver.get(download_link)
#    driver.implicitly_wait(6)
#    final_download_link = driver.find_elements(By.CLASS_NAME, "alink underline")






    
#files_tab = browser.find_elements(By.ID, "nav-files")
#files_tab_2 = files_tab.find_elements(By.CLASS_NAME, "text-primary-500 hover:no-underline")
#str(files_tab_2.get_attribute('href'))

