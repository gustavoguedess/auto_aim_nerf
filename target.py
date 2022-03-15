
class Target:
    def __init__(self, w=0, h=0):
        self.x = 0
        self.y = 0
        self.w = w
        self.h = h
        self.center_x = w//2
        self.center_y = h//2
        self.dist_x = 0
        self.dist_y = 0
        self.found = False

    def calc(self, face):
        (x, y, w, h) = face
        x_center = x+w//2
        y_center = y+h//2
        self.x = x_center
        self.y = y_center

        self.found = True

        self.dist_x = self.x-self.center_x
        self.dist_y = self.y-self.center_y

    def lose(self):
        self.found = False

    def __str__(self):
        return f"x:{self.x} y:{self.y}, dist_x:{self.dist_x} dist_y:{self.dist_y}, found:{self.found}"