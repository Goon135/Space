#Задание 1

class Spaceship:
    def __init__(self, spaceship_id, name, type_, status="available"):
        self.spaceship_id = spaceship_id
        self.name = name
        self.type_ = type_
        self.status = status

    def update_status(self, new_status):
        valid_statuses = ["available", "on mission", "under repair"]
        if new_status in valid_statuses:
            self.status = new_status
        else:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
    
    def to_dict(self):
        return {
            "spaceship_id": self.spaceship_id,
            "name": self.name,
            "type": self.type_,
            "status": self.status
        }


class Mission:
    def __init__(self, mission_id, name, goal, status="planned"):
        self.mission_id = mission_id
        self.name = name
        self.goal = goal
        self.status = status
        self.spaceships = []

    def add_spaceship(self, spaceship):
        if spaceship.status == "available":
            self.spaceships.append(spaceship)
            spaceship.update_status("on mission")
        else:
            raise ValueError(f"Cannot add spaceship {spaceship.name} - status is {spaceship.status}")
    
    def update_status(self, new_status):
        valid_statuses = ["planned", "in progress", "completed"]
        if new_status in valid_statuses:
            self.status = new_status
        else:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
    
    def to_dict(self):
        return {
            "mission_id": self.mission_id,
            "name": self.name,
            "goal": self.goal,
            "status": self.status,
            "spaceships": [spaceship.to_dict() for spaceship in self.spaceships]
        }


class CrewMember:
    def __init__(self, member_id, name, role):
        self.member_id = member_id
        self.name = name
        self.role = role
    
    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "role": self.role
        }


# Проверка работы классов
if __name__ == "__main__":
    # Создание кораблей
    ship1 = Spaceship(1, "Enterprise", "research", "available")
    ship2 = Spaceship(2, "Defiant", "combat", "available")
    
    # Создание миссии
    mission1 = Mission(1, "Deep Space Exploration", "research", "planned")
    mission1.add_spaceship(ship1)
    
    # Создание членов экипажа
    captain = CrewMember(1, "James Kirk", "captain")
    engineer = CrewMember(2, "Montgomery Scott", "engineer")
    
    # Проверка работы
    print("Spaceship:", ship1.to_dict())
    print("Mission:", mission1.to_dict())
    print("Crew Member:", captain.to_dict())

#Задание 2

from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилища данных
spaceships = []
missions = []
crew_members = []

# Счетчики для генерации ID
spaceship_counter = 1
mission_counter = 1
crew_counter = 1

@app.route('/api/v1', methods=['GET'])
def home():
    return jsonify({"message": "Сервер работает!", "status": 200})

# Эндпоинты для космических кораблей
@app.route('/api/v1/spaceships', methods=['GET'])
def get_all_spaceships():
    return jsonify([ship.to_dict() for ship in spaceships])

@app.route('/api/v1/spaceships/<int:spaceship_id>', methods=['GET'])
def get_spaceship(spaceship_id):
    ship = next((s for s in spaceships if s.spaceship_id == spaceship_id), None)
    if ship:
        return jsonify(ship.to_dict())
    return jsonify({"error": "Spaceship not found"}), 404

@app.route('/api/v1/spaceships', methods=['POST'])
def create_spaceship():
    global spaceship_counter
    try:
        data = request.get_json()
        ship = Spaceship(
            spaceship_id=spaceship_counter,
            name=data['name'],
            type_=data['type'],
            status=data.get('status', 'available')
        )
        spaceships.append(ship)
        spaceship_counter += 1
        return jsonify(ship.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/v1/spaceships/<int:spaceship_id>', methods=['PUT'])
def update_spaceship_status(spaceship_id):
    try:
        data = request.get_json()
        ship = next((s for s in spaceships if s.spaceship_id == spaceship_id), None)
        if ship:
            ship.update_status(data['status'])
            return jsonify(ship.to_dict())
        return jsonify({"error": "Spaceship not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/v1/spaceships/<int:spaceship_id>', methods=['DELETE'])
def delete_spaceship(spaceship_id):
    global spaceships
    ship = next((s for s in spaceships if s.spaceship_id == spaceship_id), None)
    if ship:
        spaceships = [s for s in spaceships if s.spaceship_id != spaceship_id]
        return jsonify({"message": "Spaceship deleted successfully"})
    return jsonify({"error": "Spaceship not found"}), 404

# Эндпоинты для миссий
@app.route('/api/v1/missions', methods=['GET'])
def get_all_missions():
    return jsonify([mission.to_dict() for mission in missions])

@app.route('/api/v1/missions/<int:mission_id>', methods=['GET'])
def get_mission(mission_id):
    mission = next((m for m in missions if m.mission_id == mission_id), None)
    if mission:
        return jsonify(mission.to_dict())
    return jsonify({"error": "Mission not found"}), 404

@app.route('/api/v1/missions', methods=['POST'])
def create_mission():
    global mission_counter
    try:
        data = request.get_json()
        mission = Mission(
            mission_id=mission_counter,
            name=data['name'],
            goal=data['goal'],
            status=data.get('status', 'planned')
        )
        missions.append(mission)
        mission_counter += 1
        return jsonify(mission.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/v1/missions/<int:mission_id>/add_spaceship', methods=['POST'])
def add_spaceship_to_mission(mission_id):
    try:
        data = request.get_json()
        mission = next((m for m in missions if m.mission_id == mission_id), None)
        spaceship_id = data['spaceship_id']
        ship = next((s for s in spaceships if s.spaceship_id == spaceship_id), None)
        
        if not mission:
            return jsonify({"error": "Mission not found"}), 404
        if not ship:
            return jsonify({"error": "Spaceship not found"}), 404
        
        mission.add_spaceship(ship)
        return jsonify(mission.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Эндпоинты для членов экипажа
@app.route('/api/v1/crew', methods=['GET'])
def get_all_crew():
    return jsonify([member.to_dict() for member in crew_members])

@app.route('/api/v1/crew', methods=['POST'])
def create_crew_member():
    global crew_counter
    try:
        data = request.get_json()
        member = CrewMember(
            member_id=crew_counter,
            name=data['name'],
            role=data['role']
        )
        crew_members.append(member)
        crew_counter += 1
        return jsonify(member.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Обработчики ошибок
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad request"}), 500

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Добавим тестовые данные
    ship1 = Spaceship(1, "Enterprise", "research")
    ship2 = Spaceship(2, "Defiant", "combat")
    spaceships.extend([ship1, ship2])
    
    mission1 = Mission(1, "Deep Space Exploration", "research")
    missions.append(mission1)
    
    captain = CrewMember(1, "James Kirk", "captain")
    crew_members.append(captain)
    
    app.run(debug=True)