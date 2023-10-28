from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from Accounts.models import User
from properties.models import Wallet
from properties.serializers import WalletSerializer

class WalletListView(APIView):
    permission_classes=([IsAuthenticated])
    def get(self, request):
        try:
            user_obj = User.objects.get(id=request.user.id)
            wallet_obj = Wallet.objects.get(wallet_owner=user_obj)
            if wallet_obj:
                serializer = WalletSerializer(wallet_obj)
                return Response({
                    "status":"success",
                    "message":"Wallet details fetched successfully",
                    "data":{
                        "wallet_details":serializer.data
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status":"error",
                "message":str(e),
                "data":{}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class WalletRechargeView(APIView):
    permission_classes=([IsAuthenticated])
    def post(self, request):
        try:
            data = request.data
            recharge_amt = data['recharge_amt']
            user_obj = User.objects.get(id=request.user.id)
            wallet_obj = Wallet.objects.get(wallet_owner=user_obj)
            wal_exist_amt = wallet_obj.wallet_amount
            amt_limit = wal_exist_amt + recharge_amt
            if amt_limit > 500:
                return Response({
                    "status":"error",
                    "message":f"Your available wallet amount is {wal_exist_amt}, your total wallet amount should be less than 500",
                    "data":{}
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                total_amt = wal_exist_amt + recharge_amt
                wallet_obj.wallet_amount = total_amt
                wallet_obj.save()
                return Response({
                    "status":"success",
                    "message":"wallet amount recharged successfully",
                    "data":{
                        "wallet_amount":wallet_obj.wallet_amount
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status":"error",
                "message":str(e),
                "data":{}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)