from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from .list_page import ListPage

MAX_WAIT = 5

class NewVisitorTest(FunctionalTest):
    def test_can_start_a_todo_list(self):
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        inputbox = list_page.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # She writes "Buy peacock feathers" in a text box
        # (Edith's hobby is tying fly-fishing lures)
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        list_page.add_list_item("Buy peacock feathers")

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly " (Edith is very methodical)
        list_page.add_list_item("Use peacock feathers to make a fly")

        # The page updates again and now shows both items on her list
        list_page.wait_for_row_in_list_table("Buy peacock feathers", 1)
        list_page.wait_for_row_in_list_table("Use peacock feathers to make a fly", 2)

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.add_list_item("Buy peacock feathers")

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Now a new user, Francis, comes along to the site.

        ## We delete all the browser's cookies
        ## as a way of simulating a brand new user session
        ## Double hashtag comments are for whys (single are for the user story)
        self.browser.delete_all_cookies()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # Francis starts a new list by entering a new item.
        # He is less interesting than Edith...
        list_page.add_list_item("Buy milk")

        # Francis gets his own URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        # Satisfied, they both go back to sleep
