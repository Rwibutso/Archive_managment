from rest_framework import serializers
from .models import File



class DocSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'cover', 'name', 'description', 'private', 'type')



# class DocImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Files_image
#         fields = ('id', 'cover', 'name', 'description', 'private')

# class DocInvoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Files_invoice
#         fields = ('id', 'cover', 'name', 'description', 'private')

# class DocReceiptSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Files_receipt
#         fields = ('id', 'cover', 'name', 'description', 'private')

# class DocLetterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Files_letter
#         fields = ('id', 'cover', 'name', 'description', 'private', 'user')
#         read_only_fields = ('user',)
        

# class DocReportsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Files_reports
#         fields = ('id', 'cover', 'name', 'description', 'private')