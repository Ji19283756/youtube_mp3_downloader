from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from os import path
from config import *

# search = //*[@id="query"]
# search button = //*[@id="button"]
# download button = //*[@id="result_1"]/div[3]
# download button 2 = //*[@id="download_1"]/div[3]/a[1]


def download_songs(songs):
    # makes sure that there isn't that pop up that says "AlLoW NotIfIcaTioNs?"
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

    # creates the chrome path
    driver = webdriver.Chrome(chrome_driver_path, options=option)
    driver.minimize_window()

    for song in songs:
        while True:
            try:
                driver.get("https://www.mp3juices.cc/")
                driver.minimize_window()

                driver.find_element_by_xpath("//*[@id=\"query\"]").send_keys(song)
                sleep(1.5)
                driver.find_element_by_xpath("//*[@id=\"button\"]").click()
                sleep(1.5)
                driver.find_element_by_xpath("//*[@id=\"result_1\"]/div[3]").click()
                driver.implicitly_wait(20)
                driver.find_element_by_xpath("//*[@id=\"download_1\"]/div[3]/a[1]").click()

                sleep(0.1)
                driver.minimize_window()
                print(song, "finished")

                break
            except:
                pass

        last_song_name = driver.find_element_by_xpath('//*[@id="download_1"]/div[1]').text

    # repeats 240 times (so max is one hour), and checks if the last file downloaded exists,
    # if not then it will keep on waiting
    sleep(5)
    for x in range(file_checks_amount * 4):
        # print(f"repeat: {repeats}")
        if path.exists(f"C:\\Users\\Kedde\\Downloads\\{last_song_name}.mp3"):
            break
        sleep(15)

    # im not sure if this works but it will continue to close tabs until there's no tabs left
    driver.quit()


songs = input("What songs do you want to download? (songs are split by their lines)").split("\n")
download_songs(songs)
