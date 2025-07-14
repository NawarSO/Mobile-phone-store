from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MobileViewSet, CartViewSet, OrderViewSet, PhoneEvaluationViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'mobiles', MobileViewSet)
router.register(r'carts', CartViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'phone-evaluations', PhoneEvaluationViewSet, basename='phone-evaluation')
urlpatterns = [
    path('', include(router.urls)),
]