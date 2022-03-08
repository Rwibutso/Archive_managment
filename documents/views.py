from .models import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *



class DocImageView(generics.ListCreateAPIView):
    serializer_class = DocImageSerializer
    queryset = Files_image.objects.all()

class DocInvoiceView(generics.ListCreateAPIView):
    serializer_class = DocInvoiceSerializer
    queryset = Files_invoice.objects.all()

class DocLetterView(generics.ListCreateAPIView):
    serializer_class = DocLetterSerializer
    queryset = Files_letter.objects.all()

class DocReceiptsView(generics.ListCreateAPIView):
    serializer_class = DocReceiptSerializer
    queryset = Files_receipt.objects.all()

class DocReportsView(generics.ListCreateAPIView):
    serializer_class = DocReportsSerializer
    queryset = Files_reports.objects.all()



