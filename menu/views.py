from datetime import datetime
from operator import attrgetter

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import MenuForm
from .models import Menu, Item


def menu_list(request):
    all_menus = Menu.objects.filter(
        Q(expiration_date__isnull=True) | Q(expiration_date__gte=timezone.now())).prefetch_related('items')

    menus = sorted(all_menus, key=attrgetter('created_date'))
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_edit_menu(request, pk=None):
    if request.method == "POST":
        title = "Add Menu"

        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        title = "Change Menu"
        try:
            menu = Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            menu = None
        form = MenuForm(instance=menu)
    return render(request, 'menu/menu_edit.html', {'form': form, 'title': title})
