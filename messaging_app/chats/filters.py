import django_filters
from .models import Message
from django.contrib.auth.models import User

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    recipient = django_filters.ModelChoiceFilter(
        field_name='conversation__participants',
        queryset=User.objects.all(),
        label='Recipient',
        method='filter_by_recipient'
    )
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'start_date', 'end_date']

    def filter_by_recipient(self, queryset, name, value):
        return queryset.filter(conversation__participants=value)
