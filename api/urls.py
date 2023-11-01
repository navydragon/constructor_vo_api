from django.urls import include, path


urlpatterns = [
    path('auth/', include('dj_rest_auth.urls'))
]