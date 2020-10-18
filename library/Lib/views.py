from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime,csv

def home(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = Student_register(request.POST)
        profile_form = Student_Profile(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = Student_register()
        profile_form = Student_Profile()
    return render(request, 'Lib/register.html', locals())



@login_required
def add_book(request):
    if not request.user.is_superuser:
        messages.warning(request,f'You dont have access')
        return redirect('lib-home')
    form = Add_Book(request.POST)
    if request.method == 'POST':
        form = Add_Book(data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book added successfully')
            return redirect('all_books')
    return render(request, 'Lib/admin/add_book.html', locals())


def all_books(request):
    # MODELNAME.objects.all() is used to get all objects from database
    book_list = Book.objects.order_by('-pk')
    return render(request, 'Lib/all_books.html', locals())


def book_detail(request, pk):
    book = get_object_or_404(Book, id = pk)
    return render(request, 'Lib/book_detail.html', locals())


@login_required
def book_update(request, pk):
    if not request.user.is_superuser:
        messages.warning(request,f'You dont have access')
        return redirect('lib-home')
    obj = Book.objects.get(id = pk)
    form = Add_Book(instance = obj)
    if request.method == 'POST':
        form = Add_Book(data = request.POST, instance = obj)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.save()
            messages.success(request, f'Book has been updated')
            return redirect('all_books')
    return render(request, 'Lib/admin/book_update.html', locals())



@login_required
def book_delete(request, pk):
    if not request.user.is_superuser:
        messages.warning(request,f'You dont have access')
        return redirect('lib-home')
    obj = get_object_or_404(Book, pk = pk)
    obj.delete()
    messages.warning(request, f'Book has been deleted')
    return redirect('all_books')


@login_required
def issue_request(request,pk):
    obj = Book.objects.get(id = pk)
    stud = User.objects.get(id = request.user.id)
    check_req = Status.objects.filter(book_id = obj)
    check_req = check_req.filter(stud_id = stud)
    pending_req = check_req.filter(req = 'pending').exists()
    approved_req = check_req.filter(req = 'approved').exists()

    if pending_req:
        messages.warning(request, f'Request already sent')
    elif approved_req:
        messages.warning(request, f'Book already approved')
    else:
        create_req = Status()
        create_req.stud_id = stud
        create_req.book_id = obj
        create_req.req = 'pending'
        create_req.save()
        messages.success(request, f'Request sent')
    return redirect('all_books')


@login_required
def requests(request):
    if not request.user.is_superuser:
        messages.warning(request,f'You dont have access')
        return redirect('lib-home')
    pending = Status.objects.filter(req='pending')
    approved = Status.objects.filter(req='approved')
    rejected = Status.objects.filter(req='rejected')
    return render(request,'Lib/admin/requests.html',locals())



@login_required
def approve(request,pk):
    if not request.user.is_superuser:
        messages.warning(request,f'You dont have access')
        return redirect('lib-home')
    approval = Status.objects.get(id=pk)
    approval.req = 'approved'
    book_pk = approval.book_id.id
    book = Book.objects.get(id=book_pk)
    book.Quantity = book.Quantity - 1
    approval.issue_date = datetime.datetime.now()
    book.save()
    approval.save()
    messages.success(request, f'Book approved')
    return redirect('requests')

@login_required
def mybooks(request):
    books_approved = Status.objects.filter(req='approved')
    books_approved = books_approved.filter(stud_id=request.user.id)
    return render(request,"Lib/student/mybooks.html",locals())


@login_required
def reject(request,pk):
    if not request.user.is_superuser:
        messages.warning(request,f'You dont have access')
        return redirect('lib-home')
    reject = Status.objects.get(id=pk)
    reject.req ='rejected'
    reject.save()
    messages.warning(request, f'Request Rejected')
    return redirect('requests')

@login_required
def return_book(request,pk):
    return_book = Status.objects.get(id=pk)
    if return_book.req == 'approved':
        return_book.req = 'none'
        book_pk = return_book.book_id.id
        book = Book.objects.get(id=book_pk)
        book.Quantity = book.Quantity + 1
        return_book.return_date = datetime.datetime.now()
        return_book.save()
        book.save()
        messages.success(request, f'Book returned successfully ')
        return redirect('mybooks')
    else:
        return HttpResponse('<H1>Invalid access</H1>')


def transactions(request):
    if request.user.is_superuser:
        completed_transaction = Status.objects.exclude(return_date = None)
    else:
        student = User.objects.get(id = request.user.id)
        completed_transaction = Status.objects.filter(stud_id=student)
        completed_transaction = completed_transaction.exclude(return_date = None)    
    return render(request,"Lib/transactions.html",locals())


def csv_file(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename = Transactions_on_' + str(datetime.datetime.now()) + '.csv'
        
        writer = csv.writer(response)
        writer.writerow(['Book','Student','Issue date','Return date','Duration'])

        transactions = Status.objects.exclude(return_date = None)

        for transaction in transactions:
            writer.writerow([transaction.book_id,transaction.stud_id,transaction.issue_date,transaction.return_date,'0'])
        return response
    else:
        return HttpResponse('<H1>Invalid access</H1>')
            

def requested(request):
    student = User.objects.get(id = request.user.id)
    pending_req = Status.objects.filter(stud_id = student)
    pending_req = pending_req.filter(req = 'pending')
    return render(request, 'Lib/student/requested.html', locals())