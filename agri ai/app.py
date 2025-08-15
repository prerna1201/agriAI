from flask import Flask, render_template, request, redirect, url_for
import openai

app = Flask(__name__)

# 🔹 Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# -------------------
# Home page – registration form
# -------------------
@app.route("/")
def index():
    return render_template("index.html")

# -------------------
# Registration route – accepts both GET & POST safely
# -------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "")
        phone = request.form.get("phone", "")

        # Simulate saving or sending SMS
        print(f"SMS Sent to {phone}: Registration successful!")

        return redirect(url_for("success", name=name))
    # Direct GET access goes back to home
    return redirect(url_for("index"))

# -------------------
# Success page
# -------------------
@app.route("/success")
def success():
    name = request.args.get("name", "")
    return render_template("success.html", name=name)

# -------------------
# Chat page
# -------------------
@app.route("/chat", methods=["GET", "POST"])
def chat():
    bot_reply = None
    user_message = None

    if request.method == "POST":
        user_message = request.form.get("message", "")
        if user_message:
            try:
                # OpenAI API call
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant for farming queries."},
                        {"role": "user", "content": user_message}
                    ]
                )
                bot_reply = response["choices"][0]["message"]["content"].strip()
            except Exception as e:
                bot_reply = f"Error: {str(e)}"

    return render_template("chat.html", bot_reply=bot_reply, user_message=user_message)

# -------------------
# Run app
# -------------------
if __name__ == "__main__":
    app.run(debug=True)
