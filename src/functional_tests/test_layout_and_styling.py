from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from .list_page import ListPage

MAX_WAIT = 5


class LayoutAndStylingTest(FunctionalTest): 
    def test_layout_and_styling(self):
        # Edith goes to the homepage
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)

        # Her browser window is set to a very specific size
        list_page.set_window_size(1024, 768)

        # She notices that the input box is nicely centered
        inputbox = list_page.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10
        )

        # She starts a new list and notices that the input is nicely centered there too
        list_page.add_list_item("testing")
        inputbox = list_page.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10
        )

    def test_row_orientation_for_list_sharing_elements(self):
        # Edith logs in to her account
        self.create_pre_authenticated_session("edith@example.com")

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item("Get help")

        # She notices a "Share this list" option
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute("placeholder"), "your-friend@example.com"
        )

        # And also notices the list owner's name, which is her
        self.assertEqual("edith@example.com", list_page.get_list_owner())

        # The list owner element is to the left of the "Share this list" option
        list_owner_element = self.browser.find_element(By.ID, "id_list_owner")
        self.assertLess(list_owner_element.location["x"], share_box.location["x"])
