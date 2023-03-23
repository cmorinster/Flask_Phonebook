from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import AddNumber
from app.models import PhoneBook

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/phonebook', methods=["GET", "POST"])
def signup():
    form = AddNumber()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        print(first_name, last_name, phone_number, address)
        new_user = PhoneBook(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)
        flash(f"{new_user.first_name} has been added!", "success")
        return redirect(url_for('index'))
    return render_template('phonebook.html', form=form)


