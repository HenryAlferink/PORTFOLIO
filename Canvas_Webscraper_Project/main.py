from SeleniumWrapper.Driver import Driver
from CanvasPages.Login import login, two_way_authentication
from CanvasPages.Navigation import get_courses_list

__author__ = "Henry Alferink"
__date__ = "2021"

if __name__ == "__main__":
    Driver.create_new_driver("https://canvas.auckland.ac.nz/")

    login()
    two_way_authentication()
    Driver.get("https://canvas.auckland.ac.nz/courses")
    get_courses_list()
