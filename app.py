from flask import Flask, render_template, request

from govhack_ml import interpret_query  
import data_queries 

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    user_query = None
    response = None
    table_img = None  # for passing matplotlib image

    if request.method == "POST":
        user_query = request.form.get("query")

          # Run through ML interpreter
        matched_func, score = interpret_query(user_query)
        #create a match case for all functions here

        if matched_func and score >= 0.500:
            try:
                # Dynamically call function by name
                func = getattr(data_queries, matched_func)

                result = func()

                # If function already returns HTML (like get_overall_leave_trends), handle directly
                if isinstance(result, str) and result.startswith("<img"):
                    response = f"Matched function: {matched_func} (score={score:.3f})"
                    table_img = result.split('src="')[1].split('"')[0]  # extract base64
                elif isinstance(result, tuple) or isinstance(result, list):
                    response = f"Matched function: {matched_func} (score={score:.3f})<br>{result}"
                else:
                    response = f"Matched function: {matched_func} (score={score:.3f})<br><pre>{result}</pre>"

            except Exception as e:
                response = f"Error running function '{matched_func}': {e}"

        else:
            response = f"Sorry, I couldn’t confidently match your query (best score={score:.3f})."

    return render_template("index.html", query=user_query, response=response, table_img=table_img)

if __name__ == "__main__":
    app.run(debug=True)
