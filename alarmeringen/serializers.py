from rest_framework import serializers

from alarmeringen.models import Alarmering, CapCode, Regio, Dienst


class CapCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapCode
        fields = ('capcode', 'omschrijving')


class RegioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regio
        fields = ('id', 'omschrijving')


class DienstSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dienst
        fields = ('id', 'omschrijving')


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class AlarmeringSerializer(serializers.ModelSerializer):
    capcodes = CapCodeSerializer(many=True, read_only=True, )
    regio = RegioSerializer(read_only=True, )
    dienst = DienstSerializer(read_only=True, )
    subitems = RecursiveField(many=True, read_only=True, )

    class Meta:
        model = Alarmering
        depth = 1
        fields = ('id', 'datum', 'tijd', 'melding', 'tekstmelding', 'dienst',
                  'prio1', 'grip', 'brandinfo', 'details', 'regio', 'plaats',
                  'postcode', 'straat', 'lat', 'lon', 'capcodes', 'subitems')
