from django.conf.urls import url
from food.views import RandomRestaurantView, PreviousResultView, ResultDetailView

urlpatterns = [
    url(r'^random/$', RandomRestaurantView.as_view()),
    url(r'^previous_result/$', PreviousResultView.as_view()),
    url(r'^result_detail/$', ResultDetailView.as_view())
]
