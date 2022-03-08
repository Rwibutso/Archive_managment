from rest_framework import serializers
from .models import *

class DocImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files_image
        fields = ('id', 'cover', 'name', 'description', 'private')

class DocInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files_invoice
        fields = ('id', 'cover', 'name', 'description', 'private')

class DocReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files_receipt
        fields = ('id', 'cover', 'name', 'description', 'private')

class DocLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files_letter
        fields = ('id', 'cover', 'name', 'description', 'private')

class DocReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files_reports
        fields = ('id', 'cover', 'name', 'description', 'private')