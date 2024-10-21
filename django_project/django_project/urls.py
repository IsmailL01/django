from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path('', include('members.urls')),
    # path('',include('websocket.urls')),
    path('snake',include('snake.urls'))
    # path('admin/', admin.site.urls),
]