from django.urls import path
from .views import (ListComissions, ListComissionDetail,
                    ListSellers, ListSellersDetail,
                    ListSales, ListSalesDetail, SalesMonth)

urlpatterns = [
     # Comission
     path('listComissions/', ListComissions.as_view(), name='list_comissions'),
     path('listComissionsDetail/<int:pk>',
          ListComissionDetail.as_view(),
          name='list_comissions_detail'),
     # Seller
     path('listSellers/', ListSellers.as_view(), name='list_sellers'),
     path('listSellersDetail/<int:pk>',
          ListSellersDetail.as_view(),
          name='list_sellers_detail'),
     # Sales
     path('listSales/', ListSales.as_view(), name='list_sales'),
     path('listSalesDetail/<int:pk>',
          ListSalesDetail.as_view(),
          name='list_sales_detail'),
     # Sales Month
     path('sales_month/', SalesMonth.as_view(), name='sales_month')

]
