"""Custom wrapper for the WebDriver object in the selenium package.

Classes:
    Driver
"""

from selenium import webdriver


__author__ = "Henry Alferink"
__date__ = "20/March/2021"


class Driver:
    """A custom wrapper for selenium.

    Class variables:
        active_driver : selenium.webdriver.chrome.webdriver.WebDriver
            variable that stores active WebDriver object to the class.
            Note that this object is a class variable and not an instance
            variable, meaning we don't need to create an instance of the
            Driver class.
        current_url :
        current_html_page_element :
            Webelement object that points to the root html element of 
            the page. This can be useful for checking whether a page has
            been left, through checking if this element has gone stale.

    Class Methods:
        get(website) -> Driver.driver
        forward() -> Driver.driver
        back() -> Driver.driver
        quit()
    """

    active_driver = None
    current_url = None
    current_html_page_element = None

    @staticmethod
    def create_new_driver(website, download_directory=None, silent=True):
        """Create and return webdriver object that points to a particular website.

        Parameters:
            website : str
                The website the driver points to.
            download_directory : str
                Location to store downloads.
            silent : bool
                If set to true the console will not output periodic info
                about the state of the driver.

        Returns:
            selenium.webdriver.chrome.webdriver.WebDriver object.
        """

        options = webdriver.ChromeOptions()
        if download_directory:
            # note that setting "safebrowsing" to false sets Chrome
            # to confirm whether you really want to download or not -
            # due to it being potentially unsafe
            prefs = {
                "download.default_directory": download_directory,
                "safebrowsing.enabled": "false"
            }
            options.add_experimental_option("prefs", prefs)
        if silent:
            # operate Selenium in silent mode with respect to the console
            options.add_argument("--log-level=3")

        Driver.active_driver = webdriver.Chrome(options=options)

        Driver.active_driver.get(website)
        Driver._fill_attributes()
        return Driver

    @staticmethod
    def _fill_attributes():
        """Fills the class attributes defined above. This method should
        be excecuted each time a new page gets loaded."""
        try:
            Driver.current_url = Driver.active_driver.current_url
            Driver.current_html_page_element = \
                Driver.active_driver.find_element_by_tag_name('html')
        except Exception:
            Driver.quit()

    @staticmethod
    def check_driver_active():
        """Checks whether driver has been initiated. If not, the
        create_new_driver() method must be used first.
        """
        if Driver.active_driver is None:
            raise Exception("Please initialize a WebDriver first "
                            "by calling Driver.create_new_driver()")

    @staticmethod
    def get(website):
        """
        Gets new website for active driver. If no driver exists,
        Driver.create_new_driver() will be called and run in silent
        mode.
        """
        Driver.check_driver_active()
        Driver.active_driver.get(website)
        Driver._fill_attributes()
        return Driver

    @staticmethod
    def back():
        """Navigate backward in the browser history."""
        Driver.active_driver.back()
        return Driver

    @staticmethod
    def forward():
        """Navigate forward in the browser history."""
        Driver.active_driver.forward()
        return Driver

    @staticmethod
    def quit():
        """Close web connection."""
        Driver.active_driver.quit()
