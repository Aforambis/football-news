from django.forms import ModelForm
from main.models import News
from main.models import Item

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ["title", "content", "category", "thumbnail", "is_featured"]

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'amount', 'description']