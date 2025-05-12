from django.shortcuts import render

# Create your views here.
from ninja import Router, Schema

auth_router = Router()


@auth_router.get("/")
def auth_base(request):
    return {"message": "Hello, world! - Auth domain is live!!!"}
