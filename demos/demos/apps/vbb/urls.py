# File: urls.py

from django.conf.urls import include, url
from demos.common.utils import base32cf
from demos.apps.vbb import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^vote/$', views.VoteView.as_view(), name='vote'),
    url(r'^qrcode/$', views.QRCodeScannerView.as_view(), name='qrcode'),
    url(r'^(?P<election_id>[' + base32cf._valid_re + r']+)/(?P<vote_token>[' \
        + base32cf._valid_re + r']+)/$', views.VoteView.as_view(), name='vote'),
]

apipatterns = [
    url(r'^setup/$', views.ApiSetupView.as_view(), name='setup'),
    url(r'^update/$', views.ApiUpdateView.as_view(), name='update'),
]

