from rest_framework import serializers
from logbook.models import Trip


class TripSerializer(serializers.ModelSerializer):
    car = serializers.StringRelatedField()
    distance_km = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trip
        fields = (
            "id",
            "car",
            "from_city",
            "to_city",
            "start_date",
            "end_date",
            "start_odometer",
            "end_odometer",
            "distance_km",
            "notes",
        )
        read_only_fields = fields


class CarStatsSerializer(serializers.Serializer):
    car_id = serializers.IntegerField()
    car_name = serializers.CharField()
    trips_count = serializers.IntegerField()
    total_distance_km = serializers.IntegerField()
    refuels_count = serializers.IntegerField()
    total_fuel_liters = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_fuel_cost = serializers.DecimalField(max_digits=12, decimal_places=2)
    avg_cost_per_liter = serializers.DecimalField(max_digits=12, decimal_places=3)
