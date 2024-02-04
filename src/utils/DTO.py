class Player:
    def __init__(self, params):
        self.params = params
        self.id = params['id']
        self.pos_x = params['pos_x']
        self.pos_y = params['pos_y']

    def __str__(self):
        return f'{self.params}'


class World:
    def __init__(self, param):
        self.params = param
        self.id = param['id']
        self.x_dim = param['x_dim']
        self.y_dim = param['y_dim']
        self.players = param['players']

    def __str__(self):
        return f'{self.params}'
