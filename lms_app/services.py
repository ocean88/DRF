import stripe
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateProductAPIView(APIView):
    """Создание продукта для оплаты"""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the product')
            }
        ),
        responses={
            201: openapi.Response('Product created successfully', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the product'),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the product'),
                }
            )),
            400: 'Bad request'
        }
    )
    def post(self, request):
        try:
            product = stripe.Product.create(name=request.data["name"])
            return Response(product, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class CreatePriceAPIView(APIView):
    """Создание цены для продукта"""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the product'),
                'unit_amount': openapi.Schema(type=openapi.TYPE_INTEGER, description='Unit amount in cents')
            }
        ),
        responses={
            201: openapi.Response('Price created successfully', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the price'),
                    'unit_amount': openapi.Schema(type=openapi.TYPE_INTEGER, description='Unit amount in cents'),
                }
            )),
            400: 'Bad request'
        }
    )
    def post(self, request):
        try:
            price = stripe.Price.create(
                product=request.data["product_id"],
                unit_amount=request.data["unit_amount"],
                currency="usd",
            )
            return Response(price, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class CreateCheckoutSessionAPIView(APIView):
    """Передать ссылку на оплату"""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'success_url': openapi.Schema(type=openapi.TYPE_STRING, description='URL to redirect after success'),
                'cancel_url': openapi.Schema(type=openapi.TYPE_STRING, description='URL to redirect after cancel'),
                'price_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the price'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity of items')
            }
        ),
        responses={
            201: openapi.Response('Checkout session created successfully', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the session'),
                    'url': openapi.Schema(type=openapi.TYPE_STRING, description='URL of the checkout session'),
                }
            )),
            400: 'Bad request'
        }
    )
    def post(self, request):
        try:
            session = stripe.checkout.Session.create(
                success_url=request.data["success_url"],
                cancel_url=request.data["cancel_url"],
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": request.data["price_id"],
                        "quantity": request.data["quantity"],
                    }
                ],
                mode="payment",
            )
            return Response(session, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
