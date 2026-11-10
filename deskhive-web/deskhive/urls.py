from django.urls import include, path

urlpatterns = [
    path("api/", include("api_m6.urls")),
    path("rpc/", include("partner_m7.urls")),
    path("", include("spaces.urls")),
    path("bookings/", include("bookings.urls")),
]
