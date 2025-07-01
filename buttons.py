class Buttons:

    def __init__(self, buttons_dict=None):
        if buttons_dict is not None:
            self.dict_to_object(buttons_dict)
        else:
            self.init_buttons()

    def init_buttons(self):
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.select = False
        self.start = False
        self.Y = False
        self.B = False
        self.X = False
        self.A = False
        self.L = False
        self.R = False

    def dict_to_object(self, buttons_dict):
        # Use .get() to avoid KeyError and handle both upper and lowercase keys
        self.up = buttons_dict.get('Up', buttons_dict.get('up', False))
        self.down = buttons_dict.get('Down', buttons_dict.get('down', False))
        self.right = buttons_dict.get('Right', buttons_dict.get('right', False))
        self.left = buttons_dict.get('Left', buttons_dict.get('left', False))
        self.select = buttons_dict.get('Select', buttons_dict.get('select', False))
        self.start = buttons_dict.get('Start', buttons_dict.get('start', False))
        self.Y = buttons_dict.get('Y', buttons_dict.get('y', False))
        self.B = buttons_dict.get('B', buttons_dict.get('b', False))
        self.X = buttons_dict.get('X', buttons_dict.get('x', False))
        self.A = buttons_dict.get('A', buttons_dict.get('a', False))
        self.L = buttons_dict.get('L', buttons_dict.get('l', False))
        self.R = buttons_dict.get('R', buttons_dict.get('r', False))

    def object_to_dict(self):
        buttons_dict = {}
        buttons_dict['Up'] = self.up
        buttons_dict['Down'] = self.down
        buttons_dict['Right'] = self.right
        buttons_dict['Left'] = self.left
        buttons_dict['Select'] = self.select
        buttons_dict['Start'] = self.start
        buttons_dict['Y'] = self.Y
        buttons_dict['B'] = self.B
        buttons_dict['X'] = self.X
        buttons_dict['A'] = self.A
        buttons_dict['L'] = self.L
        buttons_dict['R'] = self.R
        return buttons_dict