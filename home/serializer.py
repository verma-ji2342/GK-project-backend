from rest_framework import serializers
from .models import Person, Department, State
from django.contrib.auth.models import User


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ["dept_name"]

    def validate_dept_name(self, dept_name):
        if not Department.objects.filter(dept_name=dept_name).exists():
            raise serializers.ValidationError(
                {"message": "Department name is not exist in DataBase", "status": False}
            )
        return dept_name


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["state"]

    def validate_state(self, state):
        if not state.objects.filter(state=state).exists():
            raise serializers.ValidationError(
                {"message": "State is invalid", "status": False}
            )
            return None
        return state


class PeopleSerializer(serializers.ModelSerializer):

    country = serializers.SerializerMethodField()
    state = StateSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Person
        fields = [
            "id",
            "name",
            "email",
            "age",
            "pincode",
            "department",
            "address",
            "state",
            "country",
        ]
        depth = 1

    def validate_age(self, age):
        if age < 18:
            raise serializers.ValidationError("Age should be greater than 17")

        return age

    def validate_name(self, name):
        specialcharacter = "!@#$%%^&*(:)"
        if any(c in specialcharacter for c in name):
            raise serializers.ValidationError(
                "Name should not contain any special character"
            )

        return name

    def get_country(self, data):
        return "India"

    def validate_email(self, email):
        request = self.context.get('request')
        print(request)
        print("request method ", request.method)
        if request and request.method == 'POST':
            if Person.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"email": "Email is already registered by another user", "satus": False}
                )
        return email


class LoginSerializer(serializers.Serializer):
    """
    email verification
    """

    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    """
    register
    """

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """
        validation for an user
        """
        if data["username"]:
            if User.objects.filter(username=data["username"]).exists():
                raise serializers.ValidationError("Username is taken")

        if data["email"]:
            if User.objects.filter(email=data["email"]).exists():
                raise serializers.ValidationError("Email is already taken by user")

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        # you can use
        # user.set_password(validated_data['password'])
        print(validated_data)
        return validated_data


class LogoutSerializer:
    pass