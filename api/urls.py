from django.urls import path, include
from .views import CreateUserView, LoginView, ScrapeDetailView, ScrapeView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', CreateUserView.as_view()),
    path('scrape/', ScrapeView.as_view()),
    path('get_scrape_data/', ScrapeDetailView.as_view())
]
