from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request

app = Flask(__name__)
tour = [
    {
        'id': 1,
        'Title': u'Samara',
        'Role': u'Young',
        'Price': 228,
        'done': True
    },
    {
        'id': 2,
        'Title': u'Bali',
        'Role': u'Old',
        'Price': 1488,
        'done': False
    }

]


@app.route('/tour', methods=['GET'])
def get_list():
    return jsonify(tour)


@app.route('/tour/<int:id>', methods=['GET'])
def get_people(people_id):
    human = list(filter(lambda t: t['id'] == people_id, tour))
    if len(human) == 0:
        abort(404)
    return jsonify({'human': human[0]})


@app.route('/tour/add', methods=['POST'])
def create_human():
    if not request.json or 'Title' not in request.json:
        abort(404)
    human = {
        'id': tour[-1]['id'] + 1,
        'Title': request.json['Title'],
        'Price': request.json['Price'],
        'Role': request.json.get('Role', get_role(request.json['Price'])),
        'done': True
    }
    tour.append(human)
    return jsonify({'human': human}), 201


@app.route('/tour/put/<int:id>', methods=['PUT'])
def update_prod(prod_id):
    task = list(filter(lambda t: t['id'] == prod_id, tour))
    if len(task) == 0:
        abort(404)
    task[0]['Title'] = request.json.get('Title', task[0]['Title'])
    return jsonify({'task': task[0]})


@app.route('/tour/delete/<int:id>', methods=['DELETE'])
def delete_tour(tour_id):
    task = list(filter(lambda t: t['id'] == tour_id, tour))
    if len(task) == 0:
        abort(404)
    tour.remove(task[0])
    return jsonify({'result': True})


@app.route('/')
def index():
    return "Hello, World!"


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'not found'}), 404)


@app.route('/tour/tour-size', methods=['GET'])
def getsize():
    return jsonify({'tour-size': len(tour)})


@app.route('/tour/oldest', methods=['GET'])
def oldest():
    max_price = 0

    nameOfOldest = ''
    for human in tour:
        if max_price < human['Price']:
            max_price = human['Price']
            nameOfOldest = human['Name']
    return jsonify({'Title of oldest human': nameOfOldest}, {'Price of oldest human': max_price})


@app.route('/tour/average', methods=['GET'])
def average():
    average_price = 0
    for human in tour:
        average_price += human['Price']
    average_price = average_price / (len(tour))
    return jsonify({'average price': average_price})


def get_role(price):
    if price <= 16:
        role = 'cheap'
    elif 16 < price <= 35:
        role = 'medium'
    else:
        role = 'expensive'
    return role


def get_cheap(price):
    cheapest_item = price[0]
    for item in price:
        if item['Price'] < cheapest_item['Price']:
            cheapest_item = item
    return cheapest_item


def get_expensive(price):
    expensive_item = price[0]
    for item in price:
        if item['Price'] > expensive_item['Price']:
            expensive_item = item
    return expensive_item


if __name__ == 'main':
    app.run(debug=True)
