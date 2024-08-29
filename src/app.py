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
    members =jackson_family.get_all_members()# se llama al metodo get all members para obtener los miembros de la familia y se almacena en members
    return jsonify(members),200 #jsonify (members)convierte la lista de miembros en un formato JSON; 200 es un codigo de estado HTTP que indica que la solicitud fue exitosa.
# def handle_hello():
#     # this is how you can use the Family datastructure by calling its methods
#     members = jackson_family.get_all_members()
#     response_body = {
#         "hello": "world",
#         "family": members
#     }
#     return jsonify(response_body), 200

#Devuelve el miembro de la familia para el cual id == member_id.
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member=jackson_family.get_member(member_id)
    if member:
        return jsonify(member),200
    else:
        return jsonify({"mensaje": "Miembro no encontrado"}),404

#Añadir (POST) un miembro
@app.route('/member', methods=['POST'])#¿ESTA BIEN QUE EN UNA SOLA RUTA PONGAMOS GET ALL MEMBERS, CON ADD NEW MEBERS?
def add_new_member():
    # se almacenan y se obtienen los datos de body 
    new_member=request.json
    # Agregamos el nuevo miembro utilizando el método add_member
    jackson_family.add_member(new_member)
    # Devolvemos la lista actualizada de miembros
    members = jackson_family.get_all_members()
    return jsonify(members), 200

    # jackson_family.add_member(new_member)
    # return jsonify(new_member),200

#ELIMINA un miembro
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    response=jackson_family.delete_member(member_id) #Elimina al miembro con el ID dado
    print(response)
    if response["done"]:
        return jsonify(response),200
    return jsonify(response),400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
