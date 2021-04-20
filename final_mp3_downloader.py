from pyperclip import paste
from selenium.webdriver.chrome.options import Options
from config import *
from selenium import webdriver
from time import sleep
from os import path

# youtube video title //*[@id="container"]/h1/yt-formatted-string

song_link = paste()

if "https://www.youtube.com/watch?v=" in song_link:
    self_total_path = path.dirname(path.abspath(__file__))
    downloads_folder = "\\".join(self_total_path.split("\\")[:-2])+"\\Downloads"

    print("Setting up chrome driver...")
    # this is to make sure that the tab that is opened doesn't have any audio that can distract
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")
    chrome_options.headless = True
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # i want to minimize at startup, turns out you can't

    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("--disable-extensions")
    option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
    option.add_argument("--mute-audio")
    option.add_argument("--silent-launch")

    option.headless = True
    option.add_argument("--disable-gpu")
    option.add_argument("--no-sandbox")

    # this makes the driver that pretty mcuh runs everything
    driver = webdriver.Chrome(chrome_driver_path, options=option, chrome_options=chrome_options)
    # driver.minimize_window()

    params = {"behavior": "allow", "downloadPath": downloads_folder}
    driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
    # opens the link
    driver.get(song_link)

    print("Opening up YouTube...")
    # waits until the song title shows up and then sets song_name equal to it
    driver.implicitly_wait(5)
    song_name = driver.find_element_by_xpath("//*[@id=\"container\"]/h1/yt-formatted-string").text
    print("SONG FOUND: \nsong name: ", song_name)
    for x in range(tries):
        print(f"\n__________Repeat no. {x}__________")
        if x > repeats_before_shortening:
            song_name = " ".join(song_name.split()[:-1])
            print(f"Max repeat amount ({repeats_before_shortening}) reached.\n"
                  f"Shortening song name to \"{repeats_before_shortening}\"")
            repeats_before_shortening *= 2
        try:
            print("Opening \"https://wwww.mp3juices.cc\"...")
            driver.get("https://www.mp3juices.cc/")
            # driver.minimize_window()
            # get_to_first_tab()

            print(f"Searching up \"{song_name}\"...")
            driver.find_element_by_xpath("//*[@id=\"query\"]").send_keys(song_name)
            sleep(1.5)
            driver.find_element_by_xpath("//*[@id=\"button\"]").click()
            sleep(1.5)

            print("Clicking download button...")
            driver.find_element_by_xpath("//*[@id=\"result_1\"]/div[3]").click()
            driver.implicitly_wait(20)
            driver.find_element_by_xpath("//*[@id=\"download_1\"]/div[3]/a[1]").click()

            print("Commencing song download...")
            song_download_name = driver.find_element_by_xpath('//*[@id="download_1"]/div[1]').text
            # sleep(0.01)
            # driver.minimize_window()
            # sleep(0.01)
            # driver.minimize_window()
            # print(song, "finished")

            break
        except:
            pass
    try:
        print("Exit while loop...")
        # repeats 240 times (default) (so max is one hour), and checks if the last file downloaded exists,
        # if not then it will keep on waiting
        sleep(5)
        for x in range(file_checks_amount*4):
            # print(f"repeat: {repeats}")
            print("Checking if file exists...")
            if path.exists(f"{downloads_folder}\\{song_download_name}.mp3"):
                break
            print("ERROR: File not found. Waiting 15 seconds to check again...")
            sleep(15)

        print("DONE")
        driver.quit()
    except NameError:
        print("Error downloading. Try again.")
