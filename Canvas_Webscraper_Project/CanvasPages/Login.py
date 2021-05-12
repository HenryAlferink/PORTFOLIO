from SeleniumWrapper.PageElement import PageElement, NoElementFound
from SeleniumWrapper.Driver import Driver
from selenium.webdriver.common.by import By

from getpass import getpass


def login():
    while True:
        username = input("Please enter username: ")
        password = getpass("Please enter password: ")

        PageElement(By.ID, "username").clear().send_keys(username)
        PageElement(By.ID, "password").clear().send_keys(password)
        PageElement(By.ID, "_eventId_proceed").click_through_to_new_page()

        try:
            PageElement(By.XPATH, '//h4[@class="login-white" and text()\
                ="Two-factor Authentication"]')
            print("Login successful!")
            break

        except NoElementFound:
            text = (
                PageElement(By.XPATH, '//p[@class="form-error" and \
                    @role="alert"]')
                .get_text()
            )
            check_for = (
                "The combination of credentials you have entered is incorrect."
            )
            if check_for in text:
                print("Username or password incorrect. Please try again.\n")
                continue
            else:
                raise Exception("Unknown error.")


def two_way_authentication():
    # keep trying until the token you enter is correct.
    while 1:
        token = input("\nEnter Authy token: ")
        PageElement(By.ID, "token").send_keys(token)
        PageElement(By.ID, "_eventId_proceed").click_through_to_new_page()

        if Driver.current_url == "https://canvas.auckland.ac.nz/":
            print("Authentication successful!")
            break
        print("Token incorrect. Please try again.")
