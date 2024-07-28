"""
View.py
"""

# for class views
from rest_framework.decorators import api_view

# for responding
from rest_framework.response import Response
from rest_framework import viewsets
from home.models import Person, Department, State, Account, Project
from home.serializer import (
    PeopleSerializer,
    LoginSerializer,
    RegisterSerializer,
    LogoutSerializer,
    ProjectSerializer,
    AccountSerializer,
)
from rest_framework.views import APIView

# for responding errors
from rest_framework import status

# for registrations and login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# for token verification and all
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# for pagination
from django.core.paginator import Paginator, EmptyPage

# for action in django
from rest_framework.decorators import action


# for swagger integration
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db import transaction


from datetime import date, datetime

from .schemas import (
    request_body_put_schema,
    request_account_body_schema,
    person_post_body,
)


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
            return Response(
                {
                    "msg": "Invalid credentials",
                    "status": False,
                },
                status.HTTP_404_NOT_FOUND,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {"sataus": True, "user": "login", "token": str(token)},
            status.HTTP_200_OK,
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
            return Response(
                {"message": "Logout from all devices", "status": True},
                status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "Something went wrong in Token", "status": False},
                status.HTTP_400_BAD_REQUEST,
            )


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
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "Project_id",
                openapi.IN_QUERY,
                description="Project ID",
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER),
                collection_format="multi",
            ),
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Email",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "Name",
                openapi.IN_QUERY,
                description="Name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "state",
                openapi.IN_QUERY,
                description="State",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "department",
                openapi.IN_QUERY,
                description="Department",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request):
        """
        GET method
        """
        try:
            project_ids = request.GET.getlist("Project_id", [])
            print(project_ids)
            objs = Person.objects.all()
            if not len(project_ids) == 0:
                project_ids = [int(pid) for pid in project_ids]
                objs = objs.filter(project__in=project_ids).distinct()

            email = request.GET.get("email", None)
            if email is not None:
                objs = objs.filter(email=email)

            Name = request.GET.get("Name", None)
            if Name is not None:
                objs = objs.filter(name__startswith=Name)

            state_name = request.GET.get("state", None)
            if state_name is not None:
                objs = objs.filter(state__state__icontains=state_name)

            dept_name = request.GET.get("department", None)
            if dept_name is not None:
                objs = objs.filter(department__dept_name__icontains=dept_name)

            print(request.user)  # which user is logedin
            page = request.GET.get("page", 1)
            page_size = 3
            paginator = Paginator(objs, page_size)
            print(objs)
            serializer = PeopleSerializer(paginator.page(page), many=True)
            print("ohkkk ")
            return Response(serializer.data, status.HTTP_200_OK)
        except EmptyPage:
            return Response({"message": "Page Not Found"}, status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("exception", str(e))
            return Response({"message": str(e)}, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=person_post_body)
    def post(self, request):
        """
        POST method
        """
        try:
            with transaction.atomic():
                data = request.data
                print(data)
                dept_name = data["department"]["dept_name"]
                state_name = data["state"]["state"]
                print("correct chal rha hai")

                state_obj = None
                if State.objects.filter(state=state_name).exists():
                    state_obj = State.objects.get(state=state_name)

                dept_obj = None
                if Department.objects.filter(dept_name=dept_name).exists():
                    dept_obj = Department.objects.get(dept_name=dept_name)

                # Validate Name
                specialcharacter = "!@#$%+_-/><;/';[]{\}^&*(:)"
                if any(c in specialcharacter for c in data["name"]):
                    return Response(
                        {"message": "Name should not contain any special Character"},
                        status.HTTP_400_BAD_REQUEST,
                    )

                # validate Age
                if data["age"] < 18:
                    return Response(
                        {"message": "Age should be greater than 17"},
                        status.HTTP_400_BAD_REQUEST,
                    )

                # email Varification
                if Person.objects.filter(email=data["email"]).exists():
                    return Response(
                        {"message": "Email is already taken"},
                        status.HTTP_400_BAD_REQUEST,
                    )

                new_person = Person.objects.create(
                    name=data["name"],
                    age=data["age"],
                    email=data["email"],
                    pincode=data["pincode"],
                    address=data["address"],
                    state=state_obj,
                    department=dept_obj,
                )

                for pro_id in data["project"]:
                    pro_obj = Project.objects.get(id=pro_id)
                    new_person.project.add(pro_obj)

                new_person.save()

                serializer = PeopleSerializer(new_person)

                return Response(serializer.data, status.HTTP_201_CREATED)

        except Exception as e:
            print("error", str(e))
            return Response(
                {"message": f"{str(e)} field is missing"}, status.HTTP_400_BAD_REQUEST
            )


class EditPersonAPI(APIView):
    """
    Edit in Existing Data
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, id):
        """
        GET one Person
        """
        print(id)
        try:
            obj = Person.objects.get(id=id)
            print(obj)
            serializer = PeopleSerializer(obj)
            return Response(serializer.data)

        except Person.DoesNotExist:
            return Response({"message": "user not found"}, status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response(
                {"msg": "Something went wrong"}, status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(request_body=person_post_body)
    def put(self, request, id):
        """
        PUT method
        """
        try:
            data = request.data
            obj = Person.objects.get(id=id)
            print(obj)
            dept_name = data["department"]["dept_name"]
            state_name = data["state"]["state"]

            state_obj = None
            if State.objects.filter(state=state_name).exists():
                state_obj = State.objects.get(state=state_name)

            dept_obj = None
            if Department.objects.filter(dept_name=dept_name).exists():
                dept_obj = Department.objects.get(dept_name=dept_name)
            print("ohk")
            serializer = PeopleSerializer(obj, data=data)

            project_objs = []
            for pro_id in data["project"]:
                pro_obj = Project.objects.get(id=pro_id)
                project_objs.append(pro_obj)
            print("ohk")
            # serializer.save(state=state_obj, department=dept_obj, project=project_objs)
            person, created = Person.objects.update_or_create(
                id=id,
                defaults={
                    "name": data["name"],
                    "email": data["email"],
                    "department": dept_obj,
                    "state": state_obj,
                    "pincode": data["pincode"],
                    "address": data["address"],
                    "age": data["age"],
                },
            )
            person.project.set(project_objs)

            serializer = PeopleSerializer(person)
            return Response(serializer.data, status=status.HTTP_200_OK)

            # if serializer.is_valid():
            #     print("isdide")
            #     serializer.save(
            #         state=state_obj, department=dept_obj, project=project_objs
            #     )
            #     return Response(serializer.data, status.HTTP_202_ACCEPTED)
            # return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            # pers = Person.objects.aupdate_or_create()

        except Person.DoesNotExist:
            return Response({"message": "User Not Found"}, status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("error section", str(e))
            return Response(
                {"message": "Something went wrong"},
                status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "Data": openapi.Schema(type=openapi.TYPE_STRING, description="Values"),
                # Add other fields as necessary
            },
            required=[],  # Specify required fields if any
        )
    )
    def patch(self, request, id):
        """
        PATCH method
        """
        print(id)
        print(request.data)
        try:
            data = request.data

            project_objs = []
            if "project" in data.keys():
                for pro_id in data["project"]:
                    pro_obj = Project.objects.get(id=pro_id)
                    project_objs.append(pro_obj)
                data.pop("project")

            print(project_objs)
            obj = Person.objects.get(id=id)
            print(obj)
            if "state" in data.keys() and "department" in data.keys():
                dept_name = data["department"]
                state_name = data["state"]
                state_obj = None
                if State.objects.filter(state=state_name).exists():
                    state_obj = State.objects.get(state=state_name)
                dept_obj = None
                if Department.objects.filter(dept_name=dept_name).exists():
                    dept_obj = Department.objects.get(dept_name=dept_name)

                serializer = PeopleSerializer(
                    obj, data=data, partial=True, context={"request": request}
                )
                if serializer.is_valid():
                    if len(project_objs) == 0:
                        serializer.save(state=state_obj, department=dept_obj)
                    else:
                        serializer.save(
                            state=state_obj, department=dept_obj, project=project_objs
                        )
                    return Response(serializer.data, status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

            elif "state" in data.keys():
                state_name = data["state"]
                state_obj = None
                if State.objects.filter(state=state_name).exists():
                    state_obj = State.objects.get(state=state_name)
                serializer = PeopleSerializer(
                    obj, data=data, partial=True, context={"request": request}
                )
                if serializer.is_valid():
                    if len(project_objs) == 0:
                        serializer.save(state=state_obj)
                    else:
                        serializer.save(state=state_obj, project=project_objs)
                    return Response(serializer.data, status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

            elif "department" in data.keys():
                dept_name = data["department"]
                dept_obj = None
                if Department.objects.filter(dept_name=dept_name).exists():
                    dept_obj = Department.objects.get(dept_name=dept_name)

                serializer = PeopleSerializer(
                    obj, data=data, partial=True, context={"request": request}
                )
                if serializer.is_valid():
                    if len(project_objs) == 0:
                        serializer.save(department=dept_obj)
                    else:
                        serializer.save(department=dept_obj, project=project_objs)
                    return Response(serializer.data, status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

            serializer = PeopleSerializer(
                obj, data=data, partial=True, context={"request": request}
            )
            if serializer.is_valid():
                if len(project_objs) == 0:
                    serializer.save()
                else:
                    serializer.save(project=project_objs)
                return Response(serializer.data, status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Person.DoesNotExist:
            return Response({"message": "User Not found"})
        except Exception as e:
            print("error section", str(e))
            return Response({"message": str(e)}, status.HTTP_404_NOT_FOUND)

    # @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id of a person'),
    #         },
    #         required=['id']
    #     )
    # )
    def delete(self, request, id):
        """
        DELETE method
        """
        try:
            obj = Person.objects.get(id=id)
            print(obj)
            obj.delete()
            return Response({"msg": "Data has been deleted"}, status.HTTP_200_OK)
        except:
            return Response({"msg": "User Not Found"}, status.HTTP_404_NOT_FOUND)


class ProjectAPI(APIView):
    """
    Project APIs
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "project",
                openapi.IN_QUERY,
                description="Project Name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "company",
                openapi.IN_QUERY,
                description="Company Name",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request):
        """
        Get project by its name
        """
        try:
            project_name = request.GET.get("project", None)
            company_name = request.GET.get("company", None)

            if project_name is not None and company_name is not None:

                query1 = Project.objects.filter(name__startswith=project_name)
                query2 = Project.objects.filter(company__startswith=company_name)
                diff = query1 & query2

                serializer = ProjectSerializer(diff, many=True)

                if not serializer.data:
                    return Response(
                        {"message": "Result Not Found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                return Response(serializer.data, status.HTTP_200_OK)

            elif project_name is not None:

                query = Project.objects.filter(name__startswith=project_name)
                serializer = ProjectSerializer(query, many=True)

                if not serializer.data:
                    return Response(
                        {"message": "Result Not Found"}, status.HTTP_404_NOT_FOUND
                    )

                return Response(serializer.data, status.HTTP_200_OK)

            elif company_name is not None:

                query = Project.objects.filter(company__startswith=company_name)
                serializer = ProjectSerializer(query, many=True)

                if not serializer.data:
                    return Response(
                        {"message": "Result Not Found"}, status.HTTP_404_NOT_FOUND
                    )

                return Response(serializer.data, status.HTTP_200_OK)

            else:
                print("else portion")
                query = Project.objects.all()
                serializer = ProjectSerializer(query, many=True)
                return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": "Something went wrong"}, status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(request_body=ProjectSerializer)
    def post(self, request):
        """
        To create new Project in database
        """
        try:
            data = request.data
            print(data)
            serializer = ProjectSerializer(data=data)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Something went wrong"}, status.HTTP_400_BAD_REQUEST
            )


class ProjectEditAPI(APIView):
    """
    Edit in Project API
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, id):
        """
        Get project by ID
        """
        try:
            print(id)
            obj = Project.objects.get(id=id)
            serializer = ProjectSerializer(obj)
            return Response(serializer.data, status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response({"message": "Project Not Found"}, status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response(
                {"msg": "Something went wrong"}, status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "Data": openapi.Schema(type=openapi.TYPE_STRING, description="Values"),
            },
            required=[],  # Specify required fields if any
        )
    )
    def patch(self, request, id):
        """
        patch request
        """
        try:
            print(id, request.data)
            obj = Project.objects.get(id=id)
            serializer = ProjectSerializer(
                obj,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Project.DoesNotExist:
            return Response({"message": "User Not Found"}, status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response(
                {"message": "Something went wrong"}, status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id):
        """
        Delete Project
        """
        try:
            obj = Project.objects.get(id=id)
            print(obj)
            obj.delete()
            return Response({"msg": "Data has been deleted"}, status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"msg": "User Not Found"}, status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(
                {"message": "Something went wrong"}, status.HTTP_400_BAD_REQUEST
            )


class AccountAPI(APIView):
    """
    Account APIs
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "MinSalary",
                openapi.IN_QUERY,
                description="Min Salary",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "MaxSalary",
                openapi.IN_QUERY,
                description="Max Salary",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "Orderby",
                openapi.IN_QUERY,
                description="asc / desc",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "mindate",
                openapi.IN_QUERY,
                description="From Date",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                "maxdate",
                openapi.IN_QUERY,
                description="to Date",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
        ]
    )
    def get(self, request):
        """
        GET METHOD
        """
        try:
            min_balance = request.GET.get("MinSalary", 0)
            max_balance = request.GET.get("MaxSalary", 999999999)
            order_direction = request.GET.get("Orderby", "asc")
            order_by = "balance"
            order_string = order_by if order_direction == "asc" else f"-{order_by}"
            objs = Account.objects.filter(
                balance__gte=min_balance, balance__lte=max_balance
            ).order_by(order_string)

            min_date = request.GET.get('mindate', None)
            if min_date is None:
                min_date = '2024-07-05'
            
            max_date = request.GET.get('maxdate', None)
            if max_date is None:
                max_date = str(date.today())
            
            start_date = datetime.strptime(min_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(max_date, '%Y-%m-%d').date()
            print("ohk")
            print(start_date, end_date)
            objs = objs.filter(DoJ__range=[start_date, end_date])

            page = request.GET.get("page", None)
            page_size = 3
            if page is None:
                page = 1
                page_size = 1000
            paginator = Paginator(objs, page_size)
            serializer = AccountSerializer(paginator.page(page), many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except EmptyPage:
            return Response({"message": "Page Not Found"}, status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(
                {"message": "Something Went Wrong"}, status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(request_body=request_account_body_schema)
    def post(self, request):
        """
        POST request
        """
        try:
            email = request.data.get("email")
            balance = request.data.get("balance")

            try:
                person_obj = Person.objects.get(email=email)
            except Person.DoesNotExist:
                return Response(
                    {"error": "Person with this email does not exist."},
                    status.HTTP_404_NOT_FOUND,
                )

            acc_obj = {"person": person_obj.id, "balance": balance, "DoJ": date.today()}

            serializer = AccountSerializer(data=acc_obj)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_400_BAD_REQUEST)


class AccountEditAPI(APIView):
    """
    Edit in Account by ID
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, id):
        """
        Get balance by ID
        """
        print(id)
        try:
            obj = Account.objects.get(id=id)
            serializer = AccountSerializer(obj)
            return Response(serializer.data, status.HTTP_200_OK)

        except Account.DoesNotExist:
            return Response({"message": "Account Not Found"}, status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response(
                {"message": "Something went wrong"}, status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "balance": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="numbers"
                ),
            },
            required=[],  # Specify required fields if any
        )
    )
    def patch(self, request, id):
        """
        Patch
        """
        try:
            print(id)
            acc_obj = Account.objects.get(id=id)
            serializer = AccountSerializer(acc_obj, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Account.DoesNotExist:
            return Response({"message": "User Not Found"}, status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response(
                {"message": "Something went wrong"}, status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id):
        """
        Delete Account
        """
        try:
            obj = Account.objects.get(id=id)
            print(obj)
            obj.delete()
            return Response({"msg": "Account has been deleted"}, status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"msg": "User Not Found"}, status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(
                {"message": "Something went wrong"}, status.HTTP_400_BAD_REQUEST
            )
