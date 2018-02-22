"""trainingportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
# from django.contrib.auth.models import User

from rest_framework.routers import DefaultRouter
# from rest_framework import routers
# from rest_framework import renderers
from rest_framework.schemas import get_schema_view

#from .views import SnippetViewSet, UserViewSet
from . import views

# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })

app_name = 'trainingportal'

# router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet)
# router.register(r'users', views.UserViewSet)

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    #url(r'^', include(router.urls)),
    # url(r'^schema/$', schema_view),
    # url(r'^', include(router.urls)),
    #url(r'^snippets/$', views.snippet_list),
    path('admin/', admin.site.urls),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', RedirectView.as_view(url='home/')),
    url(r'^home/', views.home, name='home'),
    url(r'^register/', views.register, name='register'),
    url(r'^trainings/', views.training, name='training'),
    url(r'^trainees/', views.trainees, name='trainees'),
    path('edit/<int:training_id>/', views.edit_training, name='edit_training'),
    path('delete_training/', views.delete_training, name='delete_training'),
    path('training_status/', views.update_training_status, name='update_training_status'),
    path('tasks/', views.tasks, name='tasks'),
    path('assignments/', views.assignments, name='assignments'),
    path('evaluate_assignment/<int:assignment_id>/', views.evaluate_assignment, name='evaluate_assignment'),
    path('submit_assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('enroll_training/', views.enroll_training, name='enroll_training'),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^contact/', views.contact_us),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)