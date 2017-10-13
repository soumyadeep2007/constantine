# noinspection PyUnresolvedReferences,PyStatementEffect
class Replica (process):
    def setup(self):
        pass

    def __hash__(self):
        return hash((self._id))

    def __eq__(self, other):
        return self._id == other._id
