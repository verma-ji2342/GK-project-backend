"""
View.py
"""

# for class views
from rest_framework.decorators import api_view
# for responding 
from rest_framework.response import Response
from rest_framework import viewsets
from home.models import Person, Department, State
from home.serializer import PeopleSerializer, LoginSerializer, RegisterSerializer, LogoutSerializer
from rest_framework.views import APIView

# for responding errors
from rest_framework import status

# for registrations and login 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

#for token verification and all
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# for pagination
from  django.core.paginator import Paginator

#for action in django 
from rest_framework.decorators import action


#for swagger integration
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .schemas import request_body_schema


class LoginAPI(APIView):
    """
    Login class
    """

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                {"msg": serializer.errors, "status": False}, status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=serializer.data["username"], password=serializer.data["password"]
        )

        if not user:
            return Response({
                'msg': 'Invalid credentials',
                'status': False,
            }, status.HTTP_404_NOT_FOUND)
        
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {"sataus": True, "user": "login", "token": str(token)},
            status.HTTP_201_CREATED,
        )



class LogoutAPI(APIView):
    """
    Logout API
    """
    logout_serializer = LogoutSerializer()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        """
        Delete token from database
        """
        try: 
            request.auth.delete()
            return Response({
                'message': 'Logout from all devices',
                'status': True
            }, status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': 'Something went wrong in Token',
                'status': False
            }, status.HTTP_400_BAD_REQUEST)



class RegisterAPI(APIView):
    """
    Registration API
    """
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                {"status": False, "message": serializer.errors},
                status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            {"status": True, "msg": serializer.data}, status.HTTP_201_CREATED
        )


class PersonViewSet(viewsets.ModelViewSet):
    """
    PersonViewSet class
    """

    queryset = Person.objects.all()
    serializer_class = PeopleSerializer





class testingAPI(APIView):
    """
    testing api
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):
        """
        GET method
        """
        try:
            print(request.user)  # which user is logedin
            objs = Person.objects.all()
            page = request.GET.get('page', 1)
            page_size = 3
            paginator = Paginator(objs, page_size)
            print(objs)
            serializer = PeopleSerializer(paginator.page(page), many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        
        except Exception as e:
            print("exception", str(e))
            return Response({
                'status' : False,
                'message': "invalid page"
            })
        

        


    @swagger_auto_schema(request_body=PeopleSerializer)
    def post(self, request):
        """
        POST method
        """
        try:
            data = request.data
            print(data)
            dept_name = data['department']['dept_name']
            state_name = data['state']['state']
            serializer = PeopleSerializer(data=data, context={'request': request})
            print("correct chal rha hai")

            state_obj = None
            if State.objects.filter(state=state_name).exists():
                state_obj = State.objects.get(state=state_name)
            
            dept_obj = None
            if Department.objects.filter(dept_name = dept_name).exists():
                dept_obj = Department.objects.get(dept_name=dept_name)
            
            print("correct chal rha hai")

            print("*********************")
            if serializer.is_valid():
                print("yes...")
                # print("print karo ",serializer.data)
                serializer.save(state=state_obj, department=dept_obj)
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print(str(e))
            return Response({
                "message" : "Something went worng",
                "status": False
            }, status.HTTP_417_EXPECTATION_FAILED)


    @swagger_auto_schema(request_body=request_body_schema)
    def put(self, request):
        """
        PUT method
        """
        try:
            data = request.data
            obj = Person.objects.get(id=data["id"])
            print(obj)
            dept_name = data['department']['dept_name']
            state_name = data['state']['state']

            state_obj = None
            if State.objects.filter(state=state_name).exists():
                state_obj = State.objects.get(state=state_name)
            
            dept_obj = None
            if Department.objects.filter(dept_name = dept_name).exists():
                dept_obj = Department.objects.get(dept_name=dept_name)
            
            serializer = PeopleSerializer(obj, data=data, context={'request': request})
            
            if serializer.is_valid():
                serializer.save(state=state_obj, department=dept_obj)
                return Response(serializer.data)
            return Response(serializer.errors)
        

        except Exception as e:
            print("error section", str(e))
            return Response({
                "status": False,
                "message": "Input should be in correct format"
            }, status.HTTP_206_PARTIAL_CONTENT)


    @swagger_auto_schema(request_body=request_body_schema)
    def patch(self, request):
        """
        FATCH method
        """
        try:
            data = request.data
            obj = Person.objects.get(id=data["id"])
            print(obj)
            dept_name = data['department']['dept_name']
            state_name = data['state']['state']

            state_obj = None
            if State.objects.filter(state=state_name).exists():
                state_obj = State.objects.get(state=state_name)
            
            dept_obj = None
            if Department.objects.filter(dept_name = dept_name).exists():
                dept_obj = Department.objects.get(dept_name=dept_name)
            
            serializer = PeopleSerializer(obj, data=data, partial=True, context={'request': request})
            
            if serializer.is_valid():
                serializer.save(state=state_obj, department=dept_obj)
                return Response(serializer.data)
            return Response(serializer.errors)
        

        except Exception as e:
            print("error section", str(e))
            return Response({
                "status": False,
                "message": "Input should be in correct format"
            }, status.HTTP_206_PARTIAL_CONTENT)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id of a person'),
            },
            required=['id']
        )
    )
    def delete(self, request):
        """
        DELETE method
        """
        data = request.data
        try:
            obj = Person.objects.get(id=data["id"])
            print(obj)
            obj.delete()
            return Response({"msg": "Data has been deleted comppletely from database"})
        except:
            return Response({"msg": "Something went wrong with input DATA"})