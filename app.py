from flask import Flask, request, render_template, redirect, url_for, jsonify
import pandas as pd

app = Flask(__name__)

# Cargar datos desde el archivo Excel de usuarios
try:
    df_usuarios = pd.read_excel("usuarios.xlsx")  # Asegúrate de que el archivo esté en la misma carpeta
except Exception as e:
    print("Error al cargar el archivo Excel de usuarios:", e)
    df_usuarios = pd.DataFrame(columns=["Usuario", "Contraseña"])  # Estructura vacía en caso de error

# Cargar datos desde el archivo Excel de alumnos
try:
    df_alumnos = pd.read_excel("alumnos.xlsx")  # Archivo con las matrículas y datos de alumnos
except Exception as e:
    print("Error al cargar el archivo Excel de alumnos:", e)
    df_alumnos = pd.DataFrame(columns=["Matrícula", "Nombre", "Grupo", "Promedio", "Estatus"])  # Estructura vacía en caso de error

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
    user_match = df_usuarios[(df_usuarios["Usuario"].str.strip() == username) & (df_usuarios["Contraseña"].astype(str).str.strip() == password)]

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
        user_match = df_usuarios[(df_usuarios["Usuario"].str.strip() == username) & (df_usuarios["Contraseña"].astype(str).str.strip() == password)]
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

# Nueva ruta para buscar matrículas
@app.route("/buscar_matricula", methods=["POST"])
def buscar_matricula():
    data = request.get_json()
    matricula = data.get("matricula")

    try:
        # Leer el archivo Excel de alumnos en cada búsqueda para obtener datos actualizados
        df_alumnos = pd.read_excel("alumnos.xlsx")
        
        # Convertir la columna "Matrícula" a tipo string para evitar problemas de tipo de dato
        df_alumnos["Matrícula"] = df_alumnos["Matrícula"].astype(str).str.strip()
        matricula = str(matricula).strip()

        # Buscar la matrícula en el archivo de alumnos
        resultado = df_alumnos[df_alumnos["Matrícula"] == matricula]

        if resultado.empty:
            return jsonify({"error": "Matrícula no encontrada"}), 404

        # Convertir el resultado a un diccionario
        resultado_dict = resultado.iloc[0].to_dict()

        return jsonify(resultado_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)