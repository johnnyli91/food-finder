from django.conf.urls import url
from food.views import RandomRestaurantView

urlpatterns = [
    url(r'^random/$', RandomRestaurantView.as_view())
]
