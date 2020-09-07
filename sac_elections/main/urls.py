from django.urls import path, include

from . import views

urlpatterns = [
  # /
  path('', views.home, name='home'),
  # TEMPORARY
  path('signin', views.sign_in, name='signin'),
  path('signout', views.sign_out, name='signout'),
  path('callback', views.callback, name='callback'),
  path('vote/', include([
  		path('', views.vote, name='vote'),
  		path('<category>/', include([
  				path('', views.poll, name='poll'),
				path('confirmation', views.confirmation, name='confirmation'),
  			])),
  	])),
  path('manifesto', views.manifesto, name='manifesto'),
  path('dashboard', views.dashboard, name='dashboard'),
  path('confhash', views.confhash, name = 'confhash'),
]

#path('confirmation', views.confirmation, name='confirmation'),