from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ConstituencyViewSet, WardViewSet, PartyViewSet,
    CandidateViewSet, ElectionResultViewSet,booth_data_page
)
from . import views as v

router = DefaultRouter()
router.register('constituencies', ConstituencyViewSet)
router.register('wards', WardViewSet)
router.register('parties', PartyViewSet)
router.register('candidates', CandidateViewSet)
router.register('results', ElectionResultViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', v.booth_data_page),
]
