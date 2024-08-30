"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
#endpoints
#Obtén todos los miembros de la familia:
@app.route('/members', methods=['GET']) #se establece la ruta URL '/members' que acepta solicitudes GET(para obtener datos)
def get_members():
    try:
        members =jackson_family.get_all_members()# se llama al metodo get all members para obtener los miembros de la familia y se almacena en members
        if members==[]:
            return jsonify({"msg":"not found members"}),404
        return jsonify(members),200 #jsonify (members)convierte la lista de miembros en un formato JSON; 200 es un codigo de estado HTTP que indica que la solicitud fue exitosa.
    except Exception as e:
        return jsonify({'error': 'Internal server error','message':str(e)}),500


# @app.route('/member/<int:member_id>', methods=['GET'])
# def get_member(member_id):
#     member=jackson_family.get_member(member_id)
#     if member:
#         return jsonify(member),200
#     else:
#         return jsonify({"mensaje": "Miembro no encontrado"}),404

#Devuelve el miembro de la familia para el cual id == member_id.
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id) # Intentamos obtener el miembro por su ID
        if member:
            return jsonify(member), 200 # Si se encuentra el miembro, se devuelve en formato JSON con un código 200 (éxito)
        else:
            return jsonify({"mensaje": "Miembro no encontrado"}), 404 # Si no se encuentra el miembro, se devuelve un mensaje de error con un código 404 (no encontrado)
    except Exception as e: 
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500 # Si ocurre algún error inesperado, se captura la excepción y se devuelve un mensaje de error con un código 500 (error interno del servidor)


#Añadir (POST) un miembro
@app.route('/member', methods=['POST'])
def add_new_member():
    try:
        # Se almacenan y se obtienen los datos de body
        new_member = request.json
        if not new_member:
            return jsonify({"error": "No se proporcionaron datos para el nuevo miembro"}), 400 # Si no se envían datos, se devuelve un error 400 (solicitud incorrecta)

        # Agregamos el nuevo miembro utilizando el método add_member
        jackson_family.add_member(new_member)
        
        # Devolvemos la lista actualizada de miembros
        members = jackson_family.get_all_members()
        return jsonify(members), 200 # Se devuelve la lista actualizada de miembros con un código 200 (ok éxito)
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500 # Si ocurre algún error inesperado, se captura la excepción y se devuelve un mensaje de error con un código 500 (error interno del servidor)

    # jackson_family.add_member(new_member)
    # return jsonify(new_member),200

#ELIMINA un miembro
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        response=jackson_family.delete_member(member_id) #Elimina al miembro con el ID dado
        print(response)
        if response["done"]:
            return jsonify(response),200
        return jsonify(response),400
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
