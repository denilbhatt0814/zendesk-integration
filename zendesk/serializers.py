from rest_framework import serializers
from .models import Ticket, DailyTicketCount

class TicketSerializer(serializers.ModelSerializer):
    satisfaction_rating = serializers.JSONField(required=False, allow_null=True)
    class Meta:
        model = Ticket
        fields = '__all__'

class DailyTicketCountSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=False, allow_null=True)
    class Meta:
        model = DailyTicketCount
        fields = '__all__'