import flask
import requests
import openai
import json
from flask import Flask, request, jsonify,redirect,render_template
import stripe
import os


app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mail', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
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


        if language == "🇩🇪":
                prompt = (
                    (f"Type: Email\n"
                    f"Von: {flask.request.form['sender']}\n"
                    f"An: {flask.request.form['recipient']}\n"
                    f"Thema: {flask.request.form['subject']}\n"
                    f"Format:Vollständig geschriebene Email in Deutsch\n"
                    f"\nSchreibe eine Email mit 175 Wörtern über  {flask.request.form['message']}\n"))
                    
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
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.6,
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

            
             

        return flask.render_template('index.html', sender=flask.request.form['sender'], greeting=greeting,language=language, beginning=beginning, body=body, sign_off=sign_off, recipient=flask.request.form['recipient'], subject=flask.request.form['subject'], message=flask.request.form['message'])
    return flask.render_template('index.html')


@app.route('/checkout')
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

