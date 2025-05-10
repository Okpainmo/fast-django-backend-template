
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from django.http import JsonResponse

from . import views
from domain__auth.views import auth_router
from domain__user.views import user_router
from domain__admin.views import admin_router


api = NinjaAPI()

api.add_router("/v1/auth", auth_router)  
api.add_router("/v1/user", user_router)  
api.add_router("/v1/admin", admin_router)  

urlpatterns = [
    path("", views.index, name="index"),
    path('api/', api.urls), # do not include the ".py" extension

    # path('admin/', admin.site.urls),
]
