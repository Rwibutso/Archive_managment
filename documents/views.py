from .models import File
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics, status, filters
from .serializers import DocSerializer, DocUploadSerializer
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from documents import serializers


class DocView(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = DocSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "put", "delete"]

    def get(self, request, *args, **kwargs):
        """
        Returns user's docs informations
        """
        try:
            current_doc = File.objects.get(id=kwargs["pk"])
            doc_serialized = DocSerializer(current_doc).data
            return Response(doc_serialized)
        except get_user_model().DoesNotExist:
            return Response(
                {"detail": _("Doc is not available")},
                status=status.HTTP_404_NOT_FOUND,
            )


    def put(self, request, *args, **kwargs):
        """
        Updates user's detailed information
        """
        try:
            current_doc = File.objects.get(id=kwargs["pk"])
            
            data = request.data.copy()
        
            partial = kwargs.pop("partial", True)
            serializer = self.get_serializer(current_doc, data=data, partial=partial)

            if not serializer.is_valid():
                data_errors = {}
                data_message = str("")
                for P, M in serializer.errors.items():
                    data_message += P + ": " + M[0].replace(".", "") + ", "
                data_errors["detail"] = data_message
                return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)

            self.perform_update(serializer)
            doc_serialized = DocSerializer(current_doc).data
            return Response(doc_serialized)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



    def delete(self, request, *args, **kwargs):
        """
        Removes a user from the database
        """
        try:
            current_doc = File.objects.get(id=kwargs["pk"])
            current_doc.delete()
            return Response(
                {"detail": _("Document successfully deleted")}, status=status.HTTP_200_OK
            )
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DocListView(generics.ListAPIView):
    """
    Returns a list of all documents

    """

    serializer_class = DocSerializer
    permission_classes = (IsAuthenticated,)
    queryset = File.objects.all()
    http_method_names = ["get"]

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


class DocUploadView(generics.CreateAPIView):
    """
    Returns a list of all documents

    """

    serializer_class = DocUploadSerializer
    permission_classes = (IsAuthenticated,)
    queryset = File.objects.all()
    http_method_names = ["post"]

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
            {"detail": _("The file successfully uploaded"), "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class DocListByUserView(generics.ListAPIView):
    """
    Returns a list of all documents

    """

    serializer_class = DocSerializer
    permission_classes = (IsAuthenticated,)
    queryset = File.objects.all()
    http_method_names = ["get"]
    # get_user_model = ser as

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
        current_user = get_user_model().objects.get(id=kwargs["user_id"])

        queryset = self.filter_queryset(self.get_queryset())
        user_doc_qs = queryset.filter(user=current_user)
        serializer = self.serializer_class(user_doc_qs, many=True)
        return Response(serializer.data)
