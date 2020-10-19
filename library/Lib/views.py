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


#function to register students to give them access to library services
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


def all_books(request):
    book_list = Book.objects.order_by('-pk') #query all books and display recently added first
    return render(request, 'Lib/all_books.html', locals())


#details of the as requested
def book_detail(request, pk):
    book = get_object_or_404(Book, id = pk)
    return render(request, 'Lib/book_detail.html', locals())



#The following functions are specific for the admin user only

#function for the librarian(superuser in this case) to add new books to the portal
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


#this function updates info of the books which are already added(accessed only by the admin)
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


#deletes the book that is added(access given to admin only)
@login_required
def book_delete(request, pk):
    if not request.user.is_superuser:
        messages.warning(request,f'You dont have access')
        return redirect('lib-home')
    obj = get_object_or_404(Book, pk = pk)
    obj.delete()
    messages.warning(request, f'Book has been deleted')
    return redirect('all_books')


#this function queries and stores the request history and sorts accordingly
@login_required
def requests(request):
    if not request.user.is_superuser:
        messages.warning(request,f'You dont have access')
        return redirect('lib-home')
    pending = Status.objects.filter(req='pending')
    approved = Status.objects.filter(req='approved')
    rejected = Status.objects.filter(req='rejected')
    return render(request,'Lib/admin/requests.html',locals())


#approves the book which are requested by the user(done only by the admin)
@login_required
def approve(request,pk):
    if not request.user.is_superuser:
        messages.warning(request,f'You dont have access')
        return redirect('lib-home')
    approval = Status.objects.get(id=pk)
    approval.req = 'approved'
    book_pk = approval.book_id.id
    book = Book.objects.get(id=book_pk)
    book.quantity = book.quantity - 1
    approval.issue_date = datetime.datetime.now()
    book.save()
    approval.save()
    messages.success(request, f'Book approved')
    return redirect('requests')


#rejects the issue request created by the user
@login_required
def reject(request,pk):
    if not request.user.is_superuser:
        messages.warning(request,f'You dont have access')
        return redirect('lib-home')
    reject = Status.objects.get(id = pk)
    reject.req ='rejected'
    reject.save()
    messages.warning(request, f'Request Rejected')
    return redirect('requests')


#this function will download a csv file with required info of transactions to the admin
@login_required
def csv_file(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type = 'text/csv')
        response['Content-Disposition'] = 'attachment; filename = Transactions_as-on-' + str(datetime.datetime.now().date()) + '.csv'
        
        writer = csv.writer(response)
        #these will be the colums in the csv file
        writer.writerow(['Book','Student','Issue date','Return date','Duration(days)'])

        transactions = Status.objects.exclude(return_date = None)

        for transaction in transactions:
            #calculate duration the book has been used by student and returns the fields accordingly
            transaction.issue_date = transaction.issue_date.date()
            transaction.return_date = transaction.return_date.date()
            duration = ( transaction.return_date - transaction.issue_date ).days
            writer.writerow([
                            transaction.book_id,
                            transaction.stud_id,
                            transaction.issue_date,
                            transaction.return_date,
                            duration])
        return response
    else:
        return HttpResponse('<H1>Invalid access</H1>')


#the above functions are for admin only


#The following functions are for the students


#creates a issue request for a particular book(which will then be approved or rejected by the admin)
@login_required
def issue_request(request,pk):
    obj = Book.objects.get(id = pk)
    #check if number of books greater than 0
    if obj.quantity:
        stud = User.objects.get(id = request.user.id)
        check_req = Status.objects.filter(book_id = obj)
        check_req = check_req.filter(stud_id = stud)
        pending_req = check_req.filter(req = 'pending').exists()#checks if request has already made for that particular book
        approved_req = check_req.filter(req = 'approved').exists()#checks if book is already approved to the student

        if pending_req:
            messages.warning(request, f'Request already sent') 
        elif approved_req:
            messages.warning(request, f'Book already approved')
        #the above two conditions makes sure that no request is made on the same book if already made.
        else:
            create_req = Status()
            create_req.stud_id = stud
            create_req.book_id = obj
            create_req.req = 'pending'
            create_req.save()
            messages.success(request, f'Request sent')
    else:
        messages.warning(request, f'Book not available for now')
    return redirect('all_books')


#displays all the books which are approved and not returned back
@login_required
def mybooks(request):
    books_approved = Status.objects.filter(req='approved')
    books_approved = books_approved.filter(stud_id=request.user.id)
    return render(request,"Lib/student/mybooks.html",locals())


#returns the book back to library which were approved
@login_required
def return_book(request,pk):
    return_book = Status.objects.get(id = pk)
    if return_book.req == 'approved':
            return_book.req = 'none'
            book_pk = return_book.book_id.id
            book = Book.objects.get(id = book_pk)
            book.quantity = book.quantity + 1
            return_book.return_date = datetime.datetime.now()
            return_book.save()
            book.save()
            messages.success(request, f'Book returned successfully ')
            return redirect('mybooks')
    else:
            return HttpResponse('<H1>Invalid access</H1>')



#returns the books which are requested by the user and not approved yet        
@login_required
def requested(request):
    student = User.objects.get(id = request.user.id)
    pending_req = Status.objects.filter(stud_id = student)
    pending_req = pending_req.filter(req = 'pending')
    return render(request, 'Lib/student/requested.html', locals())


#returns the transactions that have been made till date
@login_required
def transactions(request):
    if request.user.is_superuser:
        completed_transaction = Status.objects.exclude(return_date = None)#returns all transactions to the admin that are completed
    else:
        student = User.objects.get(id = request.user.id)
        completed_transaction = Status.objects.filter(stud_id = student)
        completed_transaction = completed_transaction.exclude(return_date = None)#returns transactions made by the user with the library  
    return render(request,"Lib/transactions.html",locals())