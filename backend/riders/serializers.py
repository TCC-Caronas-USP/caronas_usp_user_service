from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .services import CustomerService
from .models import Vehicle


class RiderSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=255)
    document = serializers.CharField(max_length=14)
    phone_number = serializers.CharField(max_length=15)
    is_foreigner = serializers.BooleanField()
    is_company = serializers.BooleanField()


class RiderPatchSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(max_length=255, required=False)
    document = serializers.CharField(max_length=14, required=False)
    phone_number = serializers.CharField(max_length=15, required=False)
    is_foreigner = serializers.BooleanField(required=False)
    is_company = serializers.BooleanField(required=False)


class PatchSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=True)
    is_foreign = serializers.BooleanField(required=False)
    registration = serializers.CharField(max_length=30, required=False)
    icao_model = serializers.CharField(max_length=30, required=False)
    avanac = serializers.CharField(max_length=100, required=False, allow_blank=True)
    mtow = serializers.FloatField(required=False)
    wingspan = serializers.FloatField(required=False)
    length = serializers.FloatField(required=False)
    rider = RiderPatchSerializer()
    email = serializers.IntegerField(required=False)

    customer_service = CustomerService()

    def validate(self, attrs):

        email = attrs.get("email")

        if email is not None:
            try:
                self.customer_service.get_customer_by_id(email)
            except ObjectDoesNotExist:
                raise ValidationError("Invalid registrant ID")

        validated_data = super().validate(attrs)
        if hasattr(self, "initial_data"):
            non_editable_fields = set(self.initial_data.keys()) - set(
                self.fields.keys()
            )
            if non_editable_fields:
                raise ValidationError(
                    f"The following fields are not editable: {non_editable_fields}"
                )
        return validated_data

    class Meta:
        ref_name = "vehicle"


class VehicleSerializer(serializers.ModelSerializer):
    rider = RiderSerializer()

    class Meta:
        model = Vehicle
        fields = "__all__"

    customer_service = CustomerService()

    def validate(self, attrs):

        email = attrs.get("email")

        try:
            self.customer_service.get_customer_by_id(email)
        except ObjectDoesNotExist:
            raise ValidationError("Invalid registrant ID")

        validated_data = super().validate(attrs)
        return validated_data
