from rest_framework import serializers
from beauty_saloon_db.models import Saloon, Master, Service, Day, WorkingTime


class SaloonsListSerializer(serializers.ModelSerializer):
    """Returns all saloons"""
    class Meta:
        model = Saloon
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    """Returns services"""
    class Meta:
        model = Service
        fields = '__all__'


class MasterSerializer(serializers.ModelSerializer):
    """Returns masters"""
    services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = Master
        fields = '__all__'


class SaloonDetailSerializer(serializers.ModelSerializer):
    """Returns saloon details"""
    masters = MasterSerializer(many=True, read_only=True)

    class Meta:
        model = Saloon
        fields = ('masters',)


class DaysListSerializer(serializers.ModelSerializer):
    """Returns next week"""
    class Meta:
        model = Day
        fields = ('date',)


class WorkingTimeListSerializer(serializers.ModelSerializer):
    """Returns working times list"""
    day = serializers.SlugRelatedField(slug_field='date', read_only=True)
    class Meta:
        model = WorkingTime
        fields = '__all__'


class DayListMastersSerializer(serializers.ModelSerializer):
    """Returns days with master and worktimes for them"""

    working_times = WorkingTimeListSerializer(many=True, read_only=True)
    master = serializers.SlugRelatedField(slug_field='name',
                                          read_only=True)

    class Meta:
        model = Day
        fields = ('date', 'master', 'working_times',)