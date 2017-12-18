import math
import pyglet
from pyglet.window import key

# Consts
ACCELERATION = 20 # pixels per sec per sec
ROTATION_SPEED = 4  # radians per sec

# Global state:
objects = []  # we'll store all game objects here
pressed_keys = set()  # currently pressed keys, a set
batch = pyglet.graphics.Batch()  # we'll put all sprites here

# Classes:
class SpaceObject:
    """
    This class represents any space object

    Attributes:

     * x, y: position in the window
     * x_spped, y_speed: speed in x/y direction
     * rotation: rotation of the object in radians, 0 means facing north
    """
    def __init__(self):
        # set some initial values:
        self.x = 200
        self.y = 400
        self.rotation = 0
        self.x_speed = 0
        self.y_speed = 0

        # assign and position the sprite with image
        image = pyglet.image.load(self.image_path())
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        self.sprite = pyglet.sprite.Sprite(image, batch=batch)
        self.update_sprite()

        # register the ship to the global list of game objects
        objects.append(self)

    def update_sprite(self):
        """
        Take the attributes of the ship and apply them to it's sprite.
        Do some conversion if needed.
        """
        self.sprite.x = self.x
        self.sprite.y = self.y
        # we have rotation in rads, pyglet uses degrees
        # also, pyglet's zero is up, ours is on the right, right?
        self.sprite.rotation = 90 - math.degrees(self.rotation)

    def tick(self, dt):
        """
        A certain time period (dt) in seconds have passed, so let's move the
        ship according to its speed and the keys the user is holding
        """
        # apply SPEED * TIME = DISTANCE
        self.x += dt * self.x_speed
        self.y += dt * self.y_speed

        # infinite space - wraparound coordinates
        self.x %= window.width
        self.y %= window.height

        # finally, apply the changes to the sprite
        self.update_sprite()


class SpaceShip(SpaceObject):
    def image_path(self):
        return 'spaceship.png'

    def tick(self, dt):
        rotation_speed = 0  # no keys pressed, no rotation
        acceleration = 0
        if key.LEFT in pressed_keys:
            rotation_speed += ROTATION_SPEED
        if key.RIGHT in pressed_keys:
            rotation_speed -= ROTATION_SPEED
        if key.UP in pressed_keys:
            acceleration = ACCELERATION

        # Accelerate when key.UP is pressed
        self.x_speed += dt * acceleration * math.cos(self.rotation)
        self.y_speed += dt * acceleration * math.sin(self.rotation)

        self.rotation += rotation_speed * dt

        super().tick(dt)


# Create new spaceship, it registers itself to the global list
spaceship = SpaceShip()


# Pyglet objects and functions

# main window
window = pyglet.window.Window()


def draw_all_objects():
    """For all objects, draw theirs sprites"""
    window.clear()
    batch.draw()

def tick_all_objects(dt):
    """For all objects, tick them"""
    for obj in objects:
        obj.tick(dt)


def key_pressed(sym, mod):
    """Save the pressed keys to our global set"""
    pressed_keys.add(sym)


def key_released(sym, mod):
    """Remove the released keys from our global set"""
    pressed_keys.discard(sym)


# register our function as handlers:
window.push_handlers(
    on_draw=draw_all_objects,
    on_key_press=key_pressed,
    on_key_release=key_released,
)

# schedule our ticking function to happen often:
pyglet.clock.schedule_interval(tick_all_objects, 1/30)

# finally, run the game:
pyglet.app.run()
