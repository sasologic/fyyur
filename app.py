#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, abort, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import ForeignKey
from forms import *
from flask_migrate import Migrate
from models import Venue, Artist, Show, db

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_pyfile('config.py')

moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)




# TODO: connect to a local postgresql database
## Connection to db done


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

  


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
 
  overall_results = []
 
  # Issue a query for unique city and state venues  
  venue_query = Venue.query.distinct(Venue.city).distinct(Venue.state).all()
  
   
  for result in venue_query:
    city_state_data = {
      "city": result.city,
      "state": result.state
    }
    
    venues_by_city_state = Venue.query.filter(Venue.city==result.city).filter(Venue.state==result.state).all()
    
    venues_data = []
    current_time = datetime.now()
    
    for venue in venues_by_city_state:
      venues_data.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len(list(filter(lambda x: x.start_time > current_time, venue.shows)))
      })
      
      city_state_data['venues']= venues_data
    
    overall_results.append(city_state_data)
  
  return render_template('pages/venues.html',areas=overall_results)
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term')
  search_term = search_term.strip()
  search_results = []
  search_venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  
  for venue in search_venues:
    search_results.append( {
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": len(Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time > datetime.now()).all()),
      } )
    
  response = {
    "count": len(search_results),
    'data': search_results
  }  
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  # Issue  a query for a specific venue using primary key
  venue = Venue.query.get(venue_id)
  
  # Define results variables 
  
  past_shows = []
  up_coming_shows = []
    
  done_shows = Show.query.join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
  undone_shows = Show.query.join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time >datetime.now()).all()
  
  for done_show in done_shows:
    past_shows.append({
      "artist_id": done_show.artists.id,
      "artist_name": done_show.artists.name,
      "artist_image_link": done_show.artists.image_link,
      "start_time": format_datetime(str(done_show.start_time))
      })
    
  for undone_show in undone_shows: 
    up_coming_shows.append( {
      "artist_id": undone_show.artists.id,
      "artist_name": undone_show.artists.name,
      "artist_image_link": undone_show.artists.image_link,
      "start_time": format_datetime(str(undone_show.start_time))
      })
      
  data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": up_coming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(up_coming_shows)
      }
      
  
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # instantiate form object
  
  form = VenueForm(request.form)
  # TODO: modify data to be the data object returned from db insertion
  # Retreive form-data from form
  
  try:
    name = form.name.data
    city = form.city.data
    state = form.state.data
    address = form.address.data
    phone = form.phone.data
    image_link = form.image_link.data
    genres =  request.form.getlist('genres')
    facebook_link = form.facebook_link.data
    website_link = form.website_link.data
    seeking_talent = form.seeking_talent.data
    seeking_description = form.seeking_description.data
    
  # Instantiate Venue object
    new_venue = Venue(name=name,city=city,state=state,address=address,phone=phone,
    image_link=image_link,genres=genres,facebook_link=facebook_link,
    website=website_link,seeking_talent=seeking_talent,seeking_description=seeking_description)
    db.session.add(new_venue)
    db.session.commit()

    # on successful db insert, flash success
    flash('Venue ' + form.name.data + ' was successfully added to the list of venues!')
      
  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + form.name.data + ' could not be created as valid venue')  
    
  finally:
    db.session.close()
  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # return None
 
 
  # Execute a query to store retrieve venue based on venue_id
  print("I am here")
  venue_to_delete = Venue.query.get(venue_id)
  
  # Delete the venue from the db in a try block
  try:
    db.session.delete(venue_to_delete)
    # On successful db delete, flash success
    db.session.commit()
    flash('Venue ' + venue_to_delete.name + ' successfully deleted from the list of venues')
    
  except:
    db.session.rollback()
    flash('Venue ' + venue_to_delete.name + ' was not successfully deleted from the list of venues')
    
    
  finally:
    db.session.close()
  return redirect(url_for('index'))  
 

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # Issue a query for all artists
  artists = Artist.query.order_by(Artist.id).all()
  
  data = []
  
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name,
    })
  
 
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  # Get search term
  search_term = request.form.get('search_term')
  search_results = []
  data = []
  # Execute a query for partal case-insensitive string search
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  
  for artist in artists:
    num_upcoming_shows = len(list(filter(lambda show: show.start_time > datetime.now(), artist.shows)))
    # num_upcoming_shows = Artist.query.join(Show).filter(Show.start_time > datetime.now()).all()
    
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": num_upcoming_shows
   } )
    
  search_results.append({
      "count": len(artists),
      "data": data
    })
    
  return render_template('pages/search_artists.html', results=search_results[0], search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
   # Issue  a query for a specific venue using primary key
  artist = Artist.query.get(artist_id)
  
  # Define results variables 
  
  past_shows = []
  up_coming_shows = []
  current_time =  datetime.now()
  done_shows = Show.query.join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time < current_time).all()
  undone_shows = Show.query.join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time > current_time).all()
  
  for done_show in done_shows:
    past_shows.append({
      "venue_id": done_show.venues.id,
      "venue_name": done_show.venues.name,
      "venue_image_link": done_show.venues.image_link,
      "start_time": format_datetime(str(done_show.start_time))
      })
    
  for undone_show in undone_shows: 
    up_coming_shows.append( {
      "venue_id": undone_show.venues.id,
      "venue_name": undone_show.venues.name,
      "venue_image_link": undone_show.venues.image_link,
      "start_time": format_datetime(str(undone_show.start_time))
      })
      
  data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website_link": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": up_coming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(up_coming_shows)
      }
      
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  # TODO: populate form with fields from artist with ID <artist_id>
  
  form = ArtistForm()
  # Query for a partcular artist's record
  artist = Artist.query.get_or_404(artist_id)
  
  if not artist:
    flash('Artist does not exist')
    abort(500)
    
  else:
    form = ArtistForm(
    id=artist.id,name=artist.name, city=artist.city,state=artist.state,
    phone=artist.phone, image_link=artist.image_link,genres=artist.genres,
    facebook_link=artist.facebook_link, website_link=artist.website_link,
    seeking_seeking=artist.seeking_venue, seeking_description=artist.seeking_description)
  
  
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  # Get artist's record from db
  artist = Artist.query.get_or_404(artist_id)
  
  # Initialize form
  form = ArtistForm(request.form)
  
  #Capture data from artist form
  
  try:
    name = form.name.data
    genres = request.form.getlist('genres')
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    website_link = form.website_link.data
    facebook_link = form.facebook_link.data
    seeking_venue = form.seeking_venue.data
    seeking_description = form.seeking_description.data
    image_link = form.image_link.data
    
  # Update artist record  with values from form submitted
    artist.name = name
    artist.genres = genres
    artist.city = city
    artist.state = state
    artist.phone = phone
    artist.website_link = website_link
    artist.facebook_link = facebook_link
    artist.seeking_venue = seeking_venue
    artist.seeking_description = seeking_description
    artist.image_link = image_link
  
  # Save new artist's record into db
    
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + form.name.data + ' was updated successfully')
     
  
  except Exception as e:
    print(e)
    abort(500)
  
  finally:
    db.session.close()
    
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  # TODO: populate form with values from venue with ID <venue_id>
 
  form = VenueForm()
  
  venue = Venue.query.get_or_404(venue_id)
  
  if not venue:
    flash('Venue does not exist')
    abort(500)
  else:
    form = VenueForm(
    id=venue.id,name=venue.name, city=venue.city,state=venue.state,address=venue.address,
    phone=venue.phone, image_link=venue.image_link,genres=venue.genres,
    facebook_link=venue.facebook_link, website_link=venue.website,
    seeking_talent=venue.seeking_talent, seeking_description=venue.seeking_description)
    
 
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  
  form = VenueForm(request.form)
  
  # Get venue record from form submitted
  venue = Venue.query.get_or_404(venue_id)
  
  try:
    name = form.name.data
    city = form.city.data
    state = form.state.data
    address = form.address.data
    phone = form.phone.data
    image_link = form.image_link.data
    genres = request.form.getlist('genres')
    facebook_link = form.facebook_link.data
    website_link = form.website_link.data
    seeking_talent = form.seeking_talent.data
    seeking_description = form.seeking_description.data
    
  # Update Venue object with values obtained from form
    venue.name=name
    venue.city=city
    venue.state=state
    venue.address=address
    venue.phone = phone
    venue.image_link=image_link
    venue.genres=genres
    venue.facebook_link=facebook_link
    venue.website=website_link
    venue.seeking_talent = seeking_talent
    venue.seeking_description=seeking_description
    
    db.session.add(venue)
    db.session.commit()

    # on successful db update, flash success
    flash('Venue ' + form.name.data + ' was successfully updated')
     
  except:
      db.session.rollback()
    
      flash('An error occurred. Venue ' + form.name.data + ' could not be updated')  
    
  finally:
      db.session.close()
      return redirect(url_for('show_venue', venue_id=venue_id))
  
  
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form=ArtistForm(request.form)
  
  try:
    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    image_link = form.image_link.data
    genres = request.form.getlist('genres')
    facebook_link = form.facebook_link.data
    website_link = form.website_link.data
    seeking_venue = form.seeking_venue.data
    seeking_description = form.seeking_description.data
      
    # Instantiate Artist object
    new_artist = Artist(name=name,city=city,state=state,phone=phone,
    image_link=image_link,genres=genres,facebook_link=facebook_link,
    website_link=website_link,seeking_venue=seeking_venue,seeking_description=seeking_description)
    db.session.add(new_artist)
    db.session.commit()

  # on successful db insert, flash success
    flash('Artist ' + form.name.data + ' was successfully listed!')

  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed as valid artist')  
    
  finally:
    db.session.close()
  
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  
  # Execute shows with joins form artist and venues models
  shows_query = Show.query.join(Artist).join(Venue).all()

  # Define data array that will hold final results
  data = []
  
  for show in shows_query:
    data.append({
    "venue_id": show.venues.id,
    "venue_name": show.venues.name,
    "artist_id": show.artists.id,
    "artist_name": show.artists.name,
    "artist_image_link": show.artists.image_link,
    "start_time": format_datetime(str(show.start_time))
    })
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


  form = ShowForm(request.form)
  
  try:
    # Receive data from form
    artist_id = form.artist_id.data
    venue_id = form.venue_id.data
    start_time = form.start_time.data
    
    # Instantiate new Show
    new_show = Show(artist_id=artist_id,venue_id=venue_id,start_time=start_time)

    db.session.add(new_show)
    db.session.commit()
    flash('Show was successfully listed')
    
  except Exception as e:
    print(e)
    db.session.rollback()
    flash('Show was not successfully listed')
  
  finally:
    db.session.close()
  
  return render_template('pages/home.html')
  
 

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
