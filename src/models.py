from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Relación uno a muchos con Favourites, la tabla muchos
    id_user = relationship("Favourites", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }


class Favourites(db.Model):
    __tablename__ = "favourites"
    id = Column(Integer, primary_key=True)

    # Relación muchos a uno con User, la tabla "uno"
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="id_user")

    # Relación muchos a uno con Planet, la tabla "uno"
    planet_id = Column(Integer, ForeignKey('planets.id'))
    planet = relationship("Planets", back_populates="id_planet")

    # Relación muchos a uno con Character, la tabla "uno"
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Characters", back_populates="id_character")

    # Relación muchos a uno con Vehicle, la tabla "uno"
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    vehicle = relationship("Vehicles", back_populates="id_vehicle")

    # Relación muchos a uno con Species, la tabla "uno"
    specie_id = Column(Integer, ForeignKey('species.id'))
    specie = relationship("Species", back_populates="id_specie")
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            "vehicle_id": self.vehicle_id,
            "specie_id": self.specie_id,
        }


class Planets(db.Model):
    __tablename__ = "planets"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    population= Column(Integer)
    description = Column(String(250))

    # Relación uno a muchos con Favourites, la tabla muchos
    id_planet = relationship("Favourites", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "description": self.description,
            "id_planet": self.id_planet,
        }


class Characters(db.Model):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    homeworld = Column(String(50))
    description = Column(String(250))

    # Relación uno a muchos con Favourites, la tabla muchos
    id_character = relationship("Favourites", back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "homeworld": self.homeworld,
            "description": self.description,
            "id_character": self.id_character,
        }


class Vehicles(db.Model):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    model = Column(String(100))
    description = Column(String(250))

    # Relación uno a muchos con Favourites, la tabla muchos
    id_vehicle = relationship("Favourites", back_populates="vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "description": self.description,
            "id_vehicle": self.id_vehicle,
        }
    

class Species(db.Model):
    __tablename__ = "species"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column(String(100))
    description = Column(String(250))

    # Relación uno a muchos con Favourites, la tabla muchos
    id_specie = relationship("Favourites", back_populates="specie")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "id_species": self.id_specie,
        }