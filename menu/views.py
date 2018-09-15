from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import MenuForm, ItemForm
from .models import Menu, Item


def menu_list(request):
    all_menus = Menu.objects.filter(
        Q(expiration_date__isnull=True) | Q(expiration_date__gte=timezone.now())).prefetch_related('items')

    menus = sorted(all_menus, key=attrgetter('created_date'))
    return render(request, 'menu/menu_list.html', {'menus': menus})


def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/item_detail.html', {'item': item})


@login_required
def create_edit_menu(request, pk=None):
    if pk:
        title = 'Change Menu'
    else:
        title = 'Add Menu'

    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            form.save_m2m()

            return redirect('menu_detail', pk=menu.pk)
    else:
        try:
            menu = Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            menu = None
        form = MenuForm(instance=menu)
    return render(request, 'menu/menu_edit.html', {'form': form, 'title': title})


def item_list(request):
    all_items = Item.objects.all()
    items = sorted(all_items, key=attrgetter('created_date'))
    return render(request, 'menu/item_list.html', {'items': items})


@login_required
def create_edit_item(request, pk=None):
    if pk:
        title = 'Update Item'
    else:
        title = 'Add Item'

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_date = timezone.now()
            item.save()
            item.save_m2m()

            return redirect('item_detail', pk=item.pk)
    else:
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            item = None
        form = ItemForm(instance=item)
    return render(request, 'menu/item_edit.html', {'form': form, 'title': title})
