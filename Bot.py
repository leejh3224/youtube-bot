from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

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

    def like(self, videoId, watchFullVideo=False):
        """
        Html structure looks like below:
        yt-icon-button (aria-pressed)
            > button (aria-label)

        so first get all yt-icon-button tags,
        and then identify 'like' button by looking at aria-label text.
        """
        self.driver.get(f'https://www.youtube.com/watch?v={videoId}')

        try:
            buttons = WebDriverWait(self.driver, 10) \
                .until(EC.presence_of_all_elements_located((By.TAG_NAME, 'yt-icon-button')))

            for button in buttons:
                # html attributes are treated as string, not boolean
                liked = button.get_attribute('aria-pressed') == 'true'
                icon_button, = button.find_elements_by_css_selector(
                    '.yt-icon-button')
                label = icon_button.get_attribute('aria-label')

                # check button is like button '좋아함' == 'like' in korean
                # not able to invent better solution than comparing the text in button label
                if label and ('좋아함' in label) and not liked:
                    button.click()
                    break

            if watchFullVideo:
                # TODO: integrate youtube api v3
                WebDriverWait(self.driver, 10)

        except TimeoutException:
            print(f'Error: video with id {videoId} doesn\'t exist!')

        return self

    def subscribe(self, channelId):
        self.driver.get(f'{YOUTUBE_ADDRESS}/channel/{channelId}')

        try:
            subscribeButton = WebDriverWait(self.driver, 10) \
                .until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-subscribe-button-renderer')))
            subscribeButton.click()
        except TimeoutException:
            print('Error: channel doesn\'t exist!')

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
        except TimeoutException:
            print('Error: wrong email or password!')

        return self

    def end(self):
        self.driver.close()
