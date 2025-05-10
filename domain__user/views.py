from django.shortcuts import render

# Create your views here.
from ninja import Router, Schema

user_router = Router()

@user_router.get("/")
def user_base(request):
    return {"message": "Hello, world! - User domain is live!!!"}