from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import APIView
import logging

from credentials_app.models import User, Credentials
from credentials_app.serializers import *
from credentials_app.utilities.decorators import useronly_restriction

app_name = 'credentials_app'
logger = logging.getLogger('service')

class CredentialView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        try:
            user_obj = User.objects.get(id=request.user.id)
            user_credentials = Credentials.objects.filter(user_id=user_obj)
            serializer = CredentialsSerializer(user_credentials, many=True)
            return Response({
                "status": "success",
                "message": "Credential details fetched successfully",
                "data": {
                    "credential_details": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Exception")
            return Response({
                "status": "error",
                "message": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            serializer = CheckCredentialsSerializer(data=data)
            if serializer.is_valid():
                user_obj = User.objects.get(id=request.user.id)
                user_info = Credentials.objects.create(
                    **serializer.data, user=user_obj)
                slizer = CredentialsSerializer(user_info)
                return Response({
                    "status": "success",
                    "message": "Credentials created successfully",
                    "data": {
                        "details": slizer.data
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": serializer.errors,
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Exception")
            return Response({
                "status": "error",
                "message": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CredentialDetails(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request, id):
        try:
            user_obj = User.objects.get(id=request.user.id)
            cred_details = Credentials.objects.get(id=id, user=user_obj)
            serializer = CredentialsSerializer(cred_details)
            return Response({
                "status": "success",
                "message": "Credential details fetched successfully",
                "data": {
                    "credential_details": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Exception")
            return Response({
                "status": "error",
                "message": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            user_obj = User.objects.get(id=request.user.id)
            credential_obj = Credentials.objects.get(id=id, user=user_obj)
            serializer = CredentialsSerializer(
                credential_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Credential details updated successfully",
                    "data": {}
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": serializer.errors,
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Exception")
            return Response({
                "status": "error",
                "message": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            user_obj = User.objects.get(id=request.user.id)
            credential_obj = Credentials.objects.get(id=id, user=user_obj)
            credential_obj.delete()
            return Response({
                "status": "success",
                "message": "Credential deleted successfully",
                "data": {}
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Exception")
            return Response({
                "status": "error",
                "message": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ShareCredentials(APIView):

    permission_classes = ([IsAuthenticated])

    def post(self, request):
        try:
            data = request.data
            receiver_json = data['user_id']
            share_id = data['share_id']
            user_obj = User.objects.get(id=request.user.id)
            user_cred = Credentials.objects.get(id=share_id, user=user_obj)
            cred_share_serializer = CredentialsSerializer(user_cred)
            for users in receiver_json:
                for key, val in users.items():
                    re_ins = User.objects.get(id=val)
                    if user_cred.share_info:
                        cred_lst = user_cred.share_info
                        if val not in cred_lst:
                            Credentials.objects.create(title=cred_share_serializer.data['title'], description=cred_share_serializer.data[
                                                        'description'], value=cred_share_serializer.data['value'], expire_on=cred_share_serializer.data['expire_on'], user=re_ins)
                            cred_lst.append(val)
                            user_cred.save()
                        else:
                            return Response({
                                "status": "error",
                                "message": f"Credentials already shared to the user {val}",
                                "data": {}
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user_cred.share_info = [val]
                        Credentials.objects.create(title=cred_share_serializer.data['title'], description=cred_share_serializer.data[
                                                   'description'], value=cred_share_serializer.data['value'], expire_on=cred_share_serializer.data['expire_on'], user=re_ins)
                        user_cred.save()
            return Response({
                "status": "success",
                "message": "Credentials shared successfully",
                "data": {
                    "credentials_shared": cred_share_serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Exception")
            return Response({
                "status": "error",
                "message": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
