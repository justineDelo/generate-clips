
class DefaultLogger():

    def __init__(verbose=1):
        self.verbose = verbose
        self.values = {}

    def update(current, total, values=[]):
        for n, v in values:
            if n not in self.values:
                self.values[n] = []
            self.values[n].append(v)

        if verbose == 1:
            if not hasattr(self, 'progbar'):
                self.progbar = Progbar(target=total)
            progbar.update(current, values)

        if verbose == 2:
            if current == total:
                print(' - '.join(["%s: %.4f" % (n, np.mean(self.values[n])) for n, _ in values]))
