import pyglet, collections, math
from pyglet import gl

class SceneNotFound(Exception):
    pass

class TkWorld(object):

    def __init__(self, window):
        self.window = window
        self.current = None
        self.scenes = {}

    def transition(self, scene):
        if self.current:
            self.current.unload(self.window)
        try:
            self.current = self.scenes[scene]
        except KeyError as k:
            raise SceneNotFound(str(k))
        self.current.load(self.window)

    def add_scenes(self, new_scenes):
        self.scenes.update(new_scenes)

    def run(self, entry='main'):
        self.transition(entry)
        pyglet.app.run()


class TkWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(TkWindow, self).__init__(*args, **kwargs)
        self.set_visible(False)
        self.center()
        self.clear()
        self.flip()
        self.clear()
        self.set_visible(True)

    def center(self):
        self.set_location(self.screen.width // 2 - self.width // 2,
                        self.screen.height // 2 - self.height // 2)


class TkScene(object):

    WINDOW_EVENTS = ["on_draw", "on_mouse_press", "on_mouse_release", "on_mouse_drag", "on_key_press"]

    def __init__(self, world):
        self.world = world
        self.keys = pyglet.window.key.KeyStateHandler()
        self.world.window.push_handlers(self.keys)
        self.key_handlers = {
            pyglet.window.key.ESCAPE: pyglet.app.exit,
        }

    def on_key_press(self, button, modifiers):
        self.key_handlers.get(button, lambda : None)()

    def load(self, window):
        for event in TkScene.WINDOW_EVENTS:
            if hasattr(self, event):
                window.__setattr__(event, self.__getattribute__(event))
        if hasattr(self, "entry"):
            self.entry()

    def unload(self, window):
        for event in TkScene.WINDOW_EVENTS:
            if hasattr(self, event):
                window.__setattr__(event, lambda *args: False)
        if hasattr(self, "exit"):
            self.exit()

