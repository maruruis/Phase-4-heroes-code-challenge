#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Hero, HeroPower, Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return "Welcome to the Super Hero API!"

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [
        {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name}
        for hero in heroes
    ]
    return jsonify(heroes_data)

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero_by_id(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [
                {
                    'id': hero_power.power.id,
                    'name': hero_power.power.name,
                    'description': hero_power.power.description
                }
                for hero_power in hero.powers
            ]
        }
        return jsonify(hero_data)
    else:
        return make_response(f'Hero with id {hero_id} not found', 404)


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [
        {'id': power.id, 'name': power.name, 'description': power.description}
        for power in powers
    ]
    return jsonify(powers_data)

@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power_by_id(power_id):
    power = Power.query.get(power_id)
    if power:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        return jsonify(power_data)
    else:
        return make_response(f'Power with id {power_id} not found', 404)

from flask import jsonify, request, make_response

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power_by_id(power_id):
    power = Power.query.get(power_id)
    if power:
        power_data = request.get_json()
        
        if 'name' in power_data:
            power.name = power_data['name']

        # Validation: description must be present and at least 20 characters long
        if 'description' in power_data:
            new_description = power_data['description']

            if not new_description or len(new_description) < 20:
                return jsonify({"errors": ["Invalid description"]}), 400

            power.description = new_description

        db.session.commit()

        updated_power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }

        return jsonify(updated_power_data)
    else:
        return make_response(f'Power with id {power_id} not found', 404)

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    hero_power_data = request.get_json()
    hero_id = hero_power_data['hero_id']
    power_id = hero_power_data['power_id']
    strength = hero_power_data['strength']

    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({"errors": ["Invalid strength"]}), 400

    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    powers = [{"id": hero_power.power.id, "name": hero_power.power.name} for hero_power in hero.powers]

    created_hero_power_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }

    return jsonify(created_hero_power_data)

if __name__ == '__main__':
    app.run(port=5555)
