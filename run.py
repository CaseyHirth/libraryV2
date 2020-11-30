
from flask import render_template, redirect, request, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, BookSearchForm, BookAddForm, branch_dictionary
from app import app, db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import Member, Book, User, Employees, CheckOut, CheckIn, Region, Branch


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/books',methods=['GET','POST'])
def books():
    

    form=BookSearchForm()
    
    if form.validate_on_submit():
        books = db.session.query(Book, Branch.branchName).join(Branch, Book.branchLocation == Branch.id).filter(Book.branchLocation == form.branchLocation.data).all()
        
    else:
        books = db.session.query(Book,Branch.branchName).join(Branch, Book.branchLocation == Branch.id).all()

    print(books)

    
    available=[]
    if current_user.is_authenticated:
        if current_user.role=='member' or current_user.role=='employee':
            member = Member.query.filter_by(email=current_user.email).first()

            for book in books:
                checkouts = CheckOut.query.filter_by(book_id = book[0].id)
                checkins = CheckIn.query.filter_by(book_id = book[0].id)
                if  checkouts == None or checkouts.count() == checkins.count():
                    available.append(True)
                else:
                    available.append(False)     
    
    
    return render_template('books.html', books=books, available=available, form=form, branch_dictionary=branch_dictionary)

@app.route('/books/search')
def bookSearch():
    title = request.args.get('keyword')  
    books = db.session.query(Book,Branch.branchName).join(Branch, Book.branchLocation == Branch.id).filter(Book.title == title).all()
    if current_user.is_authenticated:
        if current_user.role == 'member' or current_user.role=='employee':
            available=[]
            member = Member.query.filter_by(email=current_user.email).first()
            
            for book in books:
                
                checkouts = CheckOut.query.filter_by(book_id = book[0].id)
                checkins = CheckIn.query.filter_by(book_id = book[0].id)
                if  checkouts == None or checkouts.count() == checkins.count():
                    available.append(True)
                else:
                    available.append(False) 
            return render_template('book_search_results.html', books=books, available=available, branch_dictionary=branch_dictionary)   
    return render_template('book_search_results.html', books=books, branch_dictionary=branch_dictionary)

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
        return redirect(url_for('access_denied'))

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
        return redirect(url_for('access_denied'))

        

@app.route('/delete_book', methods=['GET','POST'])
@login_required
def deleteAbook():
    if current_user.role=='employee':
        book_id = request.args.get('book_id')
        book = Book.query.filter_by(id=book_id).first()
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('access_denied'))



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
        return redirect(url_for('access_denied'))
    

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'member':
        return redirect(url_for('access_denied'))
    if current_user.role == 'employee':
        employee = Employees.query.filter_by(email=current_user.email).first()

        books_by_branch = db.session.query(Branch.branchName, db.func.count(Book.id)).join(Book, Book.branchLocation == Branch.id).group_by(Branch.id).all()
        total_books = 0
        for branch in books_by_branch:
            total_books+=branch[1]
        
        total_members= db.session.query(db.func.count(Member.id)).first()

        members = db.session.query(Member, db.func.count(CheckOut.id)).join(CheckOut, Member.id==CheckOut.member_id).group_by(Member.id).order_by(db.func.count(CheckOut.id).desc()).all()
        

        return render_template('dashboard.html', name=employee.firstName, members=members, books_by_branch = books_by_branch, 
                                total_books=total_books, total_members=total_members[0])

@app.route('/dashboard/report', methods=['GET'])
@login_required
def report():
    if current_user.role == 'employee':

        genre_popularity = db.session.query(Book.genre, db.func.count(CheckOut.id)).join(CheckOut, Book.id==CheckOut.book_id).\
                            group_by(Book.genre).order_by(db.func.count(CheckOut.id).desc()).all()

        genre_pop_young = db.session.query(Book.genre, db.func.count(CheckOut.id)).join(CheckOut, Book.id==CheckOut.book_id).\
                            join(Member, Member.id == CheckOut.member_id).filter(Member.age < 18).group_by(Book.genre).\
                            order_by(db.func.count(CheckOut.id).desc()).all()

        genre_pop_mid = db.session.query(Book.genre, db.func.count(CheckOut.id)).join(CheckOut, Book.id==CheckOut.book_id).\
                            join(Member, Member.id == CheckOut.member_id).filter(Member.age >= 18).filter(Member.age <= 40).\
                            group_by(Book.genre).order_by(db.func.count(CheckOut.id).desc()).all()

        genre_pop_older = db.session.query(Book.genre, db.func.count(CheckOut.id)).join(CheckOut, Book.id==CheckOut.book_id).\
                            join(Member, Member.id == CheckOut.member_id).filter(Member.age > 40).\
                            group_by(Book.genre).order_by(db.func.count(CheckOut.id).desc()).all()
        
        region_by_checkouts = db.session.query(Region.id, Region.regionName, db.func.count(CheckOut.id)).\
                            join(Branch, Region.id == Branch.region_id).join(Book, Book.branchLocation == Branch.id).\
                                join(CheckOut, CheckOut.book_id == Book.id).group_by(Region.id).\
                                    order_by(db.func.count(CheckOut.id).desc()).all()

        return render_template('report.html', genre_popularity=genre_popularity, genre_pop_young=genre_pop_young, genre_pop_mid=genre_pop_mid, 
                                genre_pop_older=genre_pop_older, region_by_checkouts=region_by_checkouts)

    return redirect(url_for('access_denied'))


@app.route('/dashboard/add_book', methods=['GET','POST'])
@login_required
def addBook():
    form = BookAddForm()

    if form.validate_on_submit():
        print(form.branchLocation.data)
        newBook = Book(isbn=form.isbn.data, title=form.title.data, author=form.author.data, genre=form.genre.data, branchLocation=form.branchLocation.data)
        db.session.add(newBook)
        db.session.commit()
        return render_template('add_book.html', form=form, bookAdded=True)
        



    return render_template('add_book.html', form=form, bookAdded=False)

@app.route('/access_denied')
def access_denied():
    return render_template('access_denied.html')        

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


with app.app_context():
    db.init_app(app) # init db in app
    db.create_all() # create all the table that haven't been created

if __name__ == '__main__':
    app.run(debug=True)