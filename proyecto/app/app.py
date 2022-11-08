from flask import Flask, render_template, redirect, request, session, url_for

app = Flask(__name__)

#webpages

@app.route("/prueba_producion")
def test():
    return "Prueba de despliegue en produccion"

@app.route("/contact")
def contact():
    return render_template('contact.html', title="Como contactarme");

@app.route("/login")
@app.route("/", methods=["GET"])
def login():
    return render_template('login.html', title="login")

@app.route("/register")
def register():
    return render_template('register.html', title="register")

@app.route("/home")
def home():
    return render_template('home.html', title="home")

@app.route("/editprofile")
def editprofile():
    return render_template('editar/editarUsuario.html', title="editarUsuario")


@app.route("/friends")
def friends():
    return render_template('friends.html', title="friends")

#functions for login, singup, etc...
@app.route("/process_login", methods=["POST"])
def process_login():
    #if request.method == "POST":
        
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(port=8888, debug=True)