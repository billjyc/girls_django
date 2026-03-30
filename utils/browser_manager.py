import logging
import time
from enum import Enum
from typing import Optional, Dict, Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

logger = logging.getLogger("django")


class BrowserType(Enum):
    """浏览器类型枚举"""
    CHROME = "chrome"
    FIREFOX = "firefox"
    # 可选：未来支持更多浏览器
    # EDGE = "edge"
    # SAFARI = "safari"


class WeiboBrowserManager:
    def __init__(
            self,
            browser_type: str = "firefox",  # 默认使用 Firefox
            headless: bool = True,  # 默认无头模式
            window_size: tuple = (1920, 1080),  # 窗口大小
            user_agent: Optional[str] = None,
            driver_path: Optional[str] = None
    ):
        """
        初始化浏览器管理器

        Args:
            browser_type: 浏览器类型，可选 "chrome" 或 "firefox"
            headless: 是否使用无头模式
            window_size: 浏览器窗口大小 (宽度, 高度)
            user_agent: 自定义 User-Agent
            driver_path: 驱动路径，如果为 None 则自动查找
        """
        self.driver = None
        self.cookies = ""
        self.browser_type = self._validate_browser_type(browser_type.lower())
        self.headless = headless
        self.window_size = window_size
        self.user_agent = user_agent or self._get_default_user_agent()
        self.driver_path = driver_path

    def _validate_browser_type(self, browser_type: str) -> BrowserType:
        """验证浏览器类型"""
        try:
            return BrowserType(browser_type)
        except ValueError:
            valid_types = [bt.value for bt in BrowserType]
            logger.warning(f"不支持的浏览器类型: {browser_type}, 使用默认值: firefox")
            return BrowserType.FIREFOX

    def _get_default_user_agent(self) -> str:
        """获取默认 User-Agent"""
        if self.browser_type == BrowserType.CHROME:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        else:  # Firefox
            return "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0"

    def _get_default_driver_path(self) -> Optional[str]:
        """获取默认驱动路径"""
        if self.browser_type == BrowserType.CHROME:
            # Chrome 驱动常见路径
            possible_paths = [
                "/usr/local/bin/chromedriver",
                "/usr/bin/chromedriver",
                "/snap/bin/chromedriver",
                "/opt/homebrew/bin/chromedriver",  # macOS
                "./chromedriver"  # 当前目录
            ]
        else:  # Firefox
            # Firefox 驱动常见路径
            possible_paths = [
                #"/usr/local/bin/geckodriver",
                #"/usr/bin/geckodriver",
                "/snap/bin/geckodriver",
                #"/opt/homebrew/bin/geckodriver",  # macOS
                #"./geckodriver"  # 当前目录
            ]

        for path in possible_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path

        logger.warning(f"未找到 {self.browser_type.value} 驱动，将尝试自动查找")
        return None

    def _create_chrome_driver(self) -> webdriver.Chrome:
        """创建 Chrome 驱动"""
        chrome_options = ChromeOptions()

        # 无头模式
        if self.headless:
            chrome_options.add_argument("--headless")

        # 无沙箱模式（Linux 环境常用）
        chrome_options.add_argument("--no-sandbox")

        # 禁用共享内存（Docker 环境常用）
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('--proxy-auto-detect')

        # 用户代理
        # chrome_options.add_argument(f"user-agent={self.user_agent}")

        # 窗口大小
        chrome_options.add_argument(f"--window-size={self.window_size[0]},{self.window_size[1]}")

        # 其他优化参数
        #chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        #chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.binary_location = r"/Users/yjia7/Downloads/APP/Google Chrome Beta.app"

        # 创建服务
        driver_path = self.driver_path or self._get_default_driver_path()
        if driver_path:
            #service = ChromeService(executable_path=driver_path)
            #driver = webdriver.Chrome(service=service, options=chrome_options)
            driver = webdriver.Chrome(options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)

        # 执行 Chrome DevTools 命令
        # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.user_agent})

        return driver

    def _create_firefox_driver(self) -> webdriver.Firefox:
        """创建 Firefox 驱动"""
        firefox_options = FirefoxOptions()

        # 无头模式
        if self.headless:
            firefox_options.add_argument("--headless")

        # 设置用户代理
        firefox_options.set_preference("general.useragent.override", self.user_agent)

        # 创建服务
        driver_path = self.driver_path or self._get_default_driver_path()

        if driver_path:
            service = FirefoxService(executable_path=driver_path)
            driver = webdriver.Firefox(service=service, options=firefox_options)
        else:
            driver = webdriver.Firefox(options=firefox_options)

        # 设置窗口大小
        driver.set_window_size(self.window_size[0], self.window_size[1])

        return driver

    def init_browser(self, retry_times: int = 2) -> bool:
        """初始化浏览器并获取 Cookie"""
        if self.driver is not None:
            logger.info("浏览器已初始化，无需重复初始化")
            return True

        for attempt in range(1, retry_times + 1):
            try:
                logger.info(f"正在初始化 {self.browser_type.value} 浏览器 (尝试 {attempt}/{retry_times})...")

                # 根据浏览器类型创建驱动
                if self.browser_type == BrowserType.CHROME:
                    self.driver = self._create_chrome_driver()
                else:  # Firefox
                    self.driver = self._create_firefox_driver()

                # 设置隐式等待
                self.driver.implicitly_wait(5)

                # 访问微博主页获取基础 Cookie
                logger.info(f"正在访问微博主页...")
                self.driver.get("https://weibo.com")
                time.sleep(5)  # 等待页面加载

                # 获取当前 URL，确认是否成功加载
                current_url = self.driver.current_url
                logger.info(f"当前页面URL: {current_url}")

                # 获取 Cookie
                selenium_cookies = self.driver.get_cookies()
                cookie_dict = {}
                for cookie in selenium_cookies:
                    cookie_dict[cookie['name']] = cookie['value']

                if not cookie_dict:
                    logger.warning("未获取到任何 Cookie")
                    if attempt < retry_times:
                        self.close()
                        continue
                    else:
                        return False

                self.cookies = '; '.join([f"{name}={value}" for name, value in cookie_dict.items()])
                logger.info(f"{self.browser_type.value} 浏览器初始化成功，获取到 {len(selenium_cookies)} 个 Cookie")

                # 验证浏览器是否正常工作
                try:
                    # 尝试执行简单的 JavaScript
                    title = self.driver.execute_script("return document.title;")
                    logger.info(f"页面标题: {title}")
                except Exception as e:
                    logger.warning(f"浏览器 JavaScript 执行测试失败: {e}")

                return True

            except Exception as e:
                logger.error(f"浏览器初始化失败 (尝试 {attempt}/{retry_times}): {e}")
                import traceback
                logger.error(traceback.format_exc())

                # 清理资源
                if self.driver:
                    self.driver.quit()
                    self.driver = None

                if attempt < retry_times:
                    logger.info(f"等待 2 秒后重试...")
                    time.sleep(2)
                else:
                    logger.error(f"浏览器初始化失败，已达到最大重试次数 {retry_times}")
                    return False

        return False

    def get_driver_info(self) -> Dict[str, Any]:
        """获取浏览器和驱动信息"""
        if not self.driver:
            return {"status": "not_initialized"}

        try:
            info = {
                "status": "running",
                "browser": self.browser_type.value,
                "headless": self.headless,
                "window_size": self.window_size,
                "page_title": self.driver.title,
                "current_url": self.driver.current_url,
                "session_id": self.driver.session_id,
                "cookie_count": len(self.cookies.split('; ')) if self.cookies else 0
            }
            return info
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def close(self):
        """关闭浏览器释放资源"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                logger.info(f"{self.browser_type.value} 浏览器已关闭")
            except Exception as e:
                logger.error(f"关闭浏览器时出错: {e}")
                self.driver = None

    def __del__(self):
        """析构函数，确保资源释放"""
        self.close()


# 创建默认浏览器管理器实例
# 可以从环境变量或配置文件中读取配置
import os
from django.conf import settings


def create_browser_manager() -> WeiboBrowserManager:
    """创建浏览器管理器实例"""
    # 从 Django settings 或环境变量获取配置
    browser_type = getattr(settings, 'WEIBO_BROWSER_TYPE', 'firefox')
    headless = getattr(settings, 'WEIBO_BROWSER_HEADLESS', True)

    # 从环境变量读取（优先级更高）
    # browser_type = os.environ.get('WEIBO_BROWSER_TYPE', 'firefox')
    # headless_str = os.environ.get('WEIBO_BROWSER_HEADLESS', 'true')
    # headless = headless_str.lower() in ('true', '1', 'yes')

    # 驱动路径
    driver_path = os.environ.get('WEIBO_DRIVER_PATH')

    logger.info(f"创建浏览器管理器: type={browser_type}, headless={headless}")

    return WeiboBrowserManager(
        browser_type=browser_type,
        headless=headless,
        driver_path=driver_path
    )


# 全局浏览器管理器实例
browser_manager = create_browser_manager()

if __name__ == "__main__":
    browser_manager.init_browser()