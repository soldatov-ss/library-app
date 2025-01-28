from rest_framework import serializers

from library_app.apps.loans.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    borrowed_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", read_only=True)
    returned_at = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S.%fZ",
        required=False,
        allow_null=True,
        read_only=True,
    )

    class Meta:
        model = Loan
        fields = ["id", "user", "book", "borrowed_at", "returned_at"]
