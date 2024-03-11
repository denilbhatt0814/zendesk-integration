from django.http import HttpRequest, HttpResponse

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Server is runnningggg...")

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Ticket, DailyTicketCount
from .serializers import TicketSerializer, DailyTicketCountSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(detail=False, methods=['get'])
    def get_by_ticket_id_and_subdomain(self, request):
        ticket_id = request.query_params.get('ticket_id')
        subdomain = request.query_params.get('subdomain')
        if not ticket_id or not subdomain:
            return Response(
                {"error": "Both 'ticket_id' and 'subdomain' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        ticket = get_object_or_404(Ticket, id=ticket_id, subdomain=subdomain)
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)
    
class DailyTicketCountViewSet(viewsets.ModelViewSet):
    queryset = DailyTicketCount.objects.all()
    serializer_class = DailyTicketCountSerializer