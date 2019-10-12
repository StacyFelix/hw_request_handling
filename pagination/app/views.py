from django.core.paginator import Paginator
from django.shortcuts import render_to_response, redirect
from django.urls import reverse
import csv
from .settings import BUS_STATION_CSV
from urllib.parse import urlencode


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    count = 1000
    list_bus_station = []
    with open(BUS_STATION_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = {'Name': row['Name'], 'Street': row['Street'], 'District': row['District']}
            list_bus_station.append(item)

    #количество записей:
    print(len(list_bus_station)) #10803

    current_number_page = int(request.GET.get('page', 1))
    paginator = Paginator(list_bus_station, count)
    current_page = paginator.get_page(current_number_page)
    data_current_page = current_page.object_list

    if current_page.has_next():
        params = {'page': str(current_page.next_page_number())}
        next_page_url = '?'.join((reverse('bus_stations'), urlencode(params)))
    else:
        next_page_url = None

    if current_page.has_previous():
        params = {'page': str(current_page.previous_page_number())}
        previous_page_url = '?'.join((reverse('bus_stations'), urlencode(params)))
    else:
        previous_page_url = None
    return render_to_response('index.html', context={
        'bus_stations': data_current_page,
        'current_page': current_number_page,
        'prev_page_url': previous_page_url,
        'next_page_url': next_page_url,
    })

