from selenium.webdriver.common.by import By

from .base import FunctionalTest


class MyListsTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session("edith@example.com")

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item("Reticulate splines")
        self.add_list_item("Immanentize eschaton")
        frist_list_url = self.browser.current_url

        # Sbe notices a "My lists" link, for the first time.
        self.browser.find_element(By.LINK_TEXT, "My lists").click()

        # She sees her email in there in the page heading
        self.wait_for(
            lambda: self.assertIn(
                "edith@example.com",
                self.browser.find_element(By.CSS_SELECTOR, "h1").text
            )
        )

        # And she sees that her list is in there,
        # named according to its first list item
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, "Reticulate splines")
        )
        self.browser.find_element(By.LINK_TEXT, "Reticulate splines").click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, frist_list_url))

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item("Click cows")
        second_list_url = self.browser.current_url

        # Under "my lists", her new list appears
        self.browser.find_element(By.LINK_TEXT, "My lists").click()
        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, "Click cows"))
        self.browser.find_element(By.LINK_TEXT, "Click cows").click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        # She logs out. The "My lists" option disappears
        self.browser.find_element(By.CSS_SELECTOR, "#id_logout").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.find_elements(By.LINK_TEXT, "My lists"), [])
        )