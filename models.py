from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

# Models defined  in this module
class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(200))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    website = db.Column(db.String(200))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(300))
    shows = db.relationship('Show', backref='venues', lazy='true')
    
    def __repr__(self):
      return f'<Artist {self.name} {self.city} {self.state} {self.address} {self.phone} {self.image_link} {self.facebook_link} {self.website} {self.seeking_talent} {self.seeking_description}>'
      

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


