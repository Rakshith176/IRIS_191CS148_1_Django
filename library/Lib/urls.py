from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='lib-home'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='Lib/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='Lib/logout.html'),name='logout'), 
    path('books/add',views.add_book,name='add_book'),
    path('books/all',views.all_books,name='all_books'),
    path('books/details<int:pk>',views.book_detail,name='book_detail'),
    path('books/update<int:pk>',views.book_update,name='book_update'),
    path('books/delete<int:pk>',views.book_delete,name='book_delete'),
    path('student/request<int:pk>',views.issue_request,name='issue_request'),
    path('books/requests',views.requests,name='requests'),
    path('books/approved<int:pk>',views.approve,name='approve'),
    path('books/rejected<int:pk>',views.reject,name='reject'),
    path('student/mybooks',views.mybooks,name='mybooks'),
    path('student/mybooks/return<int:pk>',views.return_book,name='return_book'),
    path('student/requested',views.requested,name='my_requests'),
    path('transactions',views.transactions,name='transactions'),
    path('transactions/download',views.csv_file,name='csv_file')

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
