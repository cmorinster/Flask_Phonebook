from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import AddNumber, LoginForm, SignUpForm
from app.models import PhoneBook, User
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/', methods=["GET", "POST"])
def index():
    pbook = PhoneBook.query.all()
    #form = PhoneBook()
    pbook = db.session.execute(db.select(PhoneBook).where((PhoneBook.user_id.ilike(f"%{current_user.id}"))))
    return render_template('index.html', pbook=pbook)


@app.route('/phonebook', methods=["GET", "POST"])
def addnumber():
    form = AddNumber()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        user_id = current_user.id
        print(first_name, last_name, phone_number, address)
        new_user = PhoneBook(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, user_id = current_user.id)
        flash(f"{new_user.first_name} has been added!", "success")
        return redirect(url_for('index'))
    return render_template('phonebook.html', form=form)



@app.route('/edit/<phone_id>', methods=["GET", "POST"])
@login_required
def edit_phone(phone_id):
    form = AddNumber()
    phone_to_edit = PhoneBook.query.get_or_404(phone_id)
    if phone_to_edit.user != current_user:
        flash("You do not have permission to edit this phone entry", "danger")
        return redirect(url_for('index'))

   
    if form.validate_on_submit():
        phone_to_edit.first_name = form.first_name.data
        phone_to_edit.last_name = form.last_name.data
        phone_to_edit.phone_number = form.phone_number.data
        phone_to_edit.address = form.address.data
        db.session.commit()
        flash(f"{phone_to_edit.first_name} {phone_to_edit.last_name} has been edited!", "success")
        return redirect(url_for('index'))

    
    form.title.data = phone_to_edit.title
    form.body.data = phone_to_edit.body
    form.image_url.data = phone_to_edit.image_url
    return render_template('edit.html', form=form, pbook=phone_to_edit)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Hooray our form was validated!!')
        username = form.username.data
        password = form.password.data
        print(username, password)
        check_user = db.session.execute(db.select(User).filter((User.username == username)))
        if check_user==True:
            flash("A user with that username and/or email already exists", "warning")
            return redirect(url_for('signup'))
        new_user = User(username=username, password=password)
        flash(f"Thank you {new_user.username} for signing up!", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)



@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated :)')
        username = form.username.data
        password = form.password.data
        print(username, password)
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f'You have successfully logged in as {username}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect(url_for('index'))


@app.route('/delete/<phone_id>')
@login_required
def delete_phone(phone_id):
    phone_to_delete = PhoneBook.query.get_or_404(phone_id)
    if phone_to_delete.user != current_user:
        flash("You do not have permission to delete this contact", "danger")
        return redirect(url_for('index'))

    db.session.delete(phone_to_delete)
    db.session.commit()
    flash(f"{phone_to_delete.first_name} {phone_to_delete.last_name} has been deleted", "info")
    return redirect(url_for('index'))