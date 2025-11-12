from rest_framework import serializers
from .models import Constituency, Ward, Party, Candidate, ElectionResult


class ConstituencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituency
        fields = '__all__'


class WardSerializer(serializers.ModelSerializer):
    constituency = ConstituencySerializer(read_only=True)
    constituency_id = serializers.PrimaryKeyRelatedField(
        queryset=Constituency.objects.all(), source='constituency', write_only=True
    )

    class Meta:
        model = Ward
        fields = ['id', 'ward_no', 'constituency', 'constituency_id']


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    party = PartySerializer(read_only=True)
    party_id = serializers.PrimaryKeyRelatedField(
        queryset=Party.objects.all(), source='party', write_only=True
    )

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'party', 'party_id']


class ElectionResultSerializer(serializers.ModelSerializer):
    ward = WardSerializer(read_only=True)
    candidate = CandidateSerializer(read_only=True)

    ward_id = serializers.PrimaryKeyRelatedField(
        queryset=Ward.objects.all(), source='ward', write_only=True
    )
    candidate_id = serializers.PrimaryKeyRelatedField(
        queryset=Candidate.objects.all(), source='candidate', write_only=True
    )

    class Meta:
        model = ElectionResult
        fields = [
            'id', 'ward', 'ward_id',
            'candidate', 'candidate_id',
            'total_votes', 'booth_data'
        ]
