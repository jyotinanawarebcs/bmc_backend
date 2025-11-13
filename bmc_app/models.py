from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('state', 'name')

    def __str__(self):
        return f"{self.name}, {self.state.name}"

class LocalBody(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='local_bodies')
    name = models.CharField(max_length=150)
    lb_type = models.CharField(max_length=50, blank=True, null=True)  # e.g., MC = Municipal Corporation
    lb_code = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.lb_type})"


class Ward(models.Model):
    local_body = models.ForeignKey(LocalBody, on_delete=models.CASCADE, related_name='wards')
    ward_no = models.IntegerField()
    name = models.CharField(max_length=150)
    reservation = models.CharField(max_length=100, blank=True, null=True)  # e.g., OBC(W), SC, GEN

    class Meta:
        unique_together = ('local_body', 'ward_no')

    def __str__(self):
        return f"{self.name} (Ward {self.ward_no})"


class Party(models.Model):
    party_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=150)
    abbreviation = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"

class Election(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='elections')
    year = models.IntegerField()
    polling_date = models.DateField()
    poll_no = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('state', 'year', 'polling_date')

    def __str__(self):
        return f"{self.state.name} - {self.year}"

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=150)
    father_husband_name = models.CharField(max_length=150, blank=True, null=True)
    name_o = models.CharField(max_length=150, blank=True, null=True)  # Regional language name
    father_husband_name_o = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, related_name='candidates')
    education = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.party.abbreviation if self.party else 'IND'})"



class ElectionResult(models.Model):
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE, related_name='result')
    votes = models.IntegerField()
    position = models.IntegerField()
    status = models.CharField(max_length=50, blank=True, null=True)  # e.g., Winner, Runner-up
    total_candidates = models.IntegerField(blank=True, null=True)
    valid_votes = models.IntegerField(blank=True, null=True)
    vote_share_percentage = models.FloatField(blank=True, null=True)
    deposit_lost = models.BooleanField(default=False)
    total_electors = models.IntegerField(blank=True, null=True)
    total_votes = models.IntegerField(blank=True, null=True)
    rejected_votes = models.IntegerField(blank=True, null=True)
    voter_turnout_percentage = models.FloatField(blank=True, null=True)
    affidavit_link = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.candidate.name} - {self.votes} votes"
