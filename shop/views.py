from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework import generics
from .models import Phone, Order
from .serializers import PhoneSerializer, OrderSerializer, UserRegistrationSerializer

# Create your views here.
class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # Customers see only their orders
        if self.request.user.is_authenticated:
            return Order.objects.filter(customer=self.request.user)
        return Order.objects.none()
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]