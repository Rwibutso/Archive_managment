from .models import File
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics, status, filters
from .serializers import DocSerializer
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend






class DocView(generics.ListCreateAPIView):
    serializer_class = DocSerializer
    queryset = File.objects.all()
    http_method_names = [u"get", u"post"]

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         queryset = File.objects.filter(user=self.request.user.id)
    #     return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            data_errors = {}
            data_message = str("")
            for P, M in serializer.errors.items():
                data_message += P + ": " + M[0].replace(".", "") + ", "
            data_errors["detail"] = data_message
            return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)
        self.get_success_headers(serializer.data)
        return Response(
            {
                "detail": _(
                    "The file successfully uploaded"
                )
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, *args, **kwargs):
        """
        Returns a list all users
        """
        queryset = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class DocListView(generics.ListAPIView):
    """
    Returns a list of all documents
    
    """

    serializer_class = DocSerializer
    permission_classes = (IsAuthenticated,)
    queryset = File.objects.all()
    http_method_names = [u"get"]
    #get_user_model = ser as 

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ["id", "name", "type"]
    search_fields = ["name", "id"]
    ordering_fields = ["created", "modified"]

    def get(self, request, *args, **kwargs):
        """
        Returns a list all users
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)



# class DocImageView(generics.ListCreateAPIView):
#     serializer_class = DocImageSerializer
#     queryset = Files_image.objects.all()

# class DocInvoiceView(generics.ListCreateAPIView):
#     serializer_class = DocInvoiceSerializer
#     queryset = Files_invoice.objects.all()

# class DocLetterView(generics.ListCreateAPIView):
#     serializer_class = DocLetterSerializer
#     queryset = Files_letter.objects.all()
#     http_method_names = [u"get", u"post"]


#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         if not serializer.is_valid():
#             data_errors = {}
#             data_message = str("")
#             for P, M in serializer.errors.items():
#                 data_message += P + ": " + M[0].replace(".", "") + ", "
#             data_errors["detail"] = data_message
#             return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)

#         serializer.save(user=request.user)
#         self.get_success_headers(serializer.data)
#         return Response(
#             {
#                 "detail": _(
#                     "Registration successfully completed. Please check your email to activate your account"
#                 )
#             },
#             status=status.HTTP_201_CREATED,
#         )

#     def get(self, request, *args, **kwargs):
#         """
#         Returns a list all users
#         """
#         queryset = self.queryset.filter(user=request.user)
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data)

# class DocReceiptsView(generics.ListCreateAPIView):
#     serializer_class = DocReceiptSerializer
#     queryset = Files_receipt.objects.all()

# class DocReportsView(generics.ListCreateAPIView):
#     serializer_class = DocReportsSerializer
#     queryset = Files_reports.objects.all()



