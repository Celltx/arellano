from flask import Flask, request, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Cargar datos desde el archivo Excel
try:
    df = pd.read_excel("usuarios.xlsx")  # Asegúrate de que el archivo esté en la misma carpeta
except Exception as e:
    print("Error al cargar el archivo Excel:", e)
    df = pd.DataFrame(columns=["Usuario", "Contraseña"])  # Estructura vacía en caso de error

@app.route("/")
def index():
    return render_template("index.html")  # Página de inicio de sesión para usuarios

@app.route("/admin")
def admin():
    return render_template("admin.html")  # Página de inicio de sesión para administrador

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    # Evitar que el administrador inicie sesión desde el formulario de usuario
    if username == "Yomero":
        return render_template("index.html", error="El administrador debe iniciar sesión desde la página de administrador.")

    # Validar usuario y contraseña en el archivo Excel
    user_match = df[(df["Usuario"].str.strip() == username) & (df["Contraseña"].astype(str).str.strip() == password)]

    if not user_match.empty:
        return redirect(url_for("inicio"))  # Inicio de sesión exitoso para usuarios
    else:
        return render_template("index.html", error="Usuario o contraseña incorrectos")

@app.route("/loginadmin", methods=["POST"])
def loginadmin():
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    # Verificar credenciales del administrador
    if username == "Yomero" and password == "9876":
        return redirect(url_for("inicio_admi"))
    else:
        # Verificar si el usuario existe en la base de datos pero no es el administrador
        user_match = df[(df["Usuario"].str.strip() == username) & (df["Contraseña"].astype(str).str.strip() == password)]
        if not user_match.empty:
            return render_template("admin.html", error="Esta página es solo para el administrador.")
        else:
            return render_template("admin.html", error="Usuario o contraseña incorrectos para administrador")

@app.route("/inicio")
def inicio():
    return render_template("inicio.html")  # Página después de iniciar sesión correctamente para usuarios

@app.route("/inicioadmi")
def inicio_admi():
    return render_template("inicioadmi.html")  # Página después de iniciar sesión correctamente para el administrador

if __name__ == "__main__":
    app.run(debug=True)