"""Flask app for Cupcakes"""

from flask import Flask, render_template, redirect, request, flash, jsonify

from models import DEFAULT_IMAGE_URL, db, connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get('/api/cupcakes')
def get_all_cupcakes():
    """Get data about all cupcakes.

    Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
    """

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Get data about a single cupcake.

    Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.post('/api/cupcakes')
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request.

    Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json.get("image") or None

    new_cupcake = Cupcake(flavor=flavor,size=size,rating=rating,image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized),201)


@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupcake(cupcake_id):
    """Update a cupcake using the id passed in the URL and the cupcake data
    passed in the body of the request. The request body may include flavor,
    size, rating and image data but not all fields are required."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.id = cupcake.id
    cupcake.flavor = request.json.get("flavor") or cupcake.flavor
    cupcake.size = request.json.get("size") or cupcake.size
    cupcake.rating = request.json.get("rating") or cupcake.rating

    if request.json.get("image") == "":
        cupcake.image = DEFAULT_IMAGE_URL
    else:
        cupcake.image = request.json.get("image") or cupcake.image

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """Delete cupcake with the id passed in the URL. Respond with JSON like
    {deleted: [cupcake-id]}."""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify({"deleted": cupcake_id})
