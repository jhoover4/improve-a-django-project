import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.test import TestCase
from django.utils import timezone

from menu.forms import MenuForm, ItemForm, ValidationError, date_after_today_validator
from menu.models import Menu, Item, Ingredient


class MenuTestCase(TestCase):
    def setUp(self):
        self.test_menu = Menu.objects.create(season='fall')
        self.test_user = User.objects.create_user(id='1', username='root', email='root@email.com', password='root')

    def test_menus_created_date(self):
        date_string = '%m/%d/%Y'
        test_date = datetime.datetime.strftime(self.test_menu.created_date, date_string)
        today_date = datetime.datetime.strftime(datetime.datetime.today(), date_string)

        self.assertEqual(test_date, today_date)

    def test_menu_name(self):
        self.assertEqual(str(self.test_menu), 'fall')

    def test_menu_list_view(self):
        menus = Menu.objects.filter(
            Q(expiration_date__isnull=True) | Q(expiration_date__gte=timezone.now())).prefetch_related('items')

        resp = self.client.get(reverse('menu_list'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(list(menus), list(resp.context['menus']))
        self.assertTemplateUsed(resp, 'menu/menu_list.html')

    def test_menu_detail_view(self):
        resp = self.client.get(
            reverse('menu_detail', kwargs={'pk': self.test_menu.pk})
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.test_menu, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_create_menu_view(self):
        self.client.login(username='root', password='root')
        resp = self.client.get(reverse('menu_create'))

        self.assertEqual('Add Menu', resp.context['title'])
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')

    def test_edit_menu_view(self):
        self.client.login(username='root', password='root')
        resp = self.client.get(
            reverse('menu_edit', kwargs={'pk': self.test_menu.pk})
        )

        self.assertTemplateUsed(resp, 'menu/menu_edit.html')
        self.assertEqual('Change Menu', resp.context['title'])

    def test_menu_form(self):
        test_item = Item.objects.create(name='test_item',
                                        description='Filler',
                                        chef=self.test_user
                                        )

        form_data = {'season': 'something specific',
                     'expiration_date': '01/01/2020',
                     'items': [test_item.id]
                     }
        form = MenuForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_menu_form_expiration_date(self):
        past_date = datetime.date.today() - datetime.timedelta(1)
        self.assertRaises(ValidationError, date_after_today_validator, past_date)


class ItemTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(id='1', username='root', email='root@email.com', password='root')
        self.test_item = Item.objects.create(name='test_item',
                                             description='Filler',
                                             chef=self.test_user
                                             )

    def test_item_name(self):
        self.assertEqual(str(self.test_item), 'test_item')

    def test_item_list_view(self):
        items = Item.objects.all()

        resp = self.client.get(reverse('item_list'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(list(items), list(resp.context['items']))
        self.assertTemplateUsed(resp, 'menu/item_list.html')

    def test_item_detail_view(self):
        resp = self.client.get(
            reverse('item_detail', kwargs={'pk': self.test_item.pk})
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.test_item, resp.context['item'])
        self.assertTemplateUsed(resp, 'menu/item_detail.html')

    def test_create_item_view(self):
        self.client.login(username='root', password='root')
        resp = self.client.get(reverse('item_create'))

        self.assertEqual('Add Item', resp.context['title'])
        self.assertTemplateUsed(resp, 'menu/item_edit.html')

    def test_edit_item_view(self):
        self.client.login(username='root', password='root')
        resp = self.client.get(
            reverse('item_edit', kwargs={'pk': self.test_item.pk})
        )

        self.assertTemplateUsed(resp, 'menu/item_edit.html')
        self.assertEqual('Update Item', resp.context['title'])

    def test_item_form(self):
        test_ingredients = [Ingredient.objects.create(name='chocolate').id, Ingredient.objects.create(name='cherry').id]

        form_data = {'name': 'test_item2',
                     'description': 'Description is longer than 10 characters',
                     'chef': self.test_user.id,
                     'ingredients': test_ingredients
                     }
        form = ItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_item_form_description(self):
        """Description field should raise error if less than 10 characters."""

        test_ingredients = [Ingredient.objects.create(name='chocolate').id, Ingredient.objects.create(name='cherry').id]

        form_data = {'name': 'test_item2',
                     'description': 'Short',
                     'chef': self.test_user.id,
                     'ingredients': test_ingredients
                     }
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['description'].errors[0],
            'Description must be at least 10 characters.'
        )

    def test_item_form_ingredients(self):
        """Ingredients field should raise error if there are fewer than 2."""

        test_ingredients = [Ingredient.objects.create(name='chocolate').id]

        form_data = {'name': 'test_item2',
                     'description': 'Description is longer than 10 characters',
                     'chef': self.test_user.id,
                     'ingredients': test_ingredients
                     }
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['ingredients'].errors[0],
            'An item must have at least two ingredients.'
        )


class IngredientTestCase(TestCase):
    def setUp(self):
        self.test_ingredient = Ingredient.objects.create(name='test_ingredient')

    def test_item_name(self):
        self.assertEqual(str(self.test_ingredient), 'test_ingredient')

    def test_ingredient_name(self):
        self.assertEqual(self.test_ingredient.name, 'test_ingredient')
