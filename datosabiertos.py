# -*- coding: utf-8 -*-
import os
import pandas as pd
import platform
import sys
import time
import zipfile

from selenium import webdriver

path = os.getcwd()


def datosabiertos(sesion, delete_file):
    prefs = {'download.default_directory' : path}
    ChromeOptions = webdriver.ChromeOptions()
    ChromeOptions.add_argument("--headless")  # Hide the Browser
    ChromeOptions.add_experimental_option("detach", True)
    ChromeOptions.add_argument('--disable-gpu')
    # ChromeOptions.add_argument("--remote-debugging-address=0.0.0.0")
    ChromeOptions.add_experimental_option('prefs', prefs)
    ChromeOptions.add_argument("--disable-infobars")
    ChromeOptions.add_argument('--no-sandbox')

    # Se identifica el sistema para tener la ruta hacia chromium y el cache
    sistema = platform.system()
    if sistema == "Windows":
        if sesion == True:
            ChromeOptions.add_argument('--user-data-dir={}\\{}'.format(path,"cache"))
        # Debe descargar chromedriver en el mismo directorio del archivo py
        driver = webdriver.Chrome('chromedriver.exe', options=ChromeOptions)
    elif sistema == "Linux":
        if sesion == True:
            ChromeOptions.add_argument('--user-data-dir={}/{}'.format(path,"cache"))
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=ChromeOptions)
    elif sistema == "Darwin":
        print("Tiene que agregar los argumentos para MacOS")
        sys.exit()
    else:
        print("No se puede identificar su sistema")
        sys.exit()


    driver.get("https://www.datosabiertos.gob.pe/")
    driver.maximize_window()
    time.sleep(3)

    driver.find_element_by_id("facetapi-link--199").click()
    time.sleep(3)

    driver.find_element_by_xpath("/html/body/div[3]/div/div/section/div/div/div/div/div[1]/div/div[2]/div/div/ul/li[1]/a").click()
    time.sleep(3)

    driver.find_element_by_xpath("//*[@id='main']/div/section/div/div/div/div/div[1]/div/div[4]").click()
    time.sleep(1)

    driver.find_element_by_id("facetapi-link--9").click()
    time.sleep(1)

    donaciones = driver.find_element_by_name("query")
    donaciones.send_keys("donaciones")
    time.sleep(1)

    driver.find_element_by_id("edit-submit-dkan-datasets").click()
    time.sleep(3)

    driver.find_element_by_xpath("/html/body/div[3]/div/div/section/div/div/div/div/div[2]/div/div/div/div/div[3]/div/article/div[2]/h2/a").click()
    time.sleep(3)

    driver.find_element_by_xpath("/html/body/div[3]/div/div/section/div/div/div/div/div[2]/div/div/div/article/div/div[3]/div/div/ul/li[3]/div/span/a").click()
    time.sleep(3)

    while not os.path.isfile("pcm_donaciones.zip"):
        print("No se encuentra el zip pcm_donaciones.zip")
        print("Puede cancelar el proceso precionando ctrl + Z")
        time.sleep(3)


    zf = zipfile.ZipFile("pcm_donaciones.zip")
    for file in zf.namelist():
        df = pd.read_csv(zf.open(file), encoding='latin-1')
        region = set(df["REGION"].values.tolist())
        for i in region:
            new_csv = df[df['REGION'] == i]
            new_csv.to_csv(f"csv/{i.lower()}.csv", index = False)

    if delete_file == True:
        dir_zip = os.listdir(path)
        for item in dir_zip:
            if item.endswith(".zip"):
                os.remove( os.path.join(path, item))

if __name__== "__main__":
    sesion = False
    delete_file = False
    argv = sys.argv[1:]

    if "-s" in argv:
        sesion = True
    if "-d" in argv:
        delete_file = True

    datosabiertos(sesion, delete_file)
