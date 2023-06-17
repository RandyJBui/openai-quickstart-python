import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        # animal = request.form["animal"]
        todo = request.form["name","duration","priority"]
        print(todo)
        #busy = get from google calendar

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(todo),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


'''
todo qualities: [(name, duration, priority), (name, duration, priority), (name, duration, priority)]

-name
-duration
-priority
maybe
-fatigue
-location
'''

def generate_prompt(todo):
    return """repeat what i typed""".format(
        todo.capitalize()
    )




# def generate_prompt(todo):
#     return """Create a schedule for me that puts 'todo tasks' at times when I am not also busy with 'busy tasks' ".

# todo: 
# schedule: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# todo: Dog
# schedule: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# todo: {}
# schedule:""".format(
#         todo.capitalize()
#     )

# def generate_prompt(animal):
#     return """Suggest three names for an animal that is a superhero.

# Animal: Cat
# Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# Animal: Dog
# Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# Animal: {}
# Names:""".format(animal.capitalize())

