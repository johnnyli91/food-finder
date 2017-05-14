# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import requests
from django.shortcuts import render
from rest_framework.views import APIView, Response
from food.models import Restaurant, Result
from food_finder.settings import GOOGLE_PLACES_API


def index(request):
    return render(request, '../static/templates/index.html')


class RandomRestaurantView(APIView):
    def get(self, request):
        user = request.user
        latitude = str(request.query_params['latitude'])
        longitude = str(request.query_params['longitude'])
        location = "{latitude},{longitude}".format(latitude=latitude, longitude=longitude)
        restaurant_dict = self.get_random_restaurant(location, user)
        return Response(restaurant_dict)

    def get_random_restaurant(self, location, user):
        SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        MAX_SEARCH_RADIUS = 500

        search_url = '{base_url}location={location}&radius={radius}&type=restaurant&key={api_key}'.\
            format(base_url=SEARCH_URL, location=location, radius=MAX_SEARCH_RADIUS, api_key=GOOGLE_PLACES_API)
        search_request = requests.get(search_url)
        search_result_json = search_request.json()
        restaurant_results = search_result_json['results']
        random_place_id = random.choice([restaurant['place_id'] for restaurant in restaurant_results])

        random_restaurant = self.get_restaurant_details(random_place_id, user)
        restaurant_dict = {'restaurant': random_restaurant}

        return restaurant_dict

    def get_restaurant_details(self, place_id, user):
        try:
            restaurant = Restaurant.objects.get(place_id=place_id)
        except Restaurant.DoesNotExist:
            DETAIL_URL = 'https://maps.googleapis.com/maps/api/place/details/json?'
            detail_url = '{detail_url}placeid={place_id}&key={api_key}'.\
                format(detail_url=DETAIL_URL, place_id=place_id, api_key=GOOGLE_PLACES_API)
            detail_request = requests.get(detail_url)
            detail_results = detail_request.json()['result']
            phone_number = detail_results['formatted_phone_number']
            name = detail_results['name']
            full_address = detail_results['formatted_address']
            split_address = full_address.split(', ')
            try:
                street_address = split_address[0]
                city = split_address[1]
                state, zip_code = split_address[2].split()
            except IndexError:
                street_address = city = state = zip_code = None
            try:
                photo_reference = detail_results['photos'][0]['photo_reference']
                photo = self.get_restaurant_photo(photo_reference)
            except KeyError:
                photo = None

            restaurant = Restaurant.objects.create(name=name, phone_number=phone_number,
                                                   street_address=street_address, city=city,
                                                   state=state, zip_code=zip_code, image=photo,
                                                   place_id=place_id)

        if user.is_authenticated():
            Result.objects.get_or_create(restaurant=restaurant, user=user)

        restaurant_details = {'name': restaurant.name,
                              'phone_number': restaurant.phone_number,
                              'street_address': restaurant.street_address,
                              'city': restaurant.city,
                              'state': restaurant.state,
                              'zip_code': restaurant.zip_code,
                              'image': restaurant.image,
                              'place_id': restaurant.place_id}
        return restaurant_details

    def get_restaurant_photo(self, photo_reference):
        PHOTO_URL = 'https://maps.googleapis.com/maps/api/place/photo?'
        PHOTO_WIDTH = 400
        photo_url = '{photo_url}maxwidth={width}&photoreference={photo_reference}&key={api_key}'.\
            format(photo_url=PHOTO_URL, width=PHOTO_WIDTH, photo_reference=photo_reference, api_key=GOOGLE_PLACES_API)
        photo_request = requests.get(photo_url)
        return photo_request.url


class PreviousResultView(APIView):
    def get(self, request):
        user = request.user
        previous_results = Result.objects.filter(user=user).select_related('restaurant')
        result_dict = {'data': {}}

        for result in previous_results:
            location = "{state} - {city}".format(state=result.restaurant.state, city=result.restaurant.city)
            result_data = {
                'restaurant_name': result.restaurant.name,
                'result_id': result.id,
                'rating': result.rating
            }
            try:
                result_dict['data'][location].append(result_data)
            except KeyError:
                result_dict['data'][location] = [result_data]

        if previous_results:
            result_dict['has_results'] = True
        else:
            result_dict['has_results'] = False

        return Response(result_dict)


class ResultDetailView(APIView):
    def get(self, request):
        user = request.user
        result_id = int(request.query_params['result_id'])
        response_dict = {}
        try:
            previous_result = Result.objects.select_related('restaurant').get(id=result_id, user=user)
        except Result.DoesNotExist:
            previous_result = None

        if not previous_result:
            response_dict['success'] = False
        else:
            response_dict['success'] = True
            response_dict['data'] = {
                'name': previous_result.restaurant.name,
                'phone_number': previous_result.restaurant.phone_number,
                'street_address': previous_result.restaurant.street_address,
                'city': previous_result.restaurant.city,
                'state': previous_result.restaurant.state,
                'zip_code': previous_result.restaurant.zip_code,
                'image': previous_result.restaurant.image,
                'place_id': previous_result.restaurant.place_id,
                'rating': previous_result.rating,
                'result_id': previous_result.id
            }
        return Response(response_dict)

    def post(self, request):
        response_dict = {}
        user = request.user
        result_id = int(request.data['result_id'])
        rating = int(request.data['rating'])

        try:
            result = Result.objects.get(id=result_id, user=user)
            result.rating = rating
            result.save()
            response_dict['success'] = True
        except Result.DoesNotExist:
            response_dict['success'] = False

        return Response(response_dict)
