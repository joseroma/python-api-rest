from flask import Flask, jsonify, abort, request, make_response
import mysql.connector

app = Flask(__name__)

# Queries
query = ("SELECT * FROM ACTOR;")
query1 = ("SELECT p.oid_pelicula,  p.titulo,p.fecha_lanzamiento,p.genero, a.oid_ACTOR, a.nombre, a.apellido FROM ACTOR a, PELICULA_has_ACTOR m, PELICULA p WHERE p.oid_pelicula = m.PELICULA_oid_pelicula AND a.oid_ACTOR = m.ACTOR_oid_ACTOR;")
query2 = ("SELECT * FROM DIRECTOR;")
query3 = ("SELECT p.oid_pelicula,  p.titulo,p.fecha_lanzamiento,p.genero, a.oid_director, a.name  FROM DIRECTOR a, PELICULA_has_DIRECTOR m, PELICULA p WHERE p.oid_pelicula = m.PELICULA_oid_pelicula AND a.oid_director = m.DIRECTOR_oid_director;")
query4 = ("SELECT * FROM PELICULA;")

# Conections
cnx = mysql.connector.connect(user='root', password='password',host='127.0.0.1',database='filmAffinity3')
cnx1 = mysql.connector.connect(user='root', password='password',host='127.0.0.1', database='filmAffinity3')
cnx2 = mysql.connector.connect(user='root', password='password',host='127.0.0.1', database='filmAffinity3')
cnx3 = mysql.connector.connect(user='root', password='password',host='127.0.0.1', database='filmAffinity3')
cnx4 = mysql.connector.connect(user='root', password='password',host='127.0.0.1', database='filmAffinity3')

# Get list from connection
cursor = cnx.cursor()
cursor.execute(query)
cursor1 = cnx1.cursor()
cursor1.execute(query1)
cursor2 = cnx2.cursor()
cursor2.execute(query2)
cursor3 = cnx3.cursor()
cursor3.execute(query3)
cursor4 = cnx4.cursor()
cursor4.execute(query4)

actors = []
actors_pelicula = []
directors = []
directors_movies = []
movies_ = []
movies_directors = []

for res in cursor:
    actors.append({
    "id":res[0],
    "name":res[1],
    "lastname":res[2],
    "birth_date":res[3]
})


for res in cursor1:
    actors_pelicula.append({
            "id_film": res[0],
            "title_film": res[1],
            "date_film": res[2],
            "genre_film": res[3],
            "id_actor": res[4],
            "name_actor": res[5],
            "lastname_actor": res[6]
    })

for res in cursor2:
    directors.append({
        "id": res[0],
        "name": res[1]
})

for res in cursor3:
    directors_movies.append({
        "id_film": res[0],
        "title_film": res[1],
        "date_film": res[2],
        "genre_film": res[3],
        "id_director": res[4],
        "name_director": res[5]
})

for res in cursor4:
    movies_.append({
        "id": res[0],
        "title": res[1],
        "year": res[3],
        "genre": res[4]
    })

#Close cursors and connections
cursor.close()
cnx.close()
cursor1.close()
cnx1.close()
cursor2.close()
cnx2.close()
cursor3.close()
cnx3.close()
cursor4.close()
cnx4.close()

@app.route('/')
def hello_world():
    return 'Welcome to the REST-API !'


##############
#GET METHODS
##############
#-----------
# ACTORS
#-----------

@app.route('/api/actors', methods=['GET'])
def get_actors():
    name = request.args.get('name')
    if name:
        actor = [actor for actor in actors if actor['name'] == name]
        return jsonify({"Actors": actor})
    else:
        return jsonify({"Actors": actors})


@app.route('/api/actors/<int:id>', methods=['GET'])
def get_actors_(id):
    actor = [actor for actor in actors if actor['id'] == id]
    return jsonify({"Actor": actor[0]})


@app.route('/api/actors/<int:id>/movies', methods=['GET'])
def get_actors_movies(id):
    pel= [pel for pel in actors_pelicula if pel['id_actor'] == id]
    return jsonify({"MoviesOfActor": pel})


@app.route('/api/actors/<int:id>/movies/<int:id2>', methods=['GET'])
def get_actors_movies_specific(id,id2):
    pel = [pel for pel in actors_pelicula if pel['id_film'] == id2]
    if pel:
        pelo = [pelo for pelo in pel if pelo['id_actor'] == id]
        if pelo:
            res = jsonify({"MoviesOfActor": pelo})
        else:
            res = jsonify({"Ese actor no ha participado en esa pelicula": pel})
    else:
        res = jsonify({"Esa pelicula no existe": pel})
    return res


#-----------
# DIRECTORS
#-----------


@app.route('/api/directors', methods=['GET'])
def get_directors():
    name =request.args.get('name')
    #http://localhost:5000/api/directors?name=Poland
    if name:
        director = [director for director in directors if director['name'] == name]
        return jsonify({"Directors": director})
    #http://localhost:5000/api/directors
    else:
        return jsonify({"Directors": directors})


@app.route('/api/directors/<int:id>', methods=['GET'])
def get_directors_id(id):
    director = [director for director in directors if director['id'] == id]
    return jsonify({"Director": director})


@app.route('/api/directors/<int:id>/movies', methods=['GET'])
def get_director_movies(id):
    dir = [dir for dir in directors_movies if dir['id_director'] == id]
    return jsonify({"MoviesOfActor": dir})


@app.route('/api/directors/<int:id>/movies/<int:id2>', methods=['GET'])
def get_directors_movies_specific(id, id2):
    dir = [dir for dir in directors_movies if dir['id_film'] == id2]
    if dir:
        diro = [diro for diro in dir if diro['id_director'] == id]
        if diro:
            res = jsonify({"MoviesOfActor": diro})
        else:
            res = jsonify({"Ese director no ha participado en esa pelicula": dir})
    else:
        res = jsonify({"Esa pelicula no existe": dir})
    return res

#-----------
# MOVIES
#-----------

@app.route('/api/movies', methods=['GET'])
def get_movies():
    title =request.args.get('title')
    genre = request.args.get('genre')
    year = request.args.get('year')
    #http://localhost:5000/api/wizards?house=Gryffindor
    if genre:
        mov = [mov for mov in movies_ if mov['genre'] == genre]
        return jsonify({"Movies": mov})
    elif(title):
        mov = [mov for mov in movies_ if mov['title'] == title]
        return jsonify({"Movies": mov})
    elif(year):
        mov = [mov for mov in movies_ if mov['year'] == year]
        return jsonify({"Movies": mov})
    elif(genre and title and year):
        mov = [mov for mov in movies_ if mov['genre'] == genre and mov['year'] == year and mov['title'] == title ]
        return jsonify({"Movies": mov})
    #http://localhost:5000/api/wizards
    else:
        return jsonify({"Movies": movies_})


@app.route('/api/movies/<int:id>', methods=['GET'])
def get_movies_id(id):
    mov = [mov for mov in movies_ if mov['id'] == id]
    return jsonify({"Director": mov})


@app.route('/api/movies/<int:id>/director', methods=['GET'])
def get_director_of_movies(id):
    dir = [dir for dir in directors_movies if dir['id_film'] == id]
    return jsonify({"MoviesOfActor": dir})

@app.route('/api/movies/<int:id>/actors', methods=['GET'])
def get_actors_of_movies(id):
    act = [act for act in actors_pelicula if act['id_film'] == id]
    return jsonify({"MoviesOfActor": act})


@app.route('/api/movies/<int:id>/actors/<int:id2>', methods=['GET'])
def get_actors__of_movies_specific(id, id2):

    act = [act for act in actors_pelicula if act['id_actor'] == id2]
    if act:
        act_val = [act_val for act_val in act if act_val['id_film'] == id]
        if act_val:
            res = jsonify({"MoviesOfActor": act_val})
        else:
            res = jsonify({"Ese actor no ha participado en ninguna de estas pelis": act})
    else:
        res = jsonify({"Ese actor no existe": "prueba otro mejor"})

    return res

##############
#POST METHODS
##############


@app.route('/api/actors', methods=['POST'])
def create_actor():
    if not request.json or not 'name' in request.json:
        abort(400)
    actor = {
        'id': request.json['id'],
        'name': request.json['name'],
        'lastname': request.json['lastname']
    }
    actors.append(actor)
    return jsonify({'actor': actors})


@app.route('/api/movies', methods=['POST'])
def create_movie():
    if not request.json or not 'title' in request.json or not 'genre' in request.json or not 'year' in request.json:
        abort(400)
    movie = {
        'id': request.json['id'],
        'title': request.json['title'],
        'year': request.json['year'],
        'genre': request.json['genre']
    }
    movies_.append(movie)
    return jsonify({'actor': movies_})


@app.route('/api/directors', methods=['POST'])
def create_director():
    if not request.json or not 'name' in request.json:
        abort(400)
    director = {
        'id': request.json['id'],
        'name': request.json['name']
    }
    directors.append(director)
    return jsonify({'directors': directors})


######################
#PUT METHODS (UPDATE)
######################

@app.route('/api/actors/<int:id>', methods=['PUT'])
def update_actor(id):
    act = [act for act in actors if act['id'] == id]
    if len(act) == 0:
        abort(404)
    actors[0]['name'] = request.json.get('name', act[0]['name'])
    actors[0]['lastname'] = request.json.get('lastname', act[0]['lastname'])
    return jsonify({'Actor': actors[0]})

@app.route('/api/directors/<int:id>', methods=['PUT'])
def update_director(id):
    act = [act for act in directors if act['id'] == id]
    if len(act) == 0:
        abort(404)
    directors[0]['name'] = request.json.get('name', act[0]['name'])
    return jsonify({'Director modified ': directors[0]})

@app.route('/api/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    act = [act for act in movies_ if act['id'] == id]
    if len(act) == 0:
        abort(404)
    movies_[0]['title'] = request.json.get('title', act[0]['title'])
    movies_[0]['year'] = request.json.get('year', act[0]['year'])
    movies_[0]['genre'] = request.json.get('genre', act[0]['genre'])
    return jsonify({'Movie modified ': movies_[0]})


#################
#DELETE METHODS
#################

@app.route('/api/actors/<int:id>', methods=['DELETE'])
def delete_actor(id):
    actor = [actor for actor in actors if actor['id'] == id]
    if len(actor) == 0:
        abort(404)
    actors.remove(actor[0])
    return jsonify({'deleted': True})

@app.route('/api/directors/<int:id>', methods=['DELETE'])
def delete_actor(id):
    director = [director for director in directors if director['id'] == id]
    if len(director) == 0:
        abort(404)
    directors.remove(director[0])
    return jsonify({'deleted': True})

@app.route('/api/movies/<int:id>', methods=['DELETE'])
def delete_actor(id):
    movie = [movie for movie in movies_ if movie['id'] == id]
    if len(movie) == 0:
        abort(404)
    movies_.remove(movie[0])
    return jsonify({'deleted': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



if __name__ == '__main__':
    app.run()

#localhost:5000