from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/incidencia", methods=["POST"])
def crear_incidencia():
    nombre = request.form["nombre"]
    email = request.form["email"]
    tipo = request.form["tipo"]
    prioridad = request.form["prioridad"]
    descripcion = request.form["descripcion"]

    print("Nombre: " + nombre)
    print("Email: " + email)
    print("Tipo: " + tipo)
    print("Prioridad: " + prioridad)
    print("Descripción: " + descripcion)

    return "Incidencia recibida"

if __name__ == "__main__":
    app.run(debug=True)