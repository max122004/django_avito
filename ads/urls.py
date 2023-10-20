from django.urls import path

from ads import views

urlpatterns = [
    path('cat/', views.CategoryListView.as_view()),
    path('ad/', views.AdListView.as_view()),
    path('ad/<int:pk>/', views.AdDetailView.as_view()),
    path('ad/create/', views.AdCreateView.as_view()),
    path('ad/<int:pk>/update/', views.AdUpdateView.as_view()),
    path('ad/<int:pk>/delete/', views.AdDeleteView.as_view()),
    path('ad/<int:pk>/upload_image/', views.AdUploadImageView.as_view()),
    path('like/create/', views.LikeCreateView.as_view()),
    path('liked/', views.LikedAdAPIView.as_view()),
    path('comment/create/', views.CommentCreateView.as_view())
]