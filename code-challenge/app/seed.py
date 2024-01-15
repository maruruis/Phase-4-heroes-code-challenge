from app import app, db
from models import Hero, HeroPower, Power
from faker import Faker
from random import choice

fake = Faker()

with app.app_context():
    db.session.query(HeroPower).delete()
    db.session.query(Hero).delete()
    db.session.query(Power).delete()
    db.session.commit()

    print(":female_superhero: Seeding powers...")
    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    for info in powers_data:
        power = Power(**info)
        db.session.add(power)

    print(":female_superhero: Seeding heroes...")
    heroes_data = [
        {"name": fake.first_name(), "super_name": fake.first_name() + " " + fake.last_name()}
        for _ in range(20)  # Adjust the number of heroes as needed
    ]

    for info in heroes_data:
        hero = Hero(**info)
        db.session.add(hero)

    print(":female_superhero: Adding powers to heroes...")

    strengths = ["Strong", "Weak", "Average"]
    heroes = Hero.query.all()
    powers = Power.query.all()

    for hero in heroes:
        for _ in range(choice([1, 2, 3])):
            power = choice(powers)
            strength = choice(strengths)

            hero_power = HeroPower(hero=hero, power=power, strength=strength)
            db.session.add(hero_power)

    db.session.commit()
    print(":female_superhero: Done seeding!")
