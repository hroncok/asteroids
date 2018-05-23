import math
import pyglet

window = pyglet.window.Window()

objects = []
pressed_keys = set()
ACCELERATION = 20  # pixels per second^2
ROTATION_SPEED = 5  # degrees per second

class SpaceShip:
    def __init__(self):
        objects.append(self)
        self.x = window.width // 2
        self.y = window.height // 2
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = 0
        image = pyglet.image.load('spaceship.png')
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        self.sprite = pyglet.sprite.Sprite(image)

    def handle_keys(self, t):
        if pyglet.window.key.UP in pressed_keys:
            self.x_speed += t * ACCELERATION * math.cos(self.rotation)
            self.y_speed += t * ACCELERATION * math.sin(self.rotation)            
                    
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation += ROTATION_SPEED * t
                    
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation -= ROTATION_SPEED * t

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
        self.handle_keys(t)            
        self.update_position(t)
        self.update_sprite()

spaceship = SpaceShip()

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
