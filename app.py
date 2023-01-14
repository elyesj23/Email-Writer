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
            f"Zu: {flask.request.form['recipient']}\n"
            f"Thema: {flask.request.form['subject']}\n"
            f"Format:Fully written Email\n"
            f"\nSchreibe eine Email mit 200 Wörtern über  {flask.request.form['message']} in einem {flask.request.form['style']} ton\n"))

        
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

        url = "https://api-free.deepl.com/v2/translate"
        headers = {
            "Authorization": "DeepL-Auth-Key b062df55-dee6-d717-9fb8-fa02cb214fb8:fx",
            "User-Agent": "YourApp/1.2.3",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "text": generated_message,
            "target_lang": "de"
        }

        response = requests.post(url, headers=headers, data=data)

        print(response.status_code)
        print(response.json())
        response_json = response.json()
        translated_text = response_json['translations'][0]['text']



        

        # Split the generated message into greeting, beginning, body, and sign-off
        try:
            greeting, beginning, body, sign_off = translated_text.split("\n\n", 3)
            
        except ValueError:
            print(translated_text)
            greeting = translated_text
            beginning = ""
            body = ""
            sign_off = ""

            
             

        return flask.render_template('index.html', greeting=greeting, beginning=beginning, body=body, sign_off=sign_off, recipient=flask.request.form['recipient'], subject=flask.request.form['subject'], style=flask.request.form['style'], message=flask.request.form['message'])
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run()

