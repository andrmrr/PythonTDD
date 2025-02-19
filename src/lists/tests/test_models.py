from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from lists.models import Item, List

class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        mylist = List()
        mylist.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = mylist
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = mylist
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(saved_list, mylist)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_item_saved = saved_items[0]
        second_item_saved = saved_items[1]
        self.assertEqual(first_item_saved.text, "The first (ever) list item")
        self.assertEqual(first_item_saved.list, mylist)
        self.assertEqual(second_item_saved.text, "Item the second")
        self.assertEqual(second_item_saved.list, mylist)

    def test_cannot_save_empty_list_items(self):
        myList = List.objects.create()
        item = Item(list=myList, text="")
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_cannot_save_null_list_items(self):
        myList = List.objects.create()
        item = Item(list=myList, text=None)
        with self.assertRaises(IntegrityError):
            item.save()

    def test_get_absolute_url(self):
        mylist = List.objects.create()
        self.assertEqual(mylist.get_absolute_url(), f"/lists/{mylist.id}/")
