from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Phone, Order
from .serializers import PhoneSerializer, OrderSerializer, UserRegistrationSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    # Suggestion: You can add pagination, filtering, or search if needed.

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(customer=user)
        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
        # Suggestion: You may want to handle exceptions or add logging here.

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        # Return serializer fields or a simple message
        return Response({"detail": "Send a POST request to register a new user."}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can view all users