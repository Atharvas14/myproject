from tokenize import Triple
from django.shortcuts import render
from .forms import UserInput
from .models import Database, Shipment, Random, Neworder_database, Trip
import pandas as pd
import random
import json
from myapp.utils import distance
from django.shortcuts import render
from django.db.models import F, Max, Min, Count, Avg
from decimal import Decimal
from myapp import views
from django.core.paginator import Paginator

# Create your views here.
import csv


def csv_view(request):
    with open('myapp/static/numlocations.csv', 'r') as f:
        reader = csv.DictReader(f)
        # Database.objects.all().delete()
        for row in reader:
            obj = Database(
                no=row['num'],
                address=row['address'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                pincode=row['pincode'],
                timeslot=row['timeslot'],
            )
            obj.save()
            # print(data=Database.objects.all())
        return render(request, 'myapp/database.html', {'data': Database.objects.all()})


def random_output(request):
    df = pd.read_csv('myapp/static/numlocations.csv')
    random_sample = df.sample(n=50)
    random_sample['shipment_id'] = range(1, len(random_sample) + 1)
    random_list = random_sample.to_dict('records')
    Random.objects.all().delete()
    for row in random_list:
        obj = Random(
            order_no=row['num'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            pincode=row['pincode'],
            timeslot=row['timeslot'],
        )
        obj.save()
        # print(obj)
    return render(request, 'myapp/random.html', {'random_list': random_list})


def index(request):
    if request.method == 'POST':
        input = UserInput(request.POST)
        if input.is_valid():
            input.save()
            user_pincode = input.cleaned_data['pincode']
            user_address = input.cleaned_data['address']
            matching_records = Database.objects.filter(pincode=user_pincode, address__icontains=user_address).values(
                'no', 'address', 'latitude', 'longitude', 'pincode', 'timeslot')
            print(matching_records)
            return render(request, 'myapp/output.html', {'matching_records': matching_records})
    else:
        userinput_form = UserInput()
    return render(request, 'myapp/index.html', {'userinput_form': userinput_form})



# newcode
def create_trips(request):
    pincodes = Random.objects.values('pincode').distinct()
    timeslots = Random.objects.values('timeslot').distinct()
    shipments_data = []
    trip_count = {}
    num = 1

    for pincode in pincodes:
        for timeslot in timeslots:
            all_shipments = Random.objects.filter(
                pincode=pincode['pincode'], timeslot=timeslot['timeslot'])
            count = all_shipments.count()

            # Calculate trip capacity and create trips
            while count > 0:
                trip_capacity = min(15, count) / 15
                shipments = all_shipments[:15]
                all_shipments = all_shipments[15:]
                count = all_shipments.count()

                # Calculate trip details
                latitudes = []
                longitudes = []
                for shipment in shipments:
                    latitudes.append(shipment.latitude)
                    longitudes.append(shipment.longitude)
                latitude_avg = 0
                longitude_avg = 0
                if len(latitudes) > 0 and len(longitudes) > 0:
                    latitude_avg = sum(latitudes)/len(latitudes)
                    longitude_avg = sum(longitudes)/len(longitudes)
                max_distance = 0
                for shipment in shipments:
                    d = distance(shipment.latitude, shipment.longitude,
                                 latitude_avg, longitude_avg)
                    if d > max_distance:
                        max_distance = d

                radius = float("{:.2f}".format(max_distance))
                locations = []
                float_list = []
                for shipment in shipments:
                    if shipment.latitude and shipment.longitude:
                        locations.append(
                            [shipment.latitude, shipment.longitude])
                for inner_list in locations:
                    float_inner_list = [float(decimal)
                                        for decimal in inner_list]
                    float_list.append(float_inner_list)
                trip_score = float("{:.2f}".format(
                    ((0.5*len(shipments))-(0.5*radius))))
                trip_capacity = float("{:.2f}".format(trip_capacity))

                # Save trip details to shipments_data
                shipments_data.append({
                    'num': num,
                    'pincode': pincode['pincode'],
                    'timeslot': timeslot['timeslot'],
                    'shipments': shipments,
                    'count': len(shipments),
                    'radius': radius,
                    'trip_score': trip_score,
                    'latitudes': latitudes,
                    'longitudes': longitudes,
                    'float_list': float_list,
                    'trip_capacity': trip_capacity
                })
                num += 1

                # Save trip details to database
                obj = Neworder_database(
                    num=num,
                    pincode=pincode['pincode'],
                    timeslot=timeslot['timeslot'],
                    count=len(shipments),
                    radius=radius,
                    trip_score=trip_score,
                    trip_capacity=trip_capacity,
                    locations=float_list
                )
                obj.save()

    paginator = Paginator(shipments_data, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'myapp/shipment.html', {'shipments_data': page_obj})


def new_order(request):
    # Retrieve all previously shipped orders
    shipped_orders = list(Random.objects.values_list('order_no', flat=True))

    df = pd.read_csv('myapp/static/numlocations.csv')
    available_orders = df[~df['num'].isin(shipped_orders)]

    # Sample 5 orders from the available orders
    random_sample = available_orders.sample(n=5)
    random_sample['shipment_id'] = range(1, len(random_sample) + 1)

    random_list = random_sample.to_dict('records')

    # Save new random orders to the database
    for row in random_list:
        obj = Random(
            order_no=row['num'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            pincode=row['pincode'],
            timeslot=row['timeslot'],
        )
        obj.save()

    return render(request, 'myapp/new_order.html', {'random_list': random_list})
