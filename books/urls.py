from django.urls import path
from .views import HomeView, BookDetailView, BorrowBookView, BorrowHistoryView, ReturnBookView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('borrow/<int:pk>/', BorrowBookView.as_view(), name='borrow-book'),
    path('borrow-history/', BorrowHistoryView.as_view(), name='borrow-history'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
]
