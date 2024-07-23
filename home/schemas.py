"""
Schemas
"""

from drf_yasg import openapi

request_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Age'),
        'pincode': openapi.Schema(type=openapi.TYPE_INTEGER, description='Pincode'),
        'department': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'dept_name': openapi.Schema(type=openapi.TYPE_STRING, description='Department Name')
            }
        ),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address'),
        'state': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'state': openapi.Schema(type=openapi.TYPE_STRING, description='State Name')
            }
        )
    },
    required=['id', 'name', 'email', 'age', 'pincode', 'department', 'address', 'state']
)