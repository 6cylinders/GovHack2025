from flask import Flask, render_template, request
import io
import base64
import matplotlib.pyplot as plt

from govhack_ml import interpret_query  

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    user_query = None
    response = None
    table_img = None  # for passing matplotlib image

    if request.method == "POST":
        user_query = request.form.get("query")

        matched_func, score = interpret_query(user_query)

        # For now, just echo which function was matched
        response = f"Query: {user_query}<br>Matched function: {matched_func} (score={score:.3f})"

    return render_template("index.html", query=user_query, response=response, table_img=table_img)

if __name__ == "__main__":
    app.run(debug=True)
