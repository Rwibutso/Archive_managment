from django.urls import path
from . import views 

urlpatterns = [
   
    path('images/', views.DocImageView.as_view()),
    path('invoice/', views.DocInvoiceView.as_view()),
    path('receipt/', views.DocReceiptsView.as_view()),
    path('letter/', views.DocLetterView.as_view()),
    path('report/', views.DocReportsView.as_view()),

]