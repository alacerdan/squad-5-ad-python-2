from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .models import Comissions, Sellers, Sales
from .serializers import (ComissionsSerializer,
                          SellersSerializer,
                          SalesSerializer)
from rest_framework import status
import numpy as np
import json


class ListComissions(APIView):

    def get(self, request, format=None):
        comissions = Comissions.objects.all()
        serializer = ComissionsSerializer(comissions, many=True)
        return Response({"content": serializer.data})

    def post(self, request):
        serializer = ComissionsSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            return Response({"id": content.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListComissionDetail(APIView):

    def get_object(self, pk):
        try:
            return Comissions.objects.get(pk=pk)
        except Comissions.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        comission = self.get_object(pk)
        serializer = ComissionsSerializer(comission)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        comission = self.get_object(pk)
        serializer = ComissionsSerializer(comission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comission = self.get_object(pk)
        comission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSellers(APIView):

    def get(self, request, format=None):
        sellers = Sellers.objects.all()
        serializer = SellersSerializer(sellers, many=True)
        return Response({"content": serializer.data})

    def post(self, request):
        serializer = SellersSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            return Response({"id": content.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListSellersDetail(APIView):

    def get_object(self, pk):
        try:
            return Sellers.objects.get(pk=pk)
        except Sellers.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        seller = self.get_object(pk)
        serializer = SellersSerializer(seller)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        seller = self.get_object(pk)
        serializer = SellersSerializer(seller, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        seller = self.get_object(pk)
        seller.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSales(APIView):

    def get(self, request, format=None):
        sales = Sales.objects.all()
        serializer = SalesSerializer(sales, many=True)
        return Response({"content": serializer.data})

    def post(self, request):
        serializer = SalesSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            return Response({"id": content.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SalesMonth(APIView):

    def post(self, request):
        month = request.data['month']
        seller_id = request.data['seller_id']
        seller = Sellers.objects.get(pk=seller_id)

        # Calculando a quantidade em valor das vendas realizadas pelo vendedor
        sales = Sales.objects.filter(seller_id=seller_id, month=month)
        print(sales)
        amount = [float(sale['amount']) for sale in sales.values()]
        amount = np.array(amount).sum()
        print(amount)
        min_value = seller.comission.min_value
        lower = seller.comission.lower_percentage
        upper = seller.comission.upper_percentage

        if amount < min_value:
            comission = amount*lower/100
        else:
            comission = amount*upper/100

        data = {'seller_id': seller_id,
                'comission': comission,
                'amount': amount}
        print(data)

        return Response(json.dumps(data))


class ListSalesDetail(APIView):

    def get_object(self, pk):
        try:
            return Sales.objects.get(pk=pk)
        except Sales.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        sale = self.get_object(pk)
        serializer = SellersSerializer(sale)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        sale = self.get_object(pk)
        serializer = SellersSerializer(sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        seller = self.get_object(pk)
        seller.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
