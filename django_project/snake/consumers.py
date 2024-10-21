import json
import random
from channels.generic.websocket import WebsocketConsumer
from threading import Timer

grid_size = 20
canvas_size = 800 // grid_size


class SnakeGameConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.snake1 = []
        self.snake2 = []
        self.direction1 = {'x': 1, 'y': 0}
        self.direction2 = {'x': -1, 'y': 0}
        self.food = {}
        self.game_interval = None

    def connect(self):
        print('hit')
        self.accept()
        self.start_game()

    def disconnect(self, close_code):
        if self.game_interval:
            self.game_interval.cancel()

    def receive(self, text_data):
        data = json.loads(text_data)
        
        if data['type'] == 'move':
            if data['player'] == 1:
                self.direction1 = data['direction']
            elif data['player'] == 2:
                self.direction2 = data['direction']
        
        elif data['type'] == 'restart':
            self.start_game()

    def start_game(self):
        self.snake1 = [{'x': 3, 'y': 3}]
        self.snake2 = [{'x': 16, 'y': 16}]
        self.direction1 = {'x': 1, 'y': 0}
        self.direction2 = {'x': -1, 'y': 0}

        self.food = {
            'x': random.randint(0, canvas_size - 1),
            'y': random.randint(0, canvas_size - 1)
        }

        # Запускаем игровой процесс с интервалом
        self.game_interval = Timer(0.1, self.update_game)
        self.game_interval.start()

    def update_game(self):
        self.move_snake(self.snake1, self.direction1)
        self.move_snake(self.snake2, self.direction2)

        # Проверка на столкновения и условия конца игры
        if self.check_collision(self.snake1) or self.check_collision(self.snake2):
            self.send_game_over('Game Over: One or both snakes collided!')
            return

        if self.check_head_collision(self.snake1, self.snake2):
            self.send_game_over('Game Over: The snakes collided heads!')
            return

        self.check_food_collision(self.snake1)
        self.check_food_collision(self.snake2)

        # Отправляем обновленные данные клиенту
        self.send_game_data()

        # Запускаем следующий цикл игры
        self.game_interval = Timer(0.1, self.update_game)
        self.game_interval.start()

    def send_game_data(self):
        data = {
            'type': 'game-data',
            'snake1': self.snake1,
            'snake2': self.snake2,
            'food': self.food
        }
        self.send(text_data=json.dumps(data))

    def send_game_over(self, message):
        if self.game_interval:
            self.game_interval.cancel()
        self.send(text_data=json.dumps({'type': 'game-over', 'message': message}))

    def move_snake(self, snake, direction):
        new_head = {'x': snake[0]['x'] + direction['x'], 'y': snake[0]['y'] + direction['y']}

        # Проверка на границы поля
        if (new_head['x'] < 0 or new_head['x'] >= canvas_size or
                new_head['y'] < 0 or new_head['y'] >= canvas_size):
            self.send_game_over('Game Over: Snake hit the wall!')
            return

        snake.insert(0, new_head)
        snake.pop()

    def check_collision(self, snake):
        for i in range(1, len(snake)):
            if snake[i]['x'] == snake[0]['x'] and snake[i]['y'] == snake[0]['y']:
                return True
        return False

    def check_head_collision(self, snake1, snake2):
        return snake1[0]['x'] == snake2[0]['x'] and snake1[0]['y'] == snake2[0]['y']

    def check_food_collision(self, snake):
        if snake[0]['x'] == self.food['x'] and snake[0]['y'] == self.food['y']:
            snake.append({'x': snake[-1]['x'], 'y': snake[-1]['y']})
            self.generate_food()

    def generate_food(self):
        self.food = {
            'x': random.randint(0, canvas_size - 1),
            'y': random.randint(0, canvas_size - 1)
        }
