"""Create interactive objects that correspond to elements on a webpage.
"""

from selenium import webdriver
from .Driver import Driver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class NoElementFound(Exception):
    pass


class MultipleElementsFound(Exception):
    pass


def get(by, locator, webelement=None, check_for_driver=True):
    """
    if a webelement object is passed to webelement, only the
    children of this element will be searched.
    """
    if webelement:
        if type(webelement) == webdriver.remote.webdriver.WebElement:
            elements = webelement.find_elements(by, locator)
        else:
            raise Exception("webelement is not a PageElement object")
    else:
        elements = Driver.active_driver.find_elements(by, locator)

    if len(elements) == 0:
        raise NoElementFound("No elements found.")
    if len(elements) == 1:
        return PageElement(elements[0])
    else:
        return PageElements(elements)


class PageElement:
    """An object that interfaces one web element.

    Attributes:
        __by : str
        __locator : str
        element, elements
            These attributes store the element or elements found.
            Initially they are both set to None. If only one element is
            found, the element variable will store it. Else, the elements
            variable will be a list of
    """

    def __init__(self, first_arg, locator=None):
        """There are two ways to call this class. If the first argument is
        a str object, the get() function will be called and the resulting
        object that is found (if any) will be assigned as an instance variable.
        The first argument is a webdriver.remote.webdriver.WebElement object,
        this WebElement will be directly assigned as an instance variable.
        """
        if type(first_arg) == str:
            if not locator:
                raise Exception("Please supply a valid locator.")
            element = get(first_arg, locator).element
            if type(element) == PageElements:
                raise MultipleElementsFound()
        elif type(first_arg) == webdriver.remote.webdriver.WebElement:
            element = first_arg

        self.element = element

    def get_child(self, by, locator):
        """Searches for webelement that is a child of the current element.
        Returns the new element as a new object.
        """
        if by == "xpath":
            locator = "." + locator
        child = get(by, locator, webelement=self.element)

        if type(child) == PageElement:
            return child
        else:
            raise MultipleElementsFound

    def get_children(self, by, locator):
        """Searches for webelements that are children of the current element.
        Returns the elements as a PageElements object.

        If by == "xpath", then this function adds "." to the start of the
        locator string. This makes it so that it doesn't search the entire
        html document; rather it just searches the children of the current
        element like we want it to. If by is "xpath", then the locator string
        should probably start with "//" instead of ".//" now (because we
        already add the "." in the function here.)
        """
        if by == "xpath":
            locator = "." + locator
        children = get(by, locator, webelement=self.element)
        if type(children) == PageElements:
            return children
        else:
            raise Exception("Only one or no elements found.")

    def get_element_recursive(self, by_list, locator_list):
        """Starts off with a new webelement based on the first entries in by_list
        and locator_list and then runs get_child_element recursively. by_list
        and locator_list are lists that contain corresponding "by" and
        "locator" arguments (i.e. at the same index) for the
        get_child_element() function.
        """
        n = len(by_list)

        if type(by_list) != list or type(locator_list) != list:
            raise Exception("Input arguments must be lists.")
        if n != len(locator_list):
            raise Exception("Length of input lists do not match.")

        new_element = PageElement(by_list[0], locator_list[0])
        for i in range(1, n):
            new_element = new_element.get_child_element(
                                             by_list[0], locator_list[0])
        return new_element

    def get_outer_html(self):
        """Returns the element HTML as well as all the inner HTML."""
        return self.element.get_attribute("outerHTML")

    def get_inner_html(self):
        """Returns only the inner HTML."""
        return self.element.get_attribute("innerHTML")

    def get_text(self, method=0):
        """Returns HTML text. Two method presented here. Try the other one
        if the first doesn't work.
        """
        if method == 0:
            return self.element.get_attribute("textContent")
        elif method == 1:
            return self.element.text
        else:
            raise Exception

    def get_element_html(self):
        """Return the html element text. That is, return the 'outerHTML'
        setminus the 'innerHTML'. That is, the part surrounded by '<' and
        '>'.
        """
        outer = self.get_outer_html()
        return outer.split('>', maxsplit=1)[0] + '>'

    def get_attribute(self, attribute):
        return self.element.get_attribute(attribute)

    def clear(self):
        self.element.clear()
        return self

    def send_keys(self, text):
        self.element.send_keys(text)
        return self

    def click(self):
        """See also click_through_to_new_page()."""
        self.element.click()
        Driver._fill_attributes()  # refresh webdriver
        return self

    def click_through_to_new_page(self, timeout=10):
        """Use this method instead of click() when you expect the click will
        send you through to a new page. This method will wait until
        the new page has sufficiently loaded (?) before proceeding code
        is executed. Returns Driver object.
        """
        old_page = Driver.current_html_page_element
        self.click()
        WebDriverWait(Driver.active_driver, timeout).until(
            expected_conditions.staleness_of(old_page))
        Driver._fill_attributes()  # refresh webdriver
        return Driver


class PageElements:
    """An object that stores a list of PageElement objects.

    If the first argument is a string and the locator argument is
    alse supplied, then the get() function will be called.

    If the first argument is a list containing either PageElement
    objects or webdriver.remote.webdriver.WebElement objects, the
    PageElements object will be created from these.
    """
    def __init__(self, firstarg, locator=None):
        if isinstance(firstarg, str):
            if not locator:
                raise Exception("Please supply a valid locator.")

            elements = get(firstarg, locator).get_element_list()

        elif isinstance(firstarg, list):
            elements = []
            for element in firstarg:
                if isinstance(element, PageElement):
                    elements.append(element)
                elif isinstance(
                        element, webdriver.remote.webdriver.WebElement):
                    elements.append(PageElement(element))
                else:
                    raise Exception(
                        "List contains invalid type(s).")

        self._elements = elements

    def get_element_list(self):
        return self._elements

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        """Returns iter object."""
        self.n = len(self)
        self.i = 0
        return self

    def __next__(self):
        if self.i < self.n:
            element = self._elements[self.i]
            self.i += 1
            return element
        else:
            raise StopIteration

    def __getitem__(self, key):
        if isinstance(key, slice) or isinstance(key, int):
            return self._elements[key]
        else:
            raise TypeError("Key must be of type int of slice.")
