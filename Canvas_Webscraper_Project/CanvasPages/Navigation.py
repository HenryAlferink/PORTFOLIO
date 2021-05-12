from SeleniumWrapper.PageElement import PageElement, NoElementFound
from SeleniumWrapper.Driver import Driver
from selenium.webdriver.common.by import By


def get_courses_list():
    """Get list of all courses listed under 'Past Enrolments'
    in the 'All Courses' Canvas page
    """
    assert Driver.current_url == \
        "https://canvas.auckland.ac.nz/courses"

    # single element pointing to table
    table = PageElement(
        By.XPATH,
        "//table[@id='past_enrollments_table']/tbody"
    )

    # list of elements pointing to table entries
    table_entries = table.get_children(By.XPATH, "//tr")

    # loop through each table entry and get the title and the link. 
    for element in table_entries:
        try:
            sub_element = element.get_child(
                By.XPATH,
                "//td[contains(@class,'course-list-course-title-column')]/a")
            title = sub_element.get_attribute('title')
            link = sub_element.get_attribute('href')

        # some listed courses may not include a link:
        except NoElementFound:
            continue
