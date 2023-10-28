from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated

from Accounts.models import User
from Accounts.serializers import UserSerializer
from properties.serializers import PropertySerializer
from properties.models import Catogory, Wallet, Property

class PropertyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            property_object = Property.objects.all()
            serializer = PropertySerializer(property_object, many=True)
            return Response({
                "status":"success",
                "message":"Property details fetched successfully",
                "data":{
                    "list_of_properties":serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status":"error",
                "message":str(e),
                "data":{}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data=request.data
            pos_type_obj = Catogory.objects.get(id=data['posting_type'])
            user_obj = User.objects.get(id=request.user.id)
            serializer = PropertySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            Property.objects.create(propname=serializer.data['propname'], address=serializer.data['address'], description=serializer.data['description'], amount=serializer.data['amount'], posting_type=pos_type_obj, user=user_obj)
            wallet_obj = Wallet.objects.filter(wallet_owner=user_obj, created_by=user_obj.id)
            if not wallet_obj:
                Wallet.objects.create(wallet_owner=user_obj, wallet_amount=100, wallet_limit=500)
            return Response({
                "status":"success",
                "message":"Property created successfully",
                "data":{
                    "property_created":serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status":"error",
                "message":str(e),
                "data":{}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PropertyDetailsView(APIView):
    def get(self, request, pk):
        try:
            property_object = Property.objects.get(pk=pk)
            serializer = PropertySerializer(property_object)
            return Response({
                "status":"success",
                "message":"Property details fetched succesfully",
                "data":{
                    "property":serializer.data
                }
            }, status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status":"error",
                "message":str(e),
                "data":{}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, pk):
        try:
            property_object = Property.objects.get(pk=pk)
            serializer = PropertySerializer(property_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status":"success",
                    "message":"Property updated successfully",
                    "data":{
                        "property":serializer.data
                    }
                }, status=status.HTTP_200_OK)
            return Response({
                "status":"error",
                "message":serializer.errors,
                "data":{}
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status":"error",
                "message":str(e),
                "data":{}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            pro = Property.objects.get(pk=pk)
            pro.delete()
            return Response({
                "status":"success",
                "message":"Property deleted successfully",
                "data":{}
            }, status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({
                "status":"error",
                "message":str(e),
                "data":{}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserDetails(APIView):
    permission_classes = ({IsAuthenticated})
    def get(self, request):
        try:
            user_obj = User.objects.get(id=request.user.id)
            user_serializer = UserSerializer(user_obj)
            prop_obj = Property.objects.filter(user=user_obj)
            prop_serializer = PropertySerializer(prop_obj, many=True)
            data = [user_serializer.data]
            data.extend(prop_serializer.data)
            return Response({
                "status":"success",
                "message":"User details fetched successfully",
                "data":{
                    "user_details": data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status":"error",
                "message":str(e),
                "data":{}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)