
from flask import render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, BookSearchForm, BookAddForm
from app import app, db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import Member, Book, User, Employees, CheckOut, CheckIn


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/books')
def books():
    
    books = Book.query.all()

    available=[]
    if current_user.is_authenticated:
        if current_user.role=='member':
            member = Member.query.filter_by(email=current_user.email).first()

            for book in books:
                checkouts = CheckOut.query.filter_by(book_id = book.id)
                checkins = CheckIn.query.filter_by(book_id = book.id)
                if  checkouts == None or checkouts.count() == checkins.count():
                    available.append(True)
                else:
                    available.append(False)     
    
    print(available)
    return render_template('books.html', books=books, available=available)

@app.route('/books/search')
def bookSearch():
    title = request.args.get('keyword')  
    books = Book.query.filter_by(title=title)
    if current_user.is_authenticated:
        if current_user.role == 'member':
            available=[]
            member = Member.query.filter_by(email=current_user.email).first()
            
            for book in books:
                checkouts = CheckOut.query.filter_by(book_id = book.id)
                checkins = CheckIn.query.filter_by(book_id = book.id)
                if  checkouts == None or checkouts.count() == checkins.count():
                    available.append(True)
                else:
                    available.append(False)
            return render_template('books.html', books=books, available=available)
    else:     
        return render_template('book_search_results.html', books=books)

@app.route('/checkout', methods=['GET'])
@login_required
def checkout():
    if current_user.role=='member':
        book_id = request.args.get('book_id')
        member = Member.query.filter_by(email=current_user.email).first()

        newCheckOut = CheckOut(book_id = book_id, member_id=member.id)
        db.session.add(newCheckOut)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return '<h1> Must be a member </h1>'

@app.route('/checkin', methods=['GET'])
@login_required
def checkin():
    if current_user.role=='member':
        book_id = request.args.get('book_id')
        member = Member.query.filter_by(email=current_user.email).first()

        newCheckIn = CheckIn(book_id = book_id, member_id=member.id)
        db.session.add(newCheckIn)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return '<h1> Must be a member </h1>'

        


# @app.route('/book_search', methods=['GET', 'POST'])
# def search():
#     form = BookSearchForm()

#     if form.validate_on_submit():
#         isbn = form.isbn.data
#         title = form.title.data 
#         author = form.author.data
#         genre = form.genre.data
#         branchLocation = form.branchLocation.data 
#         return redirect(url_for('bookSearchResults', isbn=isbn, title=title, author=author, genre=genre, branchLocation=branchLocation))

#     return render_template('book_search.html', form = form)

@app.route('/add_book', methods=['GET','POST'])
def addBook():
    form = BookAddForm()

    if form.validate_on_submit():
        newBook = Book(isbn=form.isbn.data, title=form.title.data, author=form.author.data, genre=form.genre.data, branchLocation=form.branchLocation.data)
        db.session.add(newBook)
        db.session.commit()


    return render_template('add_book.html', form=form)

@app.route('/delete_book', methods=['GET','POST'])
def deleteAbook():
    form = BookAddForm()

    if form.validate_on_submit():
        newBook = Book(isbn=form.isbn.data, title=form.title.data, author=form.author.data, genre=form.genre.data, branchLocation=form.branchLocation.data)
        db.session.add(deleteBook)
        db.session.commit()


    return render_template('delete_abook.html', form=form)


@app.route('/checkoutbook', methods=['GET','POST'])
def checkoutbook():
    form = BookAddForm()

    if form.validate_on_submit():
        newBook = Book(isbn=form.isbn.data, title=form.title.data, author=form.author.data, genre=form.genre.data, branchLocation=form.branchLocation.data)
        db.session.add(checkoutBook)
        db.session.commit()


    return render_template('checkoutBook.html', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                if user.role == 'member':
                    return redirect(url_for('profile'))
                else:
                    return redirect(url_for('dashboard'))
            
        return '<h1>Invalid email or password </h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashedPassword = generate_password_hash(form.password.data, method='sha256')
        newUser = User(email=form.email.data, 
                        password = hashedPassword, 
                        role = 'member')
        newMember = Member(email=form.email.data, 
                    firstName=form.firstName.data, 
                    lastName=form.lastName.data, 
                    gender=form.gender.data, 
                    age=form.age.data,
                    street=form.street.data, 
                    city=form.city.data, 
                    state=form.state.data, 
                    zip=form.zip.data)
        db.session.add(newMember)
        db.session.add(newUser)
        db.session.commit()

        return redirect(url_for('index'))
        #return '<h1>' + form.username.data + ' ' + form.password.data + ' ' + form.email.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/profile')
@login_required
def profile():
    if current_user.role == 'member':
        member = Member.query.filter_by(email=current_user.email).first()
        checkOuts = CheckOut.query.filter_by(member_id=member.id)
        books = []
        duedates=[]
        for checkOut in checkOuts:
            checkIn = CheckIn.query.filter_by(member_id=member.id,book_id=checkOut.book_id)
            outs = CheckOut.query.filter_by(member_id=member.id, book_id=checkOut.book_id).order_by(CheckOut.id.desc())
            if checkIn == None or outs.count() != checkIn.count():
                book = Book.query.get(checkOut.book_id)
                if book not in books:
                    books.append(book)
                    duedates.append(outs.first().dueDate)


        print(duedates)
        return render_template('profile.html', member=member, books = books, duedates=duedates)

    else:
        return '<h1>Must be a member </h1>'
    

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'member':
        return '<h1>Must be an employee </h1>'
    if current_user.role == 'employee':
        employee = Employees.query.filter_by(email=current_user.email).first()

        return render_template('dashboard.html', name=employee.firstName)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)