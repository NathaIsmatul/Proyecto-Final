from flask import Flask, request, jsonify
import pyodbc
import cx_Oracle

app = Flask(__name__)

# ---------------------------------------------- SQL SERVER ---------------------------------------------

# Función para configurar la conexión a la base de datos SQL Server
def conexion_sql():
    try:
        sql_conexion = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=LAPTOP-RSA168G3\\SQLSERVER;'
            'DATABASE=HUELLAS_BD;'
            'UID=HUELLAS_USER;'
            'PWD=HuellasDeVida2024;'
        )
        return sql_conexion
    except pyodbc.Error as error:
         # Obtener información detallada del error
        state, message = error.args
        print(f"SQL State: {state}")
        print(f"Error Message: {message}")
        return None

@app.route("/verificacion_datos", methods=["POST"])
def authenticate():
    data = request.get_json()
    print(data)
    nombre = data['nombre']
    contrasena = data['contrasena']

    # Establecer la conexión a la base de datos SQL Server
    conn = conexion_sql()

    if conn:
        cursor = conn.cursor()

        # Realiza la consulta SQL para obtener las opciones de menú
        consulta_sql = """
        SELECT U.id, OM.opciones
        FROM OpcionesMenu OM
        INNER JOIN Usuarios U ON OM.usuarioID = U.id
        WHERE U.usuario = ? AND U.password = ?
        """
        cursor.execute(consulta_sql, (nombre, contrasena))
        # Procesa los resultados de la consulta
        result = cursor.fetchall()
        user_id = result[0][0] if result else None
        menu_options = [opcion[1] for opcion in result]

        # Cerrar la conexión a la base de datos
        conn.close()
    else:
        # Si la conexión no se pudo establecer, maneja el error de alguna manera
        menu_options = []

    # Empaqueta los resultados en formato JSON y responde
    response_data = {
        'user_id': user_id,
        'menu_options': menu_options
    }

    return jsonify(response_data)

# ---------------------------------------------- ORACLE EXPRESS ---------------------------------------------

# Función para configurar la conexión a la base de datos Oracle
def conexion_oracle():
    try:
        # Configura la cadena de conexión de Oracle con tus credenciales
        connection = cx_Oracle.connect('HUELLAS_REFUGIO/Huellas2001@localhost:1521/XE')
        return connection
    except cx_Oracle.Error as error:
        # Maneja la excepción de Oracle aquí
        print(f'Error de Oracle: {error}')
        return None
    
# ---------------------------------------------- Castraciones ---------------------------------------------

@app.route('/recibir_Castraciones', methods=["GET"])
def Recibir_Castraciones():
    # Establecer la conexión a la base de datos Oracle
    connection = conexion_oracle()

    if connection:
        cursor = connection.cursor()

        try:
            # Ejecuta la consulta SQL para obtener las castraciones
            cursor.execute("SELECT id, mascotaID, nombreMascota, raza, fechaCastracion, veterinario FROM Castracion")
            castraciones = cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

        # Empaqueta los resultados en un formato JSON
        json_data = [{'id': row[0], 
                      'mascotaID': row[1], 
                      'nombreMascota': row[2], 
                      'raza': row[3], 
                      'fechaCastracion': str(row[4]), 
                      'veterinario': row[5]} 
                      for row in castraciones]

        return jsonify(json_data)

    # Maneja el caso en el que no se pueda establecer la conexión
    return jsonify({'error': 'Error al conectar con la base de datos'}), 500

# ---------------------------------------------- Registrar Mascota ---------------------------------------------

@app.route('/registrar_Mascotas', methods=["GET"])
def Recibir_Mascotas():
    # Establecer la conexión a la base de datos Oracle
    connection = conexion_oracle()

    if connection:
        cursor = connection.cursor()

        try:
            # Ejecuta la consulta SQL para obtener las mascotas
            cursor.execute("SELECT id, nombreMascota, especie, raza, fechaNacimiento, perfilID FROM RegistroMascotas")
            mascotas = cursor.fetchall()

            # Empaqueta los resultados en un formato JSON
            json_data = [{'id': row[0], 
                          'nombreMascota': row[1], 
                          'especie': row[2], 
                          'raza': row[3], 
                          'fechaNacimiento': str(row[4]), 
                          'perfilID': row[5]} 
                          for row in mascotas]

            return jsonify(json_data)
        finally:
            cursor.close()
            connection.close()

    # Maneja el caso en el que no se pueda establecer la conexión
    return jsonify({'error': 'Error al conectar con la base de datos'}), 500

# ---------------------------------------------- Obtener Catalogo ---------------------------------------------

@app.route('/obtener_Catalogo', methods=['GET'])
def obtener_catalogo():
    # Establecer la conexión a la base de datos Oracle
    connection = conexion_oracle()

    if connection:
        cursor = connection.cursor()

        try:
            # Ejecuta la consulta SQL para obtener la lista de pasteles
            cursor.execute("SELECT id, mascotaID, nombreMascota, raza, edad, descripcion FROM CatalogoAdopciones")
            catalogo = cursor.fetchall()

                       # Empaqueta los resultados en un formato JSON
            json_data = [{'id': row[0], 
                          'mascotaID': row[1], 
                          'nombreMascota': row[2], 
                          'raza': row[3], 
                          'edad': row[4], 
                          'perfilID': row[5]} 
                          for row in catalogo]


            # Devolver los datos en formato JSON
            return jsonify(json_data)
        finally:
            cursor.close()
            connection.close()

    # Manejar el caso en el que no se pueda establecer la conexión
    return jsonify({'error': 'Error al conectar con la base de datos'}), 500


if __name__ == '__main__':
    # Ejecuta la aplicación Flask
    app.run(host='127.0.0.1', port=5005)