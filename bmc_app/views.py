from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
from rest_framework import viewsets
from .models import Constituency, Ward, Party, Candidate, ElectionResult
from rest_framework.decorators import action
from .serializers import (
    ConstituencySerializer, WardSerializer, PartySerializer,
    CandidateSerializer, ElectionResultSerializer
)


class ConstituencyViewSet(viewsets.ModelViewSet):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer


class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.select_related('constituency').all()
    serializer_class = WardSerializer


class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.select_related('party').all()
    serializer_class = CandidateSerializer


class ElectionResultViewSet(viewsets.ModelViewSet):
    queryset = ElectionResult.objects.select_related('ward', 'candidate').all()
    serializer_class = ElectionResultSerializer

    @action(detail=True, methods=['get'], url_path='booths')
    def get_booth_data(self, request, pk=None):
        result = self.get_object()
        if result.booth_data:
            data = {
                "candidate": result.candidate.name,
                "ward": result.ward.ward_no,
                "total_votes": result.total_votes,
                "booth_data": result.booth_data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message": "No booth data available"}, status=status.HTTP_204_NO_CONTENT)


# ---------- FRONTEND HTML VIEW ----------

def booth_data_page(request):
    """
    Renders a simple HTML page that fetches booth_data via API.
    """
    return render(request, 'home.html')