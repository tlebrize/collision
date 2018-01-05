import tkengine, pyglet
from pyglet import gl

class Cell(object):
    def __init__(self, x, y, s):
        self.color = (200.0, 200.0, 200.0)
        self.s, self.x, self.y = s, x, y
        self.square = gl.glGenLists(1)
        self.move(0, 0)
        gl.glNewList(self.square, gl.GL_COMPILE)
        self.draw_square()
        gl.glEndList()

    def move(self, x, y):
        print('move', x, y)
        self.x += x
        self.y += y
        s, x, y = self.s, self.x, self.y
        self.points = (((s * x) + s * 10 * x - s * 5, (s * y) + s * 10 * y - s * 5),
            ((s * x) + s * 10 * x - s * 5, (s * y) + s * 10 * y + s * 5),
            ((s * x) + s * 10 * x + s * 5, (s * y) + s * 10 * y + s * 5),
            ((s * x) + s * 10 * x + s * 5, (s * y) + s * 10 * y - s * 5))
        print(dir(self.square))

    def draw_square(self):
        gl.glBegin(gl.GL_POLYGON)
        gl.glVertex2i(*self.points[0])
        gl.glVertex2i(*self.points[1])
        gl.glVertex2i(*self.points[2])
        gl.glVertex2i(*self.points[3])
        gl.glEnd()

    def draw(self):
        gl.glColor3f(*self.color)
        gl.glCallList(self.square)
        gl.glFlush()

class MainScene(tkengine.TkScene):
    def __init__(self, world):
        super().__init__(world)
        self.key_handlers.update({
            pyglet.window.key.RIGHT     : lambda : self.cell.move(1, 0),
            pyglet.window.key.LEFT      : lambda : self.cell.move(-1, 0),
            pyglet.window.key.DOWN      : lambda : self.cell.move(0, -1),
            pyglet.window.key.UP        : lambda : self.cell.move(0, 1),})
        self.cell = Cell(3,3,3)
        pyglet.clock.schedule_interval(self.draw, 1 / 60)

    def draw(self, _):
        self.world.window.clear()
        self.cell.draw()

def main():
    window = tkengine.TkWindow(caption='collision')
    world = tkengine.TkWorld(window)
    world.add_scenes({'main': MainScene(world)})
    world.run()

if __name__ == '__main__':
    main()