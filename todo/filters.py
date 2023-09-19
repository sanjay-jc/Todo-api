import django_filters
from .models import Todo_model

class TodoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = Todo_model
        fields = ['status','title']  
