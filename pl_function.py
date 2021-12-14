from pl_environment import Environment


class Function(object):
    def __init__(self, param_id, expr):
        self.env = Environment()
        self.param_id = param_id
        self.expr = expr
    
    def call(self, val):
        self.env.put(self.param_id, val)
        return self.expr.eval(self.env)