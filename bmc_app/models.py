from django.db import models

# Create your models here.
class Constituency(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Ward(models.Model):
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, related_name='wards')
    ward_no = models.CharField(max_length=50)  # e.g. "PRABHAG NO 1 - 1"

    def __str__(self):
        return f"{self.constituency.name} - {self.ward_no}"


class Party(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    name = models.CharField(max_length=150)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, related_name='candidates')

    def __str__(self):
        return f"{self.name} ({self.party.name if self.party else 'Independent'})"


class ElectionResult(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='results')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='results')
    total_votes = models.IntegerField()
    # Optional: store booth-level votes if available
    booth_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.candidate.name} - {self.ward.ward_no} ({self.total_votes} votes)"