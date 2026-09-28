from django.shortcuts import render
from expense.models import *
from expense.serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models.aggregates import *
from django.utils import timezone
from expense.permission import IsOwner

# Create your views here.
class UserViewSet(ViewSet):
    def create(self,request):
        dser=UserSerializer(data=request.data)

        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors)

class ExpenseMViewset(ViewSet):
    
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    def create(self,request):
        dser=ExpenseSerializer(data=request.data)
        if dser.is_valid():
            dser.save(owner=request.user)
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        list=Expenses.objects.filter(owner=request.user)
        ser=ExpenseSerializer(list,many=True)
        return Response(data=ser.data,status=status.HTTP_200_OK)

    def retrieve(self,request,pk=0):
        list=Expenses.objects.get(id=pk,owner=request.user)
        ser=ExpenseSerializer(list)
        return Response(data=ser.data,status=status.HTTP_200_OK)

    def update(self,request,pk=0):
        list=Expenses.objects.get(id=pk)
        dser=ExpenseSerializer(data=request.data,instance=list)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.erros,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=0):
        Expenses.objects.get(id=pk).delete()
        return Response(data={"msg":"deleted"})

    def partial_update(self,request,pk=0):
        list=Expenses.objects.get(id=pk)
        dser=ExpenseSerializer(list,partial=True,data=request.data)

        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors)


class SummeryViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]
    def get(self,request):
        cur_date=timezone.now()
        cur_month=cur_date.month
        cur_year=cur_date.year
        expense=Expenses.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
        summery=expense.values('amount').aggregate(Sum('amount'))
        summery_data=expense.values('category').annotate(Sum('amount'))

        summery_data={
            "total_summery":summery,
            "category_expense":summery_data
        }

        return Response(data=summery_data)
