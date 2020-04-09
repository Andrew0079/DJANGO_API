from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # backend: urls of the API

    # oauth2
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('authentication/', include('oAuth2Server.urls')),

    # API of the Item's end points
    path('api/', include('api_market.items.urls')),

    # API of the Auction's end points
    path('api/', include('api_market.auction.urls')),

    # API of the Bidding's end points
    path('api/', include('api_market.bidding.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
