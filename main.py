from flask import Flask, request, jsonify
import mysql.connector

# MySQL credentials

username = 'api'
password = 'pass'
host = 'localhost'
database = 'papadb'

# Connection

cnx = mysql.connector.connect(
    user=username,
    password=password,
    host=host,
    database=database,
    collation='utf8mb4_unicode_ci'
)
cursor = cnx.cursor()

app = Flask(__name__)
minidb = {}

def auth(success):
    headers = request.headers
    apikey = headers.get('key')
    print(apikey)
    if apikey == open('token.env').read().strip():
        return success
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

def remove_card_data(i):
    chosen = get_card_data(i)
    sql = "DELETE FROM Cards WHERE id=%s"
    cursor.execute(sql, (i,))
    return chosen

def add_card_data(data):
    sql = "INSERT INTO Cards (name, description, email, url) VALUES (%s, %s, %s, %s)"
    values = unclean_data(data)
    cursor.execute(sql, values)
    cnx.commit()
    return cursor.lastrowid
    
def get_cards_data():
    query = "SELECT * FROM Cards"
    cursor.execute(query)
    items = cursor.fetchall()
    return [cleanup_data(item) for item in items]
def get_card_data(i):
    query = "SELECT * FROM Cards WHERE id = %s"
    cursor.execute(query, (i,))

    result = cursor.fetchone()
    return cleanup_data(result) if result else {}

def unclean_data(data):
    result = ['', '', '', '']
    result[0] = data["name"]
    result[1] = data["description"]
    result[2] = data["email"]
    result[3] = data["url"]
    return tuple(result)

def cleanup_data(result):
    return {
        "id": result[0],
        "name": result[1],
        "description": result[2],
        "email": result[3],
        "url": result[4]
        }

@app.route("/remove-card/<card_id>", methods=["DELETE"])
def remove_card(card_id):
    return auth((jsonify(remove_card_data(card_id)), 200))


@app.route("/get-card/<card_id>", methods=["GET"])
def get_card(card_id):
    return jsonify(get_card_data(card_id)), 200


@app.route("/get-cards", methods=["GET"])
def get_cards():
    return jsonify(get_cards_data()), 200

@app.route("/add-card", methods=["POST"])
def add_card():
    data = request.get_json()
    cardid = add_card_data(data)
    return auth((get_card(cardid)[0], 201))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
