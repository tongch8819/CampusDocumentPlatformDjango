from django.urls import path
from .views import MaterialUploadView, MaterialListView, ToggleFavoriteView, UpdateSharingView, MaterialDetailView, MaterialDeleteView

urlpatterns = [
    path('upload/', MaterialUploadView.as_view(), name='material-upload'),
    path('list/', MaterialListView.as_view(), name='material-list'),
    path('<int:material_id>/favorite/', ToggleFavoriteView.as_view(), name='toggle-favorite'),
    path('<int:material_id>/share/', UpdateSharingView.as_view(), name='update-sharing'),
    
    # New detail endpoint:
    path('<int:pk>/', MaterialDetailView.as_view(), name='material-detail'),
    path('<int:pk>/delete/', MaterialDeleteView.as_view(), name='material-delete'),
]