from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase): #Creating our Base model that will be inherited by all other models
    pass


## The main thing we want from declarative base is the mapped and mapped column features that it comes with. So when we're setting up our database, we have that map premise already set up for us so that we can kind of create those those fields pretty easily.


db = SQLAlchemy(model_class=Base)