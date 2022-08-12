import stripe 
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt # new

from products.models import Price, Product

stripe.api_key = settings.STRIPE_SECRET_KEY

class CollectionsView(TemplateView):
    template_name = "landing.html"
    
    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Summer Series")
        prices = Price.objects.filter(product=product)
        context = super(CollectionsView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices
        })
        return context

def success_view(request):
	return render(request, "success.html")

def cancel_view(request):
	return render(request, "cancel.html")

class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=settings.BASE_URL + '/collections/success/',
            cancel_url=settings.BASE_URL + '/collections/cancel/',
        )
        return redirect(checkout_session.url)

@csrf_exempt
def create_checkout_session(request):
    print('hello')
    YOUR_DOMAIN = "https://127.0.0.1:8000"
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1LVyLbEh2FpKEa7eQkGjYrjx',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)
    print(checkout_session.url)
    return redirect(checkout_session.url, code=303)

    