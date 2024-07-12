from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from users.models import Profile
from .models import Book, Category, Borrow
from .forms import CommentForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

class HomeView(View):
    def get(self, request):
        categorys = Category.objects.all()
        books = Book.objects.all()
        selected_category = request.GET.get('category')
        if selected_category:
            books = books.filter(category__name=selected_category)
        context = {
            'categorys': categorys,
            'books': books,
        }
        return render(request, 'books/home.html', context)

# class BookDetailView(View):
#     def get(self, request, pk):
#         book = get_object_or_404(Book, pk=pk)
#         form = CommentForm()
#         context = {
#             'book': book,
#             'form': form,
#         }
#         return render(request, 'books/book_details.html', context)

#     def post(self, request, pk):
#         book = get_object_or_404(Book, pk=pk)
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.book = book
#             comment.save()
#             return redirect('book-detail', pk=book.pk)
#         context = {
#             'book': book,
#             'form': form,
#         }
#         return render(request, 'books/book_detail.html', context)

class BookDetailView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = CommentForm()
        comments = book.comments.all() 
        context = {
            'book': book,
            'form': form,
            'comments': comments,
        }
        return render(request, 'books/book_detail.html', context)

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.user = request.user
            comment.save()

            send_mail(
                'New Comment Added',
                f'Thank you for commenting on the book: {book.title}',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )

            return redirect('book-detail', pk=book.pk)
        
        comments = book.comments.all()
        context = {
            'book': book,
            'form': form,
            'comments': comments,
        }
        return render(request, 'books/book_detail.html', context)

    
@method_decorator(login_required, name='dispatch')
class BorrowBookView(View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        user = request.user

        if book.quantity > 0 and user.profile.balance >= book.price:
            borrow = Borrow(user=user, book=book)
            borrow.save()

            user.profile.balance -= book.price
            user.profile.save()

            book.quantity -= 1
            book.save()

            send_mail(
                'Book Borrowed Successfully',
                f'You have successfully borrowed the book "{book.title}". Your remaining balance is {user.profile.balance}.',
                'nafizuop@gmail.com',
                [user.email],
                fail_silently=False,
            )

            return redirect('profile')
        else:
            return render(request, 'users/insufficient_balance.html')
    
@method_decorator(login_required, name='dispatch')
class ReturnBookView(View):
    def post(self, request, pk):
        borrow = get_object_or_404(Borrow, pk=pk, user=request.user)
        book = borrow.book
        profile = request.user.profile
        profile.balance += book.price
        profile.save()
        book.quantity += 1
        book.save()
        borrow.delete()
        messages.success(request, f'Book "{book.title}" returned successfully.')
        return redirect('profile')
    
@method_decorator(login_required, name='dispatch')
class BorrowHistoryView(View):
    def get(self, request):
        borrows = Borrow.objects.filter(user=request.user)
        context = {
            'borrows': borrows,
        }
        return render(request, 'books/borrow_history.html', context)
