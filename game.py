import math
import pyglet
import random

window = pyglet.window.Window()

objects = []
pressed_keys = set()
ACCELERATION = 20  # pixels per second^2
ROTATION_SPEED = 5  # degrees per second
MAX_ASTEROID_SPEED = 150  # pixels per second
MAX_ASTEROID_ROT_SPEED = 3  # rads per second

class SpaceObject:
    def __init__(self):
        objects.append(self)
        self.x = window.width // 2
        self.y = window.height // 2
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = 0
        image = self.get_image()
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        self.sprite = pyglet.sprite.Sprite(image)

    def get_image(self):
        raise NotImplementedError('you must implement this on child')

    def update_position(self, t):
        self.x += t * self.x_speed
        self.y += t * self.y_speed
        self.x %= window.width
        self.y %= window.height

    def update_sprite(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = 90 - math.degrees(self.rotation)
       
    def tick(self, t):
        self.update_position(t)
        self.update_sprite()

class SpaceShip(SpaceObject):
    def handle_keys(self, t):
        if pyglet.window.key.UP in pressed_keys:
            self.x_speed += t * ACCELERATION * math.cos(self.rotation)
            self.y_speed += t * ACCELERATION * math.sin(self.rotation)            
                    
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation += ROTATION_SPEED * t
                    
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation -= ROTATION_SPEED * t

    def get_image(self):
        return pyglet.image.load('spaceship.png')

    def tick(self, t):
        self.handle_keys(t) 
        super().tick(t)


class Asteroid(SpaceObject):
    def __init__(self):
        super().__init__()
        if random.randint(0, 1) == 0:
            self.x = 0
            self.y = window.height // 2
        else:
            self.x = window.width // 2
            self.y = 0
        self.x_speed = random.randint(-MAX_ASTEROID_SPEED,
                                      MAX_ASTEROID_SPEED)
        self.y_speed = random.randint(-MAX_ASTEROID_SPEED,
                                       MAX_ASTEROID_SPEED)
        self.rotation_speed = random.randint(-MAX_ASTEROID_ROT_SPEED,
                                             MAX_ASTEROID_ROT_SPEED)

    def tick(self, t):
        self.rotation += t * self.rotation_speed
        super().tick(t)

    def get_image(self):
        size = random.choice(['big', 'med', 'small'])
        num = random.randint(1, 2)
        return pyglet.image.load(
            'asteroid_{}{}.png'.format(size, num))




spaceship = SpaceShip()
for _ in range(5):
    Asteroid()

def on_draw():
    window.clear()
    for obj in objects:
        obj.sprite.draw()

def tick(t):
    for obj in objects:
        obj.tick(t)

def on_key_press(sym, mod):
    pressed_keys.add(sym)

def on_key_release(sym, mod):
    pressed_keys.discard(sym)

window.push_handlers(
    on_draw=on_draw,
    on_key_press=on_key_press,
    on_key_release=on_key_release,
)

pyglet.clock.schedule_interval(tick, 1/30)

pyglet.app.run()
