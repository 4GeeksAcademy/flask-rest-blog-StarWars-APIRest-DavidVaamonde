"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Vehicles, Species, Favourites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



#
# Endpoints GET
#
#
# Genera la ruta People
#
@app.route('/people', methods=['GET'])
def get_all_characters():

    characters = Characters.query.all()

    if not characters:
        return jsonify({ "msg": "Characters not found"}), 404
    
    response_body = [character.serialize() for character in characters]
    
    return jsonify(response_body), 200

#
# Genera la ruta People que indica a un personaje
#
@app.route('/people/<int:character_id>', methods=['GET'])
def get_character(character_id):

    character = Characters.query.get(character_id)

    if character is None:
        return jsonify({ "msg": "Character not found"}), 404
    
    response_body = character.serialize()
    
    return jsonify(response_body), 200

#
# Genera la ruta Planets
#
@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planets.query.all()

    if not planets:
        return jsonify({ "msg": "Planets not found"}), 404
    
    response_body = [planet.serialize() for planet in planets]
    
    return jsonify(response_body), 200

#
# Genera la ruta Planets que indica a un planeta
#
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({ "msg": "Planet not found"}), 404
    
    response_body = planet.serialize()
    
    return jsonify(response_body), 200

#
# Genera la ruta Vehicles
#
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():

    vehicles = Vehicles.query.all()

    if not vehicles:
        return jsonify({ "msg": "Vehicles not found"}), 404
    
    response_body = [vehicle.serialize() for vehicle in vehicles]
    
    return jsonify(response_body), 200

#
# Genera la ruta Vehicles que indica a un vehiculo
#
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):

    vehicle = Vehicles.query.get(vehicle_id)

    if vehicle is None:
        return jsonify({ "msg": "Vehicle not found"}), 404
    
    response_body = vehicle.serialize()
    
    return jsonify(response_body), 200

#
# Genera la ruta Species
#
@app.route('/species', methods=['GET'])
def get_all_species():

    species = Species.query.all()

    if not species:
        return jsonify({ "msg": "Species not found"}), 404
    
    response_body = [specie.serialize() for specie in species]
    
    return jsonify(response_body), 200

#
# Genera la ruta Species que indica a una especie
#
@app.route('/species/<int:specie_id>', methods=['GET'])
def get_specie(specie_id):

    specie = Species.query.get(specie_id)

    if specie is None:
        return jsonify({ "msg": "Specie not found"}), 404
    
    response_body = specie.serialize()
    
    return jsonify(response_body), 200

#
# Enpoint POST
#
#
# Crear un nuevo personaje
#
@app.route('/people', methods=['POST'])
def create_character():
    # Obetenemos los datos de la request
    request_data =request.get_json()

    # Verificamos si se han introducido los campos necesarios
    if not request_data.get("name"):
        return jsonify({"error": "El nombre del personaje es obligatorio"}), 400
    
    if not request_data.get("homeworld"):
        return jsonify({"error": "La ciudad natal del personaje es obligatorio"}), 400
    
    # Creamos un nuevo personaje
    new_character = Characters(
        name = request_data.get('name'),
        homeworld = request_data.get('homeworld'),
        description = request_data.get('description', '') # Valor por defecto si no se prporciona
    )

    # Intentaremos añadir el personaje con try/except
    try:
        # Agregar a la sesion y gusrdar en la base de datos
        db.session.add(new_character)
        db.session.commit()

        # Devuelve el personaje creado
        return jsonify(new_character.serialize()), 201 # Aviso 201 --> Creado con exito
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear el personaje: {str(e)}"}), 500 # Aviso 500 --> Error en el servidor
    
#
# Crear un nuevo planeta
#
@app.route('/planets', methods=['POST'])
def create_planet():
    # Obetenemos los datos de la request
    request_data =request.get_json()

    # Verificamos si se han introducido los campos necesarios
    if not request_data.get("name"):
        return jsonify({"error": "El nombre del planeta es obligatorio"}), 400
    
    # Creamos un nuevo planeta
    new_planet = Planets(
        name = request_data.get('name'),
        population = request_data.get('population', 0), # Valor por defecto si no se proporciona
        description = request_data.get('description', '') # Valor por defecto si no se prporciona
    )

    # Si sale error al intentar agregar planeta, hacemos try/except
    try:
        # Agregar a la sesion y gusrdar en la base de datos
        db.session.add(new_planet)
        db.session.commit()

        # Devuelve el personaje creado
        return jsonify(new_planet.serialize()), 201 # Aviso 201 --> Creado con exito
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear el planeta: {str(e)}"}), 500 # Aviso 500 --> Error en el servidor
    
#
# Crear un nuevo vehiculo
#
@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    # Obetenemos los datos de la request
    request_data =request.get_json()

    # Verificamos si se han introducido los campos necesarios
    if not request_data.get("name"):
        return jsonify({"error": "El nombre del vehiculo es obligatorio"}), 400
    
    if not request_data.get("model"):
        return jsonify({"error": "El modelo del vehiculo es obligatorio"}), 400
    
    # Creamos un nuevo vehiculo
    new_vehicle = Vehicles(
        name = request_data.get('name'),
        model = request_data.get('model'), 
        description = request_data.get('description', '') # Valor por defecto si no se prporciona
    )

    # Si sale error al intentar agregar vehiculo, hacemos try/except
    try:
        # Agregar a la sesion y guardar en la base de datos
        db.session.add(new_vehicle)
        db.session.commit()

        # Devuelve el personaje creado
        return jsonify(new_vehicle.serialize()), 201 # Aviso 201 --> Creado con exito
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear el vehiculo: {str(e)}"}), 500 # Aviso 500 --> Error en el servidor
    
#
# Crear una nueva especie
#
@app.route('/species', methods=['POST'])
def create_specie():
    # Obetenemos los datos de la request
    request_data =request.get_json()

    # Verificamos si se han introducido los campos necesarios
    if not request_data.get("name"):
        return jsonify({"error": "El nombre de la especie es obligatorio"}), 400
    
    if not request_data.get("type"):
        return jsonify({"error": "El tipo de la especie es obligatorio"}), 400
    
    # Creamos una nueva especie
    new_specie = Species(
        name = request_data.get('name'),
        type = request_data.get('type'), 
        description = request_data.get('description', '') # Valor por defecto si no se prporciona
    )

    # Si sale error al intentar agregar especie, hacemos try/except
    try:
        # Agregar a la sesion y guardar en la base de datos
        db.session.add(new_specie)
        db.session.commit()

        # Devuelve el personaje creado
        return jsonify(new_specie.serialize()), 201 # Aviso 201 --> Creado con exito
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear la especie: {str(e)}"}), 500 # Aviso 500 --> Error en el servidor
    
#
# Enpoint PUT
#
#
# Actualizar un personaje existente
#
@app.route('/people/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    # Buscamos al personaje por su ID
    character = Characters.query.get(character_id)

    # Verificamos si el personaje existe
    if not character:
        return jsonify({"error": "Personaje no encontrado"}), 404
    
    # Obtenemos los datos de la request
    request_data = request.get_json()

    # Actualizamos los campos si estan presentes en la solicitud
    if "name" in request_data:
        character.name = request_data['name']
    
    if "homeworld" in request_data:
        character.homeworld = request_data['homeworld']

    if "description" in request_data:
        character.description = request_data['description']

    # Si sale error al actualizar personaje, hacemos try/except
    try:
        # Guardamos los cambios en la base de datos
        db.session.commit()

        # Devolvemos (retornamos) el personaje actualizado
        return jsonify(character.serialize()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Error al actualizar el personaje: {str(e)}"}), 500

#
# Actualizar un planeta existente
#
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    # Buscamos al planeta por su ID
    planet = Planets.query.get(planet_id)

    # Verificamos si el planeta existe
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404
    
    # Obtenemos los datos de la request
    request_data = request.get_json()

    # Actualizamos los campos si estan presentes en la solicitud
    if "name" in request_data:
        planet.name = request_data['name']
    
    if "population" in request_data:
        planet.population = request_data['population']

    if "description" in request_data:
        planet.description = request_data['description']

    # Si sale error al actualizar planeta, hacemos try/except
    try:
        # Guardamos los cambios en la base de datos
        db.session.commit()

        # Devolvemos (retornamos) el planeta actualizado
        return jsonify(planet.serialize()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Error al actualizar el planeta: {str(e)}"}), 500

#
# Actualizar un vehiculo existente
#
@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    # Buscamos al vehiculo por su ID
    vehicle = Vehicles.query.get(vehicle_id)

    # Verificamos si el vehiculo existe
    if not vehicle:
        return jsonify({"error": "Vehiculo no encontrado"}), 404
    
    # Obtenemos los datos de la request
    request_data = request.get_json()

    # Actualizamos los campos si estan presentes en la solicitud
    if "name" in request_data:
        vehicle.name = request_data['name']
    
    if "model" in request_data:
        vehicle.model = request_data['model']

    if "description" in request_data:
        vehicle.description = request_data['description']

    # Si sale error al actualizar vehiculo, hacemos try/except
    try:
        # Guardamos los cambios en la base de datos
        db.session.commit()

        # Devolvemos (retornamos) el vehiculo actualizado
        return jsonify(vehicle.serialize()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Error al actualizar el vehiculo: {str(e)}"}), 500


#
# Actualizar una especie existente
#
@app.route('/species/<int:specie_id>', methods=['PUT'])
def update_specie(specie_id):
    # Buscamos a la especie por su ID
    specie = Species.query.get(specie_id)

    # Verificamos si la especie existe
    if not specie:
        return jsonify({"error": "Especie no encontrada"}), 404
    
    # Obtenemos los datos de la request
    request_data = request.get_json()

    # Actualizamos los campos si estan presentes en la solicitud
    if "name" in request_data:
        specie.name = request_data['name']
    
    if "type" in request_data:
        specie.type = request_data['type']

    if "description" in request_data:
        specie.description = request_data['description']

    # Si sale error al actualizar especie, hacemos try/except
    try:
        # Guardamos los cambios en la base de datos
        db.session.commit()

        # Devolvemos (retornamos) la especie actualizada
        return jsonify(specie.serialize()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Error al actualizar la especie: {str(e)}"}), 500


#
# Endpoint DELETE
#
#
# Borrar un personaje existente
#
@app.route('/people/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    # Buscamos al personaje por ID
    character = Characters.query.get(character_id)

    # Verificar si el personaje existe
    if not character:
        return jsonify({"error": "Personaje no encontrado"}), 404
    
    # Si sale error al eliminar personaje, hacemos try/except
    try:
        # Eliminamos el personaje de la base de datos
        db.session.delete(character)
        db.session.commit()

        # Devolver mensaje de exito
        return jsonify({"message": f"Personaje {character_id} eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Error al eliminar el personaje: {str(e)}"}), 500
    
#
# Borrar un planeta existente
#
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    # Buscamos al planeta por ID
    planet = Planets.query.get(planet_id)

    # Verificar si el planeta existe
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404
    
    # Si sale error al eliminar planeta, hacemos try/except
    try:
        # Eliminamos el planeta de la base de datos
        db.session.delete(planet)
        db.session.commit()

        # Devolver mensaje de exito
        return jsonify({"message": f"Planeta {planet_id} eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Error al eliminar el planeta: {str(e)}"}), 500
    
#
# Borrar un vehiculo existente
#
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    # Buscamos al vehiculo por ID
    vehicle = Vehicles.query.get(vehicle_id)

    # Verificar si el vehiculo existe
    if not vehicle:
        return jsonify({"error": "Vehiculo no encontrado"}), 404
    
    # Si sale error al eliminar vehiculo, hacemos try/except
    try:
        # Eliminamos el vehiculo de la base de datos
        db.session.delete(vehicle)
        db.session.commit()

        # Devolver mensaje de exito
        return jsonify({"message": f"Vehiculo {vehicle_id} eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Error al eliminar el vehiculo: {str(e)}"}), 500
    
#
# Borrar una especie existente
#
@app.route('/species/<int:specie_id>', methods=['DELETE'])
def delete_specie(specie_id):
    # Buscamos a la especie por ID
    specie = Species.query.get(specie_id)

    # Verificar si el vehiculo existe
    if not specie:
        return jsonify({"error": "Especie no encontrada"}), 404
    
    # Si sale error al eliminar especie, hacemos try/except
    try:
        # Eliminamos la especie de la base de datos
        db.session.delete(specie)
        db.session.commit()

        # Devolver mensaje de exito
        return jsonify({"message": f"Especie {specie_id} eliminada correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Error al eliminar la especie: {str(e)}"}), 500
    
#
# Usuarios y Favoritos
#
#
# Listar todos los usuarios de la base de datos
#
@app.route('/users', methods=['GET'])
def get_all_users():

    users = User.query.all()

    if not users:
        return jsonify({ "msg": "Users not found"}), 404
    
    response_body = [user.serialize() for user in users]
    
    return jsonify(response_body), 200

#
# Genera la ruta users que indica a un usuario
#
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = User.query.get(user_id)

    if user is None:
        return jsonify({ "msg": "User not found"}), 404
    
    response_body = user.serialize()
    
    return jsonify(response_body), 200

#
# Crear un nuevo usuario
#
@app.route('/users', methods=['POST'])
def create_user():
    # Obetenemos los datos de la request
    request_data =request.get_json()

    # Verificamos si se han introducido los campos necesarios
    if not request_data.get("username"):
        return jsonify({"error": "El nombre de usuario es obligatorio"}), 400
    
    if not request_data.get("email"):
        return jsonify({"error": "El correo electronico es obligatorio"}), 400
    
    if not request_data.get("password"):
        return jsonify({"error": "La contraseña es obligatoria"}), 400
    
    # Creamos un nuevo usuario
    new_user = User(
        username = request_data.get('username'),
        firstname = request_data.get('firstname', ''), # Valor por defecto si no se prporciona
        lastname = request_data.get('lastname', ''), # Valor por defecto si no se prporciona
        email = request_data.get('email'), 
        password = request_data.get('password') 
    )

    # Si sale error al intentar agregar usuario, hacemos try/except
    try:
        # Agregar a la sesion y guardar en la base de datos
        db.session.add(new_user)
        db.session.commit()

        # Devuelve el personaje creado
        return jsonify(new_user.serialize()), 201 # Aviso 201 --> Creado con exito
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear el usuario: {str(e)}"}), 500 # Aviso 500 --> Error en el servidor



#
# Borrar un usuario existente
#
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):    
    # Buscamos a la especie por ID
    user = User.query.get(user_id)

    # Verificar si el usuario existe
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    # Si sale error al eliminar usuario, hacemos try/except
    try:
        # Eliminamos el usuario de la base de datos
        db.session.delete(user)
        db.session.commit()

        # Devolver mensaje de exito
        return jsonify({"message": f"Usuario {user_id} eliminada correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Error al eliminar el usuario: {str(e)}"}), 500
    
# GET - Conseguir todos los favoritos
@app.route('/users/<int:user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):
    # Buscamos todos los favoritos del usuario con el id especificado
    favourites = Favourites.query.filter_by(user_id=user_id).all()

    if not favourites:
        return jsonify({"msg": f"El usuario {user_id} no tiene ningún favorito", "data": []}), 200

    results = []
    for fav in favourites:
        fav_data = {
            "id": fav.id,
            "user_id": fav.user_id
        }

        # Introducimos los datos del planeta si existe
        if fav.planet_id and fav.planet:
            fav_data["planet"] = {
                "id": fav.planet.id,
                "name": fav.planet.name,
                "population": fav.planet.population,
                "description": fav.planet.description
            }

        # Introducimos los datos del personaje si existe
        if fav.character_id and fav.character:
            fav_data["character"] = {
                "id": fav.character.id,
                "name": fav.planet.name,
                "homeworld": fav.planet.homeworld,
                "description": fav.planet.description
            }

        # Introducimos los datos del vehiculo si existe
        if fav.vehicle_id and fav.vehicle:
            fav_data["vehicle"] = {
                "id": fav.vehicle.id,
                "name": fav.vehicle.name,
                "model": fav.vehicle.model,
                "description": fav.vehicle.description
            }

        # Introducimos los datos de la especie si existe
        if fav.specie_id and fav.specie:
            fav_data["specie"] = {
                "id": fav.specie.id,
                "name": fav.specie.name,
                "type": fav.specie.type,
                "description": fav.specie.description
            }

        results.append(fav_data)

    return jsonify({"results_favs": results}), 200

#
# POST - Agregar nuevo favorito para un usuario específico
#
@app.route('/users/<int:user_id>/favourites', methods=['POST'])
def add_user_favourite(user_id):
    request_data = request.get_json()
    
    # Verificar que se proporcionó al menos planet_id, character_id, vehicle_id o specie_id
    if not request_data.get('planet_id') and not request_data.get('character_id') and not request_data.get('vehicle_id') and not request_data.get('specie_id'):
        return jsonify({"error": "Se requiere planet_id, character_id, vehicle_id o specie_id"}), 400
    
    # Crear nuevo favorito con el user_id de la URL
    new_favourite = Favourites(
        user_id = user_id,
        planet_id = request_data.get('planet_id'),
        character_id = request_data.get('character_id'),
        vehicle_id = request_data.get('vehicle_id'),
        specie_id = request_data.get('specie_id')
    )
    
    try:
        # Verificar si el planeta existe (si se proporciona planet_id)
        if request_data.get('planet_id'):
            planet = Planets.query.get(request_data.get('planet_id'))
            if not planet:
                return jsonify({"error": f"El planeta con ID {request_data.get('planet_id')} no existe"}), 404
        
        # Verificar si el personaje existe (si se proporciona character_id)
        if request_data.get('character_id'):
            character = Characters.query.get(request_data.get('character_id'))
            if not character:
                return jsonify({"error": f"El personaje con ID {request_data.get('character_id')} no existe"}), 404
            
        # Verificar si el vehiculo existe (si se proporciona vehicle_id)
        if request_data.get('vehicle_id'):
            vehicle = Vehicles.query.get(request_data.get('vehicle_id'))
            if not vehicle:
                return jsonify({"error": f"El vehiculo con ID {request_data.get('vehiculo_id')} no existe"}), 404
        
        # Verificar si la especie existe (si se proporciona specie_id)
        if request_data.get('specie_id'):
            specie = Species.query.get(request_data.get('specie_id'))
            if not specie:
                return jsonify({"error": f"La especie con ID {request_data.get('specie_id')} no existe"}), 404
        
        # Agregar a la base de datos
        db.session.add(new_favourite)
        db.session.commit()
        
        # Crear respuesta detallada
        response = {
            "id": new_favourite.id,
            "user_id": new_favourite.user_id
        }
        
        # Incluir detalles del planeta
        if new_favourite.planet_id and new_favourite.planet:
            response["planet"] = {
                "id": new_favourite.planet.id,
                "name": new_favourite.planet.name,
                "population": new_favourite.planet.population,
                "description": new_favourite.planet.description
            }
        
        # Incluir detalles del personaje
        if new_favourite.character_id and new_favourite.character:
            response["character"] = {
                "id": new_favourite.character.id,
                "name": new_favourite.character.name,
                "homeworld": new_favourite.planet.homeworld,
                "description": new_favourite.planet.description
            }

        # Incluir detalles del vehiculo
        if new_favourite.vehicle_id and new_favourite.vehicle:
            response["vehicle"] = {
                "id": new_favourite.vehicle.id,
                "name": new_favourite.vehicle.name,
                "model": new_favourite.vehicle.model,
                "description": new_favourite.vehicle.description
            }
    
        # Incluir detalles de la especie
        if new_favourite.specie_id and new_favourite.specie:
            response["specie"] = {
                "id": new_favourite.specie.id,
                "name": new_favourite.specie.name,
                "type": new_favourite.specie.type,
                "description": new_favourite.specie.description
            }
        
        return jsonify(response), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear favorito: {str(e)}"}), 500

#    
# DELETE: Eliminar favorito por ID
#
@app.route('/users/<int:user_id>/favourites/<int:favourite_id>', methods=['DELETE'])
def delete_user_favourite(user_id, favourite_id):
    # Buscar el favorito que pertenezca al usuario especificado
    favourite = Favourites.query.filter_by(id=favourite_id, user_id=user_id).first()
    
    if not favourite:
        return jsonify({"error": "Favorito no encontrado o no pertenece a este usuario"}), 404
    
    try:
        db.session.delete(favourite)
        db.session.commit()
        return jsonify({"success": True, "message": "Favorito eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar favorito: {str(e)}"}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
