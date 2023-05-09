import os
import json
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        print("FILESSS")
        print(request.files)
        # files
        education = request.files["Education"].read()
        positions = request.files["Positions"].read()
        skills = request.files["Skills"].read()
        # education, position, skills = ('', '', '')
        # vacancy
        vacancy = request.form["Vacancy"]
        message = f"I am applying to the following job vacancy: {vacancy}\n\n My education is: {education}\n\n My previous work experience is: {positions}\n\n My skills include: {skills}\n\n Can you write a motivation letter for this vacancy based on my profile?"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional job application writer.",
                },
                {"role": "user", "content": message},
            ],
        )
        # save response to json
        json_response = response.to_dict()

        with open("response.json", "w") as f:
            json.dump(json_response, f, indent=4)
        return redirect(
            url_for("index", result=response["choices"][0]["message"]["content"])
        )

    result = request.args.get("result")
    # save result to text file
    if result:
        with open("results.txt", "a") as f:
            f.write(result + "\n")

    return render_template("index.html", result=result)
