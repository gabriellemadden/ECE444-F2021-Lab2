from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, ValidationError

from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

# Example 4.1 requirement
# Not creating some crazy string because it's
# exposed in this github repo anyways
app.config['SECRET_KEY'] = 'key'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UofTForm()

    if form.validate_on_submit():
        old_name = session.get('name')
        print(old_name)
        print(form.name.data)

        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')

        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))

    return render_template(
        'index.html',
        current_time=datetime.utcnow(),
        form=form,
        name=session.get('name'),
        email=session.get('email')
    )

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

class EmailValidator(object):
    """
    Checks for the presence of an '@' symbol.
    """

    def __call__(self, form, field):
        if '@' not in field.data:
            message = 'Please include an \'@\' in the email address. \'' + field.data + '\' is missing an \'@\'.'
            raise ValidationError(message)

class UofTForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your UofT Email address?', validators=[EmailValidator()])
    submit = SubmitField('Submit')


if __name__ == '__main__':
    app.run(debug=True)
