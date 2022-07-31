from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

# Models defined  in this module

class Venues(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(200), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(200), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(300), nullable=False)
    shows = db.relationship('Show', backref='venues', lazy='true')
    
    def __repr__(self):
      return f'<Artist {self.name} {self.city} {self.state} {self.address} {self.phone} {self.image_link} {self.facebook_link} {self.website} {self.seeking_talent} {self.seeking_description}>'
      

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artists(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(100))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    shows = db.relationship('Show', backref='artists', lazy='dynamic')
    
    
    def __repr__(self):
      return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.image_link} {self.facebook_link}>'
      

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Shows(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    
    def __repr__(self):
      return f'<Show {self.id} start_time: {self.start_time} artist_id: {self.artist_id} venue_id: {self.venue_id} >'
  