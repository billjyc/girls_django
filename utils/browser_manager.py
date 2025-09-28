import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)

class WeiboBrowserManager:
    def __init__(self):
        self.driver = None
        self.cookies = ""
        self.user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0"

    def init_browser(self):
        """初始化无头浏览器并获取Cookie"""
        if self.driver is not None:
            return True

        try:
            # 配置无头浏览器选项[2,3](@ref)
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"user-agent={self.user_agent}")
            chrome_options.add_argument("--window-size=1920,1080")

            # 启动浏览器[1,4](@ref)
            self.driver = webdriver.Chrome(options=chrome_options)

            # 访问微博主页获取基础Cookie
            self.driver.get("https://weibo.com")
            time.sleep(3)

            # 获取Cookie并转换为requests可用的格式[4](@ref)
            selenium_cookies = self.driver.get_cookies()
            cookie_dict = {}
            for cookie in selenium_cookies:
                cookie_dict[cookie['name']] = cookie['value']

            self.cookies = '; '.join([f"{name}={value}" for name, value in cookie_dict.items()])
            logger.info(f"浏览器初始化成功，获取到 {len(selenium_cookies)} 个Cookie")
            return True

        except Exception as e:
            logger.error(f"浏览器初始化失败: {e}")
            if self.driver:
                self.driver.quit()
                self.driver = None
            return False

    def close(self):
        """关闭浏览器释放资源"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("浏览器已关闭")


browser_manager = WeiboBrowserManager()