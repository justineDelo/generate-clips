class Node(object):

    def __init__(self):
        #self.params = []
        #self.regularizers = []
        #self.constraints = []
        self.children = []

    def get_params(self):
        params = []
        if self.children:
            for child in self.children:
                params += child.get_params()
        return params

    def get_regularizers(self):
        regularizers = []

    def get_constraints(self):
        constraints = []

    def connect(self, node):
        self.previous = node

    def get_input(self, train=False):
        if self.children:
            return self.children[0].get_input(train)
        else:
            raise NotImplementedError

    def get_ouput(self, train=False):
        if self.children:
            return self.children[-1].get_ouput(train)
        else:
            raise NotImplementedError

    def get_config(self):
        # recursive
        raise NotImplementedError

    def get_weights(self, weights):
        # recursive
        raise NotImplementedError

    def set_weights(self, weights):
        # recursive
        raise NotImplementedError