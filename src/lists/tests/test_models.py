from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from lists.models import Item, List

User = get_user_model()

class ItemModelTest(TestCase):
    def test_default_text(self):
       item = Item()
       self.assertEqual(item.text, "")

    def test_item_is_related_to_list(self):
        mylist = List.objects.create()
        item = Item()
        item.list = mylist
        item.save()
        self.assertIn(item, mylist.item_set.all())

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

    def test_duplicate_items_are_invalid(self):
        mylist = List.objects.create()
        Item.objects.create(list=mylist, text="bla")
        with self.assertRaises(ValidationError):
            item = Item(list=mylist, text="bla")
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(text="bla", list=list1)
        item = Item(text="bla", list=list2)
        item.full_clean() # should not raise

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="i1")
        item2 = Item.objects.create(list=list1, text="item 2")
        item3 = Item.objects.create(list=list1, text="3")
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_string_representation(self):
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        mylist = List.objects.create()
        self.assertEqual(mylist.get_absolute_url(), f"/lists/{mylist.id}/")

    def test_lists_can_have_owners(self):
        user = User.objects.create(email="a@b.com")
        mylist = List.objects.create(owner=user)
        self.assertIn(mylist, user.lists.all())

    def test_list_owner_is_optional(self):
        List.objects.create() # should not raise

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="first item")
        Item.objects.create(list=list_, text="second item")
        self.assertEqual(list_.name, "first item")

    def test_list_has_shared_with_add_method(self):
        list_ = List.objects.create()
        user = User.objects.create(email="a@b.com")
        list_.shared_with.add("a@b.com")
        self.assertIn(user, list_.shared_with.all())