from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .models import Room, Reservation
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import Q
import stripe, json

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def index(request):
    rooms = Room.objects.filter(active=True).all()
    return render(request, 'index.html', {
        'rooms': rooms, 'STRIPE_TEST_KEY': settings.STRIPE_TEST_PUBLISHABLE_KEY})

def get_delta(start_date, end_date):
    date_format = '%Y-%m-%d'
    a = datetime.datetime.strptime(start_date, date_format)
    b = datetime.datetime.strptime(end_date, date_format)
    return (b - a).days
@csrf_exempt
def create_session(request):
    if request.method == "POST":
        data = json.loads(request.body)
        room = Room.objects.get(pk=data['room_id'])
        if Room.is_avaliable(data['start_date'], data['end_date'], room):
            return HttpResponse('not avaliable')
        delta = get_delta(data['start_date'], data['end_date'])
        price = room.amount_per_night * delta
        session = stripe.checkout.Session.create(
            submit_type="book",
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'{room.title} ({str(delta)} night stay; ${room.amount_per_night}/night)',
                    },
                    'unit_amount': price * 100,
                    },
                    'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/cancel',
        )
        reservation = Reservation(
            room=room,
            first_name=data['first_name'],
            last_name=data['last_name'],
            start_date=data['start_date'], 
            end_date=data['end_date'], 
            stripe_id=session.id
        )
        reservation.save()
        return JsonResponse(session)

def payment_success(request):
    return render(request, 'success.html')

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'checkout.session.completed':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        reservation = Reservation.objects.filter(stripe_id=payment_intent.id).first()
        reservation.status = 'paid'
        reservation.stripe_payment_intent = payment_intent.payment_intent
        reservation.save()

    
    return HttpResponse(status=200)

def check_availability(request):
    rooms = Room.objects.filter(active=True).all()
    if request.method == "POST":
        data = json.loads(request.body)
        av_rooms = []
        if data['room_id'] == 'any':
            for room in rooms:
                if not room.is_avaliable(data['start_date'], data['end_date'], room):
                    av_rooms.append(room.to_json())
        else:
            room = Room.objects.get(pk=data['room_id'])
            if not room.is_avaliable(data['start_date'], data['end_date'], room):
                av_rooms.append(room.to_json())
        return JsonResponse(av_rooms, safe=False)

    
    return render(request, 'check_availability.html', {'rooms': rooms})