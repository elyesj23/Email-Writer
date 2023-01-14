import flask
import requests
import openai

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
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



        prompt = (
            (f"Type: Email\n"
            f"Von: {flask.request.form['sender']}\n"
            f"An: {flask.request.form['recipient']}\n"
            f"Thema: {flask.request.form['subject']}\n"
            f"Format:Vollständig geschriebene Email in Deutsch\n"
            f"\nSchreibe eine Email mit 175 Wörtern über  {flask.request.form['message']}\n"))

        
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.6,
        )
        print(prompt)
        generated_message = completions.choices[0].text

       



        

        # Split the generated message into greeting, beginning, body, and sign-off
        try:
            greeting, beginning, body, sign_off = generated_message.split("\n\n", 3)
            
        except ValueError:
            
            greeting = generated_message
            beginning = ""
            body = ""
            sign_off = ""

            
             

        return flask.render_template('index.html', greeting=greeting, beginning=beginning, body=body, sign_off=sign_off, recipient=flask.request.form['recipient'], subject=flask.request.form['subject'], message=flask.request.form['message'])
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run()

