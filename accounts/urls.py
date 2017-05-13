from django.conf.urls import url
from accounts.views import login_view, logout_view, sign_up

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^signup/$', sign_up, name='sign_up')
]
