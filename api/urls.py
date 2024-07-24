"""
urls.py
"""
# pylint: disable-all
from home.views import testingAPI,RegisterAPI, LoginAPI, LogoutAPI, EditPersonAPI
from django.urls import path, include
# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'person', PersonViewSet)
# router.register(r'department', AddressViewSet)
# router.register(r'address', DepartmentViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('login/', LoginAPI.as_view()),
    path('person/', testingAPI.as_view()),
    path('register/', RegisterAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('people/<int:id>/', EditPersonAPI.as_view()),
]