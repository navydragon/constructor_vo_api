from rest_framework import serializers

from products.models import Product
from programs.models import NsiType, Ministry, Nsi

class NsiTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NsiType
        fields = '__all__'

class MinistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ministry
        fields = ['id', 'fullname', 'short_nominative', 'short_genitive']

class NsiSerializer(serializers.ModelSerializer):
    nsiDate = serializers.DateField(allow_null=True, required=False)
    nsiProtocolDate = serializers.DateField(allow_null=True, required=False)
    nsiYear = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Nsi
        fields = '__all__'

    def to_internal_value(self, data):
        for field in ['nsiDate', 'nsiProtocolDate','nsiYear']:
            if data.get(field) == '':
                data[field] = None
        return super().to_internal_value(data)



