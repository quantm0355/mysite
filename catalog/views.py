from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    """View function for home page of site."""
    # generate counts of some of the main objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits
    }  # Render the HTML template index.html with the data in the context variablereturn render(request, 'index.html', context=context)
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'  # your own name for the list as a template
    variablequeryset = Book.objects.filter(title__icontains='Anh')[
        :5]  # Get 5 books containing the title war


class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})
