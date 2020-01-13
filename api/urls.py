from django.urls import path, include

urlpatterns = [
    path('fixture/', include('cricket_app.urls')),
]
