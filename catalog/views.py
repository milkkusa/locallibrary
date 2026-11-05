import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import RenewBookForm
from .models import Author, Book, BookInstance, Genre, Language

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()
    num_genres = Genre.objects.all().count()
    num_books_python = Book.objects.filter(title__icontains='python').count()
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
        request,
        'index.html',
        context={
            'num_books':num_books,
            'num_instances':num_instances,
            'num_instances_available':num_instances_available,
            'num_authors':num_authors,
            'num_genres': num_genres,
            'num_books_python': num_books_python,
            'num_visits': num_visits,
        },
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10 # Постраничный вывод по 10 авторов

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'  # Требуем права библиотекаря
    template_name = 'catalog/bookinstance_list_borrowed_all.html' # Новый шаблон
    context_object_name = 'bookinstance_list' # Имя переменной для шаблона

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})

class LanguageCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_language'
    model = Language
    fields = ['name']
    success_url = reverse_lazy('languages')

class LanguageUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_language'
    model = Language
    fields = ['name']
    success_url = reverse_lazy('languages')

class LanguageListView(generic.ListView):
    model = Language
    paginate_by = 10

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

class GenreCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_genre'
    model = Genre
    fields = ['name']
    success_url = reverse_lazy('genres')

class GenreUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_genre'
    model = Genre
    fields = ['name']
    success_url = reverse_lazy('genres')

class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 10

class LanguageCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_language'
    model = Language
    fields = ['name']
    success_url = reverse_lazy('languages')

class LanguageUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_language'
    model = Language
    fields = ['name']
    success_url = reverse_lazy('languages')

class LanguageListView(generic.ListView):
    model = Language
    paginate_by = 10