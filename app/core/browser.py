import os
from django.conf import settings
from selenium import webdriver

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
WINDOW_SIZE = "1200x1000"


class Browser(webdriver.Chrome):
    timeout = 15

    def __init__(self):
        path_bin = str(settings.BASE_DIR / 'bin')
        if path_bin not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + path_bin
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={USER_AGENT}")
        chrome_options.add_argument(f"window-size={WINDOW_SIZE}")
        super().__init__(chrome_options=chrome_options)
