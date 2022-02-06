# Curseforge Scraper

This is a python script that uses Selenium to scrape files and information from [Curseforge](https://www.curseforge.com/minecraft).

## Functions

```
cfscraper_single(url, download_directory)

url is a string of the url of the item you want
download_directory is a string of the download directory you want to download the items to

```
for example:
cfscraper_single('https://www.curseforge.com/minecraft/mc-mods/farlands-forge',f'C:\CurseforgeScraperProject\Mods')



```
cfscraper_multi(url, start_page, end_page, download_directory)

url is a string of the url of the item you want
start_page is an int of the page you want to start on
end_page is an int of the page you want to end on
download_directory is a string of the download directory you want to download the items to

```
for example:
cfscraper_multi('https://www.curseforge.com/minecraft/mc-mods?filter-sort=1',1,2,f'C:\CurseforgeScraperProject\Mods')

![end_result1](https://raw.githubusercontent.com/rarwin77/Curseforge-Scraper/main/exampleresultcss.png)

![end_result2](https://raw.githubusercontent.com/rarwin77/Curseforge-Scraper/main/individualresultcss.png)
