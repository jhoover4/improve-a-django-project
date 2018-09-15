from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from menu.forms import MenuForm
from menu.models import Menu, Item, Ingredient


class MenuTestCase(TestCase):
    def setUp(self):
        self.test_menu = Menu.objects.create(season='fall')

    def test_menus_created_date(self):
        date_string = '%m/%d/%Y'
        test_date = datetime.strftime(self.test_menu.created_date, date_string)
        today_date = datetime.strftime(datetime.today(), date_string)

        self.assertEqual(test_date, today_date)

    def test_menu_name(self):
        self.assertEqual(str(self.test_menu), 'fall')

    def test_menu_detail_view(self):
        resp = self.client.get(
            reverse('menu_detail', kwargs={'pk': self.test_menu.pk})
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.test_menu, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_menu_list_view(self):
        menus = Menu.objects.all()

        resp = self.client.get(reverse('menu_list'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(list(menus), list(resp.context['menus']))
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')

    def test_create_menu_view(self):
        resp = self.client.get(reverse('menu_create'))

        self.assertEqual('Add Menu', resp.context['title'])
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')

    def test_edit_menu_view(self):
        resp = self.client.get(
            reverse('menu_edit', kwargs={'pk': self.test_menu.pk})
        )

        self.assertTemplateUsed(resp, 'menu/menu_edit.html')
        self.assertEqual('Change Menu', resp.context['title'])

    def test_menu_form(self):
        self.test_user = User.objects.create_user(id='1', username='root', email='root@email.com', password='root')
        self.test_item = Item.objects.create(name='test_item',
                                             description='Filler',
                                             chef=self.test_user
                                             )

        form_data = {'season': 'something specific',
                     'expiration_date': '01/01/2020',
                     'item_select': [1]
                     }
        form = MenuForm(data=form_data)
        self.assertTrue(form.is_valid())


class ItemTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(id='1', username='root', email='root@email.com', password='root')
        self.test_item = Item.objects.create(name='test_item',
                                             description='Filler',
                                             chef=self.test_user
                                             )

    def test_item_name(self):
        self.assertEqual(str(self.test_item), 'test_item')

    def test_item_detail_view(self):
        resp = self.client.get(
            reverse('item_detail', kwargs={'pk': self.test_item.pk})
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.test_item, resp.context['item'])
        self.assertTemplateUsed(resp, 'menu/detail_item.html')


class IngredientTestCase(TestCase):
    def setUp(self):
        self.test_ingredient = Ingredient.objects.create(name='test_ingredient')

    def test_item_name(self):
        self.assertEqual(str(self.test_ingredient), 'test_ingredient')

    def test_ingredient_name(self):
        self.assertEqual(self.test_ingredient.name, 'test_ingredient')
