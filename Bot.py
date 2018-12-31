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
        videoUrl = f'https://www.youtube.com/watch?v={videoId}'
        likeButtonLocator = 'ytd-toggle-button-renderer #button.ytd-toggle-button-renderer'
        likeButtonWrapperLocator = 'yt-icon-button#button.style-scope.ytd-toggle-button-renderer'

        self.driver.get(videoUrl)

        try:
            likeButton = WebDriverWait(self.driver, 10) \
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR, likeButtonLocator)))
            likeButtonWrapper = self.driver.find_element_by_css_selector(
                likeButtonWrapperLocator)

            # aria-pressed attribute is of type string, not boolean
            liked = likeButtonWrapper.get_attribute('aria-pressed') == 'true'

            if (not liked):
                likeButton.click()

            if watchFullVideo:
                # TODO: integrate youtube api v3 to get video duration
                WebDriverWait(self.driver, 10)

        except TimeoutException:
            print(f'Error: video with id {videoId} doesn\'t exist!')

        return self

    def subscribe(self, channelId):
        channelUrl = f'{YOUTUBE_ADDRESS}/channel/{channelId}'
        subscribeButtonLocator = (By.TAG_NAME, 'ytd-subscribe-button-renderer')

        self.driver.get(channelUrl)

        try:
            subscribeButton = WebDriverWait(self.driver, 10) \
                .until(EC.presence_of_element_located(subscribeButtonLocator))
            subscribeButton.click()
        except TimeoutException:
            print('Error: channel doesn\'t exist!')

        return self

    def login(self, email, password):
        loginButtonLocator = 'ytd-button-renderer.style-blue-text[is-paper-button]'
        emailInputLocator = 'identifier'
        passwordInputLocator = (By.NAME, 'password')
        userProfileLocator = (By.TAG_NAME, 'ytd-topbar-menu-button-renderer')

        # go to login page
        loginButton = self.driver.find_element_by_css_selector(
            loginButtonLocator)
        loginButton.click()

        emailInput = self.driver.find_element_by_name(emailInputLocator)
        emailInput.send_keys(email, Keys.RETURN)

        try:
            # wait until 'password' element is interactable
            passwordInput = WebDriverWait(self.driver, 10) \
                .until(EC.element_to_be_clickable(passwordInputLocator))

            passwordInput.send_keys(password, Keys.RETURN)

            # wait until redirect ends so that you can see your profile image on right top corner
            WebDriverWait(self.driver, 10) \
                .until(EC.presence_of_element_located(userProfileLocator))
        except TimeoutException:
            print('Error: wrong email or password!')

        return self

    def end(self):
        self.driver.close()
