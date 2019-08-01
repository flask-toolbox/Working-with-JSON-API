# Working with JSON-API

[How to build a JSON API with Python](https://www-freecodecamp-org.cdn.ampproject.org/c/s/www.freecodecamp.org/news/build-a-simple-json-api-in-python/amp/)

[json:api - A SPECIFICATION FOR BUILDING APIS IN JSON](https://jsonapi.org/)

## Requirements

## Install

Prepare source folder

    mkdir flask-jsonapi-demo
    cd    flask-jsonapi-demo

Install Flask and required modules

    pip install flask flask-rest-jsonapi flask-sqlalchemy

## Call API

Basic
    http://localhost:5000/artists

Relations
    http://localhost:5000/artists/1/relationships/artworks
    http://localhost:5000/artists/1?include=artworks
    http://localhost:5000/artists/1?include=artworks&fields[artwork]=title

Sorting and Filtering
    http://localhost:5000/artists?sort=birth_year.
    http://localhost:5000/artists?filter=[{%22name%22:%22birth_year%22,%22op%22:%22gt%22,%22val%22:1900}]

Pagination
    http://localhost:5000/artists?page[size]=2&page[number]=2



## Post

curl -i -X POST -H 'Content-Type: application/json' -d '{"data": "type":"artist", "attributes":{"name":"Salvador Dali", "birth_year":1904, "genre":"Surrealism"}}}' http://localhost:5000/artists


curl -i -X POST -H 'Content-Type: application/json' -d '{"data":{"type":"artwork", "attributes":{"title":"The Persistance of Memory", "artist_id":1}}}' http://localhost:5000/artworks