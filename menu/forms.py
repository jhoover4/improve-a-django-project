import datetime

from django.forms import DateField, ModelForm, ValidationError
from django.forms.extras.widgets import SelectDateWidget

from .models import Menu, Item


def date_after_today_validator(exp_date):
    if exp_date and exp_date < datetime.date.today():
        raise ValidationError('The expiration date has already passed.')


class MenuForm(ModelForm):
    expiration_date = DateField(
        required=False, widget=SelectDateWidget(), validators=[date_after_today_validator]
    )

    class Meta:
        model = Menu
        exclude = ('created_date',)


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ('created_date',)

    def clean_description(self):
        """Description must have at least 10 characters."""

        description = self.cleaned_data['description']
        if not description or len(description) < 10:
            raise ValidationError('Description must be at least 10 characters.')

        return description

    def clean_ingredients(self):
        """Must have at least 2 ingredients."""

        ingredients = self.cleaned_data['ingredients']

        if len(ingredients) < 2:
            raise ValidationError('An item must have at least two ingredients.')

        return ingredients
