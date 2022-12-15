from django.urls import include, re_path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView 

urlpatterns = [
    re_path('^$',views.index,name='index'),
    # re_path('accounts/register/', views.registration, name='register'),
    # re_path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    re_path('^search/', views.search_results, name='search_results'),
    # re_path('pharmacy/(\d+)',views.pharm_details,name='pharm_details'),
    # re_path('profile', views.profile, name='profile'),
    # re_path('drug/(\d+)',views.get_details,name='get_details'),
    # re_path('about',views.about_us,name='about'),
    # re_path('pharma',views.pharmacies,name='pharma'),
    

   
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)