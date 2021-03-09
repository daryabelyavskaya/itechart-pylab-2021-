from selenium import webdriver
from selenium.webdriver import ActionChains


class RedditParser:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def scroll(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def page(self):
        return self.driver.page_source

    def close(self):
        self.driver.close()

    def driver_get_link(self, link):
        self.driver.get(link)

    def find_elements_by_id(self, str):
        return self.driver.find_elements_by_id(str)

    def find_elements_by_class_name(self, str):
        return self.driver.find_elements_by_class_name(str)

    def find_elements_by_css_selector(self, str):
        return self.driver.find_elements_by_css_selector(str)

    def find_elements_by_xpath(self, str):
        return self.driver.find_elements_by_xpath(str)

    def get_links(self, users):
        return [i.get_attribute('href') for i in users]

    def get_attributes(self, element) -> dict:
        return self.driver.execute_script(
            """
            let attr = arguments[0].attributes;
            let items = {};
            for (let i = 0; i < attr.length; i++) {
                items[attr[i].name] = attr[i].value;
            }
            return items;
            """,
            element
        )

    def new_action(self):
        return ActionChains(self.driver)
