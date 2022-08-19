import stripe 
from django.core.mail import send_mail 
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt # new
from django.http import HttpResponse

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
            'quantity': 1,
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
                    'adjustable_quantity': {
                        'enabled': True,
                        'minimum': 1,
                        'maximum': 10,
                    },
                },
            ],
            mode='payment',
            success_url=settings.BASE_URL + '/collections/success/',
            cancel_url=settings.BASE_URL + '/collections/cancel/',
            # consent_collection={
            #     'promotions': 'auto',
            # },
        )
        return redirect(checkout_session.url)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    # For now, you only need to print out the webhook payload so you can see
    # the structure.
    print(payload)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["medtadata"]["product_id"]
        
        send_mail(
            subject="Your YCCLA Purchase!",
            message="Thank you for your purchase. Your product is below and will be processed and shipped within 3-5 business days.",
            recipeient_list=[customer_email], 
            from_email="youcancookliterallyanything@gmail.com"
        )


    return HttpResponse(status=200)
  
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

    
