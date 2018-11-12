from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

YOUTUBE_ADDRESS = 'https://www.youtube.com/'
YOUTUBE_TITLE = 'YouTube'


class Bot:
    def __init__(self, chromeDriverLocation):
        # Download chromedriver first: https://sites.google.com/a/chromium.org/chromedriver/downloads
        self.driver = webdriver.Chrome(chromeDriverLocation)

    def goto_youtube(self):
        self.driver.get(YOUTUBE_ADDRESS)
        assert YOUTUBE_TITLE in self.driver.title
        return self

    def subscribe(self, channelId):
        self.driver.get(f'{YOUTUBE_ADDRESS}/channel/{channelId}')
        subscribeButton = WebDriverWait(self.driver, 10) \
            .until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-subscribe-button-renderer')))
        subscribeButton.click()
        return self

    def login(self, email, password):
        loginButton = self.driver.find_element_by_link_text('로그인')
        loginButton.click()

        emailInput = self.driver.find_element_by_name('identifier')
        emailInput.send_keys(email, Keys.RETURN)

        try:
            # wait until 'password' element shows up
            passwordInput = WebDriverWait(self.driver, 10) \
                .until(EC.presence_of_element_located((By.NAME, 'password')))
            passwordInput.send_keys(password, Keys.RETURN)

            # wait until redirect ends so that you can see your profile image on right top corner
            WebDriverWait(self.driver, 10) \
                .until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-topbar-menu-button-renderer')))
        finally:
            return self

    def end(self):
        self.driver.close()
