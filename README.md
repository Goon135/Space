# Space
Космический флот


# Примеры тестирования API

Создание нового корабля (curl):

curl -X POST http://127.0.0.1:5000/api/v1/spaceships \
-H "Content-Type: application/json" \
-d '{
    "name": "Voyager",
    "type": "research",
    "status": "available"
}'

Получение всех кораблей:

curl -X GET http://127.0.0.1:5000/api/v1/spaceships

Создание миссии:

curl -X POST http://127.0.0.1:5000/api/v1/missions \
-H "Content-Type: application/json" \
-d '{
    "name": "Border Patrol",
    "goal": "combat",
    "status": "planned"
}'

Добавление корабля к миссии:

curl -X POST http://127.0.0.1:5000/api/v1/missions/1/add_spaceship \
-H "Content-Type: application/json" \
-d '{
    "spaceship_id": 2
}'
