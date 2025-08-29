from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    user_query = None
    response = None

    if request.method == "POST":
        user_query = request.form.get("query")
        response = f"You asked: {user_query}. The chatbot will now do its thing"

    return render_template("index.html", query=user_query, response=response)

if __name__ == "__main__":
    app.run(debug=True)