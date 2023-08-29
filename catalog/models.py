from django.db import models
from django.urls import reverse
import uuid  # Required for unique book instances
from django.utils.translation import gettext
# Create your models here.


class Genre(models.Model):
    """Model representing a book genre"""
    name = models.CharField(
        max_length=20, help_text=gettext('Enter a book genre'))

    def __str__(self):
        """String for representing the Model object"""
        return self.name


class Book(models.Model):
    """Model representing a book"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text=gettext('Brief discussion of the book'))
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text=gettext('13 characters <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'))
    genre = models.ManyToManyField(
        Genre, help_text=gettext('Select a genre for this book'))

    def __str__(self):
        """Return book title"""
        return self.title

    def get_absolute_url(self):
        """Return url to access details of this book"""
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific copy of the book"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text=gettext('Unique ID for the book'))
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text=gettext('Book availability')
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object"""
        return f'{self.id}({self.book.title})'


class Author(models.Model):
    """Model for representing an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
