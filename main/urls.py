from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^signup/', views.signup_view, name='signup'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^contest/round-1', views.r1, name='r1'),
    url(r'^contest/round-2', views.r2, name='r2'),
    url(r'^contest/', views.contest, name='contest'),
    url(r'^validate_spoj/', views.validate_spoj, name='validate_spoj'),
    url(r'^validate_hackerearth/', views.validate_hackerearth, name='validate_hackerearth'),
    url(r'^validate_codechef/', views.validate_codechef, name='validate_codechef'),
    url(r'^validate_compile/', views.validate_compile, name='validate_compile'),
    url(r'^validate_run/', views.validate_run, name='validate_run'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)