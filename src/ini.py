from app import app
from models import db, User, Planets, Characters, Vehicles, Species

with app.app_context():
    
    #
    # Generamos datos por defecto para la base de datos
    #

    users = [
        User(username="pepitochoco", firstname="Pepe",
            lastname="Chocolatero", email="pepechocolatero@gmail.com", password="P3p1t0*hola"),
        User(username="DavidCarola", firstname="David",
            lastname="Carola", email="davidcarola@gmail.com", password="Deivid@67")
    ]
    # Si no existe ningun registro en la base de datos, usar esta condicional:
    if not User.query.first():
        db.session.add_all(users)
        db.session.commit()

    planets = [
        Planets(name="Tatooine", population=38000000,
            description="Un planeta"),
        Planets(name="Estrella de la muerte", population=138000000,
            description="Una estrella DE LA MUERTE")
    ]
    # Si no existe ningun registro en la base de datos, usar esta condicional:
    if not Planets.query.first():
        db.session.add_all(planets)
        db.session.commit()

    characters = [
        Characters(name="Luke Skywalker", homeworld="Tattooine",
            description="Protagonista que se convierte en Darth Vader"),
        Characters(name="Obiwan Kenobi", homeworld="Tattione",
            description="Maestro de Luke Skywalker")
    ]
    # Si no existe ningun registro en la base de datos, usar esta condicional:
    if not Characters.query.first():
        db.session.add_all(characters)
        db.session.commit()

    vehicles = [
        Vehicles(name="Ala-A", model="Slash",
            description="Caza espacial de Star Wars"),
        Vehicles(name="Destructor estelar", model="Clase imperial",
            description="Espina dorsal de la armada imperial de Star Wars")
    ]
    # Si no existe ningun registro en la base de datos, usar esta condicional:
    if not Vehicles.query.first():
        db.session.add_all(vehicles)
        db.session.commit()

    species = [
        Species(name="Chewbacca", type="Wookie",
            description="Mejor amigo de Han Solo"),
        Species(name="Jar jar binks", type="Gungan",
            description="Amigo divertido de Luke Skywalker")
    ]
    # Si no existe ningun registro en la base de datos, usar esta condicional:
    if not Species.query.first():
        db.session.add_all(species)
        db.session.commit()

print("Iniciar base de datos")