from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

MAX_WAIT = 5


class LayoutAndStylingTest(FunctionalTest): 
    def test_layout_and_styling(self):
        # Edith goes to the homepage
        self.browser.get(self.live_server_url)

        # Her browser window is set to a very specific size
        self.browser.set_window_size(1024, 768)

        # She notices that the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10
        )

        # She starts a new list and notices that the input is nicely centered there too
        self.add_list_item("testing")
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10
        )
