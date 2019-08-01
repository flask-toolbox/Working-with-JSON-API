from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound

from sqlalchemy.orm.exc import NoResultFound

from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields

from sqlalchemy.orm import relationship

import sys
import os
basedir = os.path.abspath(os.path.dirname(__file__))


def debug(line):
    print('DEBUG: %s', line)


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Create a new Flask application
debug('create flask app')
app = Flask(__name__)
app.config.from_object(Config)

debug('create db app')
db = SQLAlchemy(app)

debug('define Artists')
# Define a class for the Artist table


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birth_year = db.Column(db.Integer)
    genre = db.Column(db.String)

    def __repr__(self):
        return '<name %r>' % self.name


class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship('Artist', backref=db.backref('artworks'))


class ArtistSchema(Schema):
    class Meta:
        type_ = 'artist'
        self_view = 'artist_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'artist_many'

    id = fields.Integer()
    name = fields.Str(required=True)
    birth_year = fields.Integer(load_only=True)
    genre = fields.Str()

    artworks = Relationship(self_view='artist_artworks',
                            self_view_kwargs={'id': '<id>'},
                            related_view='artwork_many',
                            many=True,
                            schema='ArtworkSchema',
                            type_='artwork')


class ArtworkSchema(Schema):
    class Meta:
        type_ = 'artwork'
        self_view = 'artwork_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'artwork_many'

    id = fields.Integer()
    title = fields.Str(required=True)
    artist_id = fields.Integer(required=True)


class ArtworkMany(ResourceList):
    schema = ArtworkSchema
    data_layer = {'session': db.session, 'model': Artwork}


class ArtworkOne(ResourceDetail):
    schema = ArtworkSchema
    data_layer = {'session': db.session, 'model': Artwork}


class ArtistArtwork(ResourceRelationship):
    schema = ArtistSchema
    data_layer = {'session': db.session, 'model': Artist}


api = Api(app)
api.route(ArtworkOne, 'artwork_one', '/artworks/<int:id>')
api.route(ArtworkMany, 'artwork_many', '/artworks')
api.route(ArtistArtwork, 'artist_artworks',
          '/artists/<int:id>/relationships/artworks')

# main loop to run app in debug mode
if __name__ == '__main__':
    # Create the table
    db.create_all()

    app.run(debug=True)
