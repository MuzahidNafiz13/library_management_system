from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='books/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Borrow {self.id} by {self.user.username}"

# class Comment(models.Model):
#     book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='comments')
#     name = models.CharField(max_length=100)
#     text = models.TextField()

#     def __str__(self):
#         return f"{self.name} on {self.book}"

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'{self.user.username} on {self.book}'
