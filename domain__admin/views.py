from django.shortcuts import render

# Create your views here.
from ninja import Router, Schema

admin_router = Router()


@admin_router.get("/")
def admin_base(request):
    return {"message": "Hello, world! - Admin domain is live!!!"}
