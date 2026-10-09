from rest_framework import serializers

from jobs.models import Job

# Explicitly defining API fields for Input API contract i.e. JobCreateSerializer
class JobCreateSerializer(serializers.Serializer): 
    name = serializers.CharField(
        max_length=120,
        allow_blank=False,
    )

    payload = serializers.JSONField(
        required=False,
        default=dict,
    )

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Job name must contain at least 3 characters."
            )

        return value # returning value so that `validated_data` gets the cleaned version & not the raw input

# Output API contract = JobSerializer using ModelSerializer
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "name",
            "payload",
            "status",
            "created_at",
            "updated_at",
        ]