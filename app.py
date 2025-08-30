from flask import Flask, render_template, request
import io
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    user_query = None
    response = None
    table_img = None  # for passing matplotlib image

    if request.method == "POST":
        user_query = request.form.get("query")

         # Example logic: if user types "table", generate a matplotlib table
        # if user_query.lower() == "table":
        #     fig, ax = plt.subplots()
        #     # Example data for table
        #     data = [["Alice", 24], ["Bob", 30], ["Charlie", 28]]
        #     col_labels = ["Name", "Age"]
        #     # Hide axes
        #     ax.axis("tight")
        #     ax.axis("off")
        #     # Create table
        #     table = ax.table(cellText=data, colLabels=col_labels, loc="center")
        #     # Save to BytesIO
        #     buf = io.BytesIO()
        #     plt.savefig(buf, format="png")
        #     buf.seek(0)
        #     # Encode as base64 so it can be embedded in HTML
        #     table_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        #     plt.close(fig)
        #     response = "Here’s the table you asked for:"
        # else:
        response = f"You asked: {user_query}."

    return render_template("index.html", query=user_query, response=response, table_img=table_img)

if __name__ == "__main__":
    app.run(debug=True)
