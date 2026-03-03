from rest_framework import serializers
from claims.models import Claim, Member, ProcedureCost
from fraud.models import ClaimValidation
from decimal import Decimal

class ClaimInputSerializer(serializers.Serializer):
    member_id = serializers.CharField()
    provider_id = serializers.CharField()
    diagnosis_code = serializers.CharField()
    procedure_code = serializers.CharField()
    claim_amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_claim_amount(self, value):
        if value <= Decimal('0'):
            raise serializers.ValidationError("Claim amount must be positive.")
        return value

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class ProcedureCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureCost
        fields = '__all__'

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'
        read_only_fields = ['claim_date']

class ClaimValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimValidation
        fields = '__all__'
