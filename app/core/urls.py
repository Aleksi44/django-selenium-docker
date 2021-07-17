from django.urls import path
from app.core.consumers import TaskConsumer


websocket_urlpatterns = [
    path('ws/task/<key_composer>/', TaskConsumer.as_asgi()),
]
