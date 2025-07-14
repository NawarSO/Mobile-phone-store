from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from .models import User, Mobile, Cart, CartItem, Order, PhoneSpecs
from .serializers import UserSerializer, MobileSerializer, CartSerializer, OrderSerializer, PhoneSpecsSerializer
from .ai_service.predict import evaluate_price

class PhoneEvaluationViewSet(viewsets.ModelViewSet):
    queryset = PhoneSpecs.objects.all()
    serializer_class = PhoneSpecsSerializer

    @action(detail=False, methods=['post'], url_path='evaluate')
    def evaluate_phone(self, request):
        """
        Evaluate phone price based on specifications
        The Required parameters:
         brand: string 
        ram: string 
         storage: string
             screen_size: string
        """
        try:
            # Validate  fields
            required_fields = ['brand', 'ram', 'storage', 'screen_size']
            if not all(field in request.data for field in required_fields):
                missing = [f for f in required_fields if f not in request.data]
                return Response(
                    {'error': f'Missing required fields: {missing}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get price evaluation
            price = evaluate_price({
                'brand': request.data['brand'],
                'ram': request.data['ram'],
                'storage': request.data['storage'],
                'screen_size': request.data['screen_size']
            })

            if price is None:
                return Response(
                    {'error': 'Price evaluation failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Save evaluation to the db
            evaluation = PhoneSpecs.objects.create(
                brand=request.data['brand'],
                ram=request.data['ram'],
                storage=request.data['storage'],
                screen_size=request.data['screen_size'],
                estimated_price=price,
                user=request.user if request.user.is_authenticated else None
            )

            return Response({
                'price': price,
                'evaluation_id': evaluation.id
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )       

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        
        pass

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})

    @action(detail=True, methods=['put'])
    def manage_profile(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class MobileViewSet(viewsets.ModelViewSet):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer

    @action(detail=False, methods=['get'])
    def filter(self, request):
        brand = request.query_params.get('brand', None)
        if brand:
            mobiles = Mobile.objects.filter(brand__iexact=brand)
            serializer = self.get_serializer(mobiles, many=True)
            return Response(serializer.data)
        return Response([])

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        mobile = self.get_object()
        quantity = request.data.get('quantity')
        if quantity is not None:
            mobile.quantity = quantity
            mobile.save()
            return Response({'status': 'stock updated'})
        return Response({'error': 'quantity not provided'}, status=status.HTTP_400_BAD_REQUEST)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        mobile_id = request.data.get('mobile_id')
        quantity = request.data.get('quantity', 1)
        
        mobile = get_object_or_404(Mobile, pk=mobile_id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            mobile=mobile,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
            
        return Response({'status': 'item added to cart'})

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        mobile_id = request.data.get('mobile_id')
        CartItem.objects.filter(cart=cart, mobile_id=mobile_id).delete()
        return Response({'status': 'item removed from cart'})

    @action(detail=True, methods=['get'])
    def calculate_total(self, request, pk=None):
        cart = self.get_object()
        return Response({'total': cart.calculate_total()})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request):
        cart_id = request.data.get('cart_id')
        cart = get_object_or_404(Cart, pk=cart_id, user=request.user)
        
        if Order.objects.filter(cart=cart).exists():
            return Response({'error': 'Order already exists for this cart'}, status=status.HTTP_400_BAD_REQUEST)
            
        total = cart.calculate_total()
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            total_amount=total
        )
        
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.cancel_order()
        return Response({'status': 'order cancelled'})