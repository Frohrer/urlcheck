from PIL import Image
import random
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    try:
        # update_tld_names()
        argParser = argparse.ArgumentParser(description='Get screenshot of webpage.')
        argParser.add_argument('url', help='The url of the website (including http/s)')
        argParser.add_argument('filename', help='The filename of the screenshot to be')

        args = argParser.parse_args()
        print(args.url)
        print(args.filename)
        if not args.url or not args.filename:
            print('undefined input')

        photoRandom = random.randint(1,10000)
        chromeOptions = Options()
        chromeOptions.headless = True
        browser = webdriver.Chrome(executable_path="./chromedriver", options=chromeOptions)
        browser.implicitly_wait(10)
        browser.get(args.url)
        browser.set_window_size(1200,675)
        browser.save_screenshot('../tmp/'+args.filename)
        browser.quit()
    except Exception as e:
        print(e)
        exit()
    finally:
        exit()
