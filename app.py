import openai
import flask

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        openai.api_key = "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"
        prompt = (
            (f"Type: Email\n"
         f"To: {flask.request.form['recipient']}\n"
         f"Subject: {flask.request.form['subject']}\n"
         f"Style: {flask.request.form['style']}\n"
         f"Format:Fully written Email\n"
         f"\n{flask.request.form['message']}\n"))
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        print(prompt)
        generated_message = completions.choices[0].text

        # Split the generated message into greeting, beginning, body, and sign-off
        greeting, beginning, body, sign_off = generated_message.split("\n\n", 3)
        print(greeting)
        print(beginning)
        print(body)
        print(sign_off)
        print()

        return flask.render_template('index.html', greeting=greeting, beginning=beginning, body=body, sign_off=sign_off, recipient=flask.request.form['recipient'], subject=flask.request.form['subject'], style=flask.request.form['style'], message=flask.request.form['message'])
    return flask.render_template('index.html')




if __name__ == '__main__':
    app.run()
