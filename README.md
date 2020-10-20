# IRIS_191CS148_1_Django
The repo contains the IRIS WEB team recruitment task

# Online Library

### Contents
* [Getting started](#getting-started)
* [Implemented Features](#implemented-features)
* [Planned Features](#planned-features)
* [Known Bugs](#known-bugs)
* [References](#references)

[PEP 8](https://www.python.org/dev/peps/pep-0008/) Python style guide is followed for all codes in python along with [Django conventions](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/).

## Getting started
* Install, create and activate the virtual environment(env_name is the name given to the environment. Installs python3 if not installed)
```
pip install virtualenv
virtualenv env_name
virtualenv -p /usr/bin/python3 virtualenv_name
source env_name/bin/activate
```
* Once the virtual environment is created, install all dependecies required for the project
```
pip install -r requirements.txt
```

* Run the below command to copy the source code locally(Assuming git is installed)
```
git clone https://github.com/Rakshith176/IRIS_191CS148_1_Django.git
```
* Now the complete source code is setup on your local computer and ready to run on a local server.
* Once the process is completed. Navigate to the directory where all apps are present
```
cd IRIS_191CS148_1_Django
cd library
```
* Create a user_id and password for the admin manually
```
python manage.py createsuperuser
```

* The final step to start the local server by running the below command
```
python manage.py runserver
```
* You will be provided a url on the terminal which for example looks like http://127.0.0.1:8000/
Paste the url in the browser to run the project locally(this project's home page will appear after adding /lib at the end of given url)
 
 
## Implemented Features
   ### Admin
   * Dashboard to add , edit, update, delete books
   * Has access to approve or reject the book issue request created by the student(initially the request would be pending when the student creates the request)
   * A dashboard to view the approved, pending, rejected requests in three different tabs
   * Once the approved book is returned(considered a complete transaction) it gets added to the transaction dashboard. Where all transaction history is shown with required parameters
   * The admin also has an option to **download** all the transaction history(book, student, issue date, return date, duration) as a csv file.
   
   ### Student
   * A student can create a issue request to the library for a book which is available and displayed.
   * A list of books that are yet to be approved by the library is made available.
   * He/She is **prohibited from creating multiple requests** to the same book if its approved(and not returned back) or requested and not approved yet. A warning message is displayed if a request is made to the same book.
   * The student cannot create a request if the book quantity is 0.
   * Once the book has been approved it will be displayed in **mybooks** section.
   * The approved books in my books section is displayed with an option to return. Once the student clicks on return the book will no longer appear in mybooks section.
   * The transaction section is made available for the student to view all transactions that were completed till date.
   
   ### General Features
   * All books that are added by the admin is showed in all books section(which has quantity greater than 0)
   * Quantity of book is decreased once the book is approved and increased if the book is returned by the student automatically.
   * Options to add, delete, update, approve books etc.. students are prevented access to this as they are specific to admin only.
   * Flash messages are activated for every action done.
   * Features given to admin are not made available to student(security issues are sorted)
   
   
## Planned Features
 * For now the admin will be given userid and password to login to admin portal(or can be created manually). A registration page can be made giving a secret key opt for teachers to create their admin profile through the website. **This data can be stored in the same table where student info is stored**. Which we will have a single table in the database for student and teachers..
 * Multiple images uploading option.
 * Frontend can be improved better
 
 ## Known Bugs
 * There is slight problem with media folder
 If any bugs or issues is found please do open an issue mentioning the problem
 
 ## References
 * [Django documentation](https://docs.djangoproject.com/en/3.1/)
 * [Bootstrap](https://getbootstrap.com/docs/4.5/getting-started/introduction/) - for frontend works
 * [Stackoverflow](https://stackoverflow.com/)
 
