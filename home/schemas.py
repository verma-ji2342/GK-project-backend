"""
Schemas
"""

from drf_yasg import openapi

request_body_put_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
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
    required=['name', 'email', 'age', 'pincode', 'department', 'address', 'state']
)



request_account_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
        'balance': openapi.Schema(type=openapi.TYPE_INTEGER, description='INR'),
    },
    required=['email', 'balance']
)


person_post_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'state': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'state': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        'department': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'dept_name': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        'project': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_INTEGER)
        ),
        'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
        'name': openapi.Schema(type=openapi.TYPE_STRING),
        'age': openapi.Schema(type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64),
        'pincode': openapi.Schema(type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64),
        'address': openapi.Schema(type=openapi.TYPE_STRING)
    }
)