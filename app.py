import flask
import openai

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        openai.api_key = "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"
        length=flask.request.form['length']
        max_tokens=125
        try:
            if length:
                max_tokens = int(length)
                if not 0 < max_tokens <= 500:
                    max_tokens = 125
        except ValueError:
            max_tokens = 125
        language = flask.request.form['language']
        if language == "German":
            engine = "text-davinci-002-german"
        else:
            engine = "text-davinci-002"
        prompt = (
            (f"Type: Email\n"
            f"From: {flask.request.form['sender']}\n"
            f"To: {flask.request.form['recipient']}\n"
            f"Subject: {flask.request.form['subject']}\n"
            f"Style: {flask.request.form['style']}\n"
            f"Language: {language}\n"
            f"Length: {max_tokens}\n"
            f"Format:Fully written Email\n"
            f"\n{flask.request.form['message']}\n"))

        completions = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.5,
        )
        print(prompt)
        generated_message = completions.choices[0].text
        # Split the generated message into greeting, beginning, body, and sign-off
        try:
            greeting, beginning, body, sign_off = generated_message.split("\n\n", 3)
            print(generated_message)
        except ValueError:
            print(generated_message)
            greeting = generated_message
            beginning = ""
            body = ""
            sign_off = ""


            
             

        return flask.render_template('index.html', greeting=greeting, beginning=beginning, body=body, sign_off=sign_off, recipient=flask.request.form['recipient'], subject=flask.request.form['subject'], style=flask.request.form['style'], message=flask.request.form['message'])
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run()
