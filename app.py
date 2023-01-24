import flask
import requests
import openai
import json
from flask import Flask, request, jsonify,redirect,render_template
import stripe
import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt



app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/mail', methods=['GET', 'POST'])
@login_required
def index():
    if flask.request.method == 'GET':
        form_data = flask.session.get('form_data', {})
        
    elif flask.request.method == 'POST':
        # Save form data to a session variable
        flask.session['form_data'] = flask.request.form
        
        form_data = {}
        if 'form_data' in flask.session:
            # Retrieve form data from the session variable
            form_data = flask.session.pop('form_data')
        else:
            # Set default values for form data
            form_data = {
                'sender': '',
                'recipient': '',
                'subject': '',
                'message': '',
                'language': '🇺🇸',
                'style': 'professional',
                'respond': ''
        }
        openai.api_key = "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"
        length = 200
        max_tokens=200
        try:
            if length:
                max_tokens = int(length)
                if not 0 < max_tokens <= 500:
                    max_tokens = 200
        except ValueError:
            max_tokens = 200

        language = flask.request.form.get("language")
        style = flask.request.form.get("style")
        respond = flask.request.form.get("flexSwitchCheckDefault")



        if language == "🇩🇪":
            if respond == "respond":
                    prompt = (
                        (f"schreibe eine antwort für diese email: {flask.request.form['message']}\n"))
            else:
                prompt = (
                    (f"Type: Email\n"
                    f"Von: {flask.request.form['sender']}\n"
                    f"Zu: {flask.request.form['recipient']}\n"
                    f"Thea=ma: {flask.request.form['subject']}\n"
                    f"Format:Fully written email in English\n"
                    f"\nSchreibe eine Email über: {flask.request.form['message']}\n"))
                    
        elif language == "🇺🇸":
                prompt = (
                    (f"Type: Email\n"
                    f"From: {flask.request.form['sender']}\n"
                    f"To: {flask.request.form['recipient']}\n"
                    f"Subject: {flask.request.form['subject']}\n"
                    f"Format:Fully written email in Deutsch\n"
                    f"\nWrite an email with 175 words about {flask.request.form['message']}\n"))

        elif language == "🇫🇷":
                prompt = (
                    (f"Type : Email\n"
                    f"De : {flask.request.form['sender']}\n"
                    f"À : {flask.request.form['recipient']}\n"
                    f"Sujet : {flask.request.form['subject']}\n"
                    f"Format:Email entièrement rédigé en français\n"
                    f"\nÉcrivez un email de 175 mots sur {flask.request.form['message']}\n"))
                    
        completions = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

        )
        print(prompt)
        print(language)
        print(style)
        generated_message = completions.choices[0].text

       



        

        # Split the generated message into greeting, beginning, body, and sign-off
        try:
            greeting, beginning, body, sign_off = generated_message.split("\n\n", 3)
            
        except ValueError:
            
            greeting = generated_message
            beginning = ""
            body = ""
            sign_off = ""

            
             

        return flask.render_template('index.html', form_data=form_data, greeting=greeting, beginning=beginning, body=body, sign_off=sign_off)
    return flask.render_template('index.html',form_data=form_data)


@app.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html')

@app.route('/success19')
def success19():
    session_id = request.args.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    customer = stripe.Customer.retrieve(session.customer)
    customer_email = customer.email

    print(customer_email)
    #SQL statement here 
    return render_template('success19.html', customer_email=customer_email)

@app.route('/success33')
def success33():
    session_id = request.args.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    customer = stripe.Customer.retrieve(session.customer)
    customer_email = customer.email

    print(customer_email)
    #SQL statement here 
    return render_template('success33.html', customer_email=customer_email)

@app.route('/success299')
def success299():
    session_id = request.args.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    customer = stripe.Customer.retrieve(session.customer)
    customer_email = customer.email

    print(customer_email)
    #SQL statement here 
    return render_template('success299.html', customer_email=customer_email)
redirect('/home')

@app.route('/webhook', methods=['POST'])
def webhook():
    event = json.loads(request.data)
    if event['type'] == 'customer.subscription.deleted':
        # Get the customer ID from the event
        customer_id = event['data']['object']['customer']
        customer = stripe.Customer.retrieve(customer_id)
        customer_email = customer.email
        # Update the user's access in your database
        update_user_access(customer_email, False)
    return '', 200


stripe.api_key = "sk_test_51MQ8TIEsdTh7VZgicQGZEqhkIyjZPgSmlV0cQ3f8sG5jlazr6FxNqOjfTBigCjo9AbDxy7yJuumQzXhn6uWYpZ5000GSpY1BN8"
endpoint_secret = 'whsec_a6cc887c04ddb9a429410362d58a4322f5b0cc9338e14c14158c5c7782f0774f'
YOUR_DOMAIN = 'http://localhost:4242'
#flask run --host=localhost --port=4242 


@app.route('/monthlyprivate', methods=['POST'])
def monthlyprivate():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    #below is the price id  for 19$
                    'price': 'price_1MQE85EsdTh7VZgiDY4NJAsd',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success19?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@app.route('/monthlybussines', methods=['POST'])
def monthlybussines():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    #this is for 34$
                    'price': 'price_1MScKTEsdTh7VZgiVc9AnFV5',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success33?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@app.route('/yearlybuissnes', methods=['POST'])
def yearlybussines():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                     #this is for 299$ yearly subscription
                    'price': 'price_1MScImEsdTh7VZgihxBnnUUi',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success299?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

def update_user_access(customer_email, has_access):
    print('cancelled premium access')
    pass

if __name__ == '__main__':
    app.run(debug=True)

