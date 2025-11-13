from django.urls import path
from .views import CandidateExcelDataView

urlpatterns = [
    path("candidates/", CandidateExcelDataView.as_view(), name="candidate-excel-data"),
]
