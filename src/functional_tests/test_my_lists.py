from selenium.webdriver.common.by import By

from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage

class MyListsTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session("edith@example.com")

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.add_list_item("Reticulate splines")
        list_page.add_list_item("Immanentize eschaton")
        first_list_url = self.browser.current_url

        # Sbe notices a "My lists" link, for the first time.
        # She sees her email in there in the page heading
        MyListsPage(self).go_to_my_lists_page("edith@example.com")

        # And she sees that her list is in there,
        # named according to its first list item
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, "Reticulate splines")
        )
        self.browser.find_element(By.LINK_TEXT, "Reticulate splines").click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        list_page.add_list_item("Click cows")
        second_list_url = self.browser.current_url

        # Under "my lists", her new list appears
        MyListsPage(self).go_to_my_lists_page("edith@example.com")
        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, "Click cows"))
        self.browser.find_element(By.LINK_TEXT, "Click cows").click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        # She logs out. The "My lists" option disappears
        self.browser.find_element(By.CSS_SELECTOR, "#id_logout").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.find_elements(By.LINK_TEXT, "My lists"), [])
        )