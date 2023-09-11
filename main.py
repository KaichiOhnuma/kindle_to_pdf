"convert kindle books to a pdf file by using screenshot"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from PIL import Image
from tqdm import tqdm
import time
import os
import img2pdf
import glob

class Kindle_to_pdf(object):
    def __init__(self, email, password, book_title, page_count, output_file_name, crop_require=False):
        self.email = email
        self.password = password
        self.book_title = book_title
        self.page_count = page_count
        self.output_file_name = output_file_name
        self.crop_require = crop_require

    def open_kindle(self):
        # init driver
        options = Options()
        options.add_experimental_option("detach", True)

        # open a browser
        self.browser = webdriver.Chrome("C:/Program Files/Google/Chrome/chromedriver-win64/chromedriver.exe", options=options)
        self.browser.maximize_window()

        # open Kindle
        self.browser.get("https://read.amazon.co.jp/landing")

    def main(self):
        self.open_kindle()
        self.sign_in()
        self.open_the_book()
        self.take_screenshot()
        if self.crop_require:
            self.crop_img()
        self.imgs_to_pdf()

    def sign_in(self):
        # open the sign-in page
        sign_in_button = self.browser.find_element_by_id("top-sign-in-btn")
        sign_in_button.click()

        # sign in
        email_input = self.browser.find_element_by_id("ap_email")
        email_input.send_keys(self.email)
        password_input = self.browser.find_element_by_id("ap_password")
        password_input.send_keys(self.password)
        sign_in_confirm_button = self.browser.find_element_by_id("signInSubmit")
        sign_in_confirm_button.click()

        # load the new page
        time.sleep(2)

    def open_the_book(self):
        # get all book elements
        elements = self.browser.find_elements_by_xpath("//div[@id='library']//ul[@id='cover']//p[@class='_2czmS0An9GDlVR9xgpCNOC']")

        # find target book
        for e in elements:
            if e.text == self.book_title:
                e.click()
                return
            elif self.book_title in e.text:
                possible_target = e
        possible_target.click()

        time.sleep(5)

    def take_screenshot(self):
        # switch main window
        for window_handle in self.browser.window_handles:
            if window_handle != self.browser.current_window_handle:
                self.browser.switch_to.window(window_handle)
                break

        # move to first page
        action_left = webdriver.ActionChains(self.browser)
        action_left.key_down(Keys.LEFT)
        for i in range(self.page_count):
            action_left.perform()
            time.sleep(1)

        # init the output folder
        os.mkdir(f"./data/{self.output_file_name}")

        # take screenshot
        action_right = webdriver.ActionChains(self.browser)
        action_right.key_down(Keys.RIGHT)
        for i in range(self.page_count):
            time.sleep(1)
            self.browser.get_screenshot_as_file(f"./data/{self.output_file_name}/{i}.png")
            action_right.perform()   

    def crop_img(self):
        for file in glob.glob(f"./data/{self.output_file_name}/*.png"):
            img = Image.open(file)
            img = img.crop((img.width*0.1, img.height*0.05, img.width*0.9, img.height*0.905))
            img.save(file, quality=95)

    def imgs_to_pdf(self):
        # get list of imgs
        imgs = []
        for i in tqdm(range(self.page_count)):
            img = glob.glob(f"./data/{output_file_name}/{i}.png")
            if img:
                imgs.append(img[0])
            else:
                break
        
        # convert to pdf
        with open(f"./data/{output_file_name}/{output_file_name}.pdf", "wb") as f:
            f.write(img2pdf.convert(imgs))

if __name__ == "__main__":
    email = input("email: ")
    password = input("password: ")

    book_title = "The Hunger Game"
    page_count = 300
    output_file_name = "hunger_game_1"
    crop_require = True

    executer = Kindle_to_pdf(email, password, book_title, page_count, output_file_name, crop_require)
    executer.main()
    # executer.crop_img()
    # executer.imgs_to_pdf()