from flask import Flask, render_template, request
import mysql.connector # <-- 1. Importación necesaria

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/incidencia", methods=["POST"])
def crear_incidencia():
    usuario = request.form["usuario"]
    email = request.form["email"]
    aula = request.form["aula"]
    tipo = request.form["tipo"]
    prioridad = request.form["prioridad"]
    descripcion = request.form["descripcion"]

    # 3. Bloque try-except para evitar que la app explote si la BBDD falla
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="incidencias",
            password="incidencias",
            database="incidencias"
        )
        cursor = conexion.cursor()

        # 2. Corregido: 6 columnas y 6 parámetros %s
        sql = """
            INSERT INTO registro
            (aula, descripcion, usuario, estado)
            VALUES (%s, %s, %s, %s)
        """

        valores = (
            aula, 
            descripcion, 
            usuario, 
            "ABIERTA"
        )

        cursor.execute(sql, valores)
        conexion.commit()
        
    except mysql.connector.Error as error:
        # Si la base de datos falla, mostramos un error controlado
        return f"<h2>Error al guardar en la base de datos: {error}</h2>"
        
    finally:
        # El bloque finally asegura que las conexiones se cierren SIEMPRE, 
        # haya habido error o no. Vital para no saturar el servidor.
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()
    
    # 4. Si todo ha ido bien, devolvemos el HTML (Recuerda la vulnerabilidad XSS que comentamos antes)
    return f"""
    <h2>Incidencia recibida correctamente</h2>
    <ul>
        <li><strong>Usuario del alumno:</strong> {usuario}</li>
        <li><strong>Email:</strong> {email}</li>
        <li><strong>Tipo de incidencia:</strong> {tipo}</li>
        <li><strong>Prioridad:</strong> {prioridad}</li>
        <li><strong>Descripción:</strong> {descripcion}</li>
    </ul>
    <br>
    <a href="/">Volver al formulario</a>
    """

if __name__ == "__main__":
    app.run(debug=True)