import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateProductAPIView(APIView):
    """Создание продукта для оплаты"""

    def post(self, request):
        try:
            product = stripe.Product.create(name=request.data["name"])
            return Response(product, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class CreatePriceAPIView(APIView):
    """Создание цены для продукта"""

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
