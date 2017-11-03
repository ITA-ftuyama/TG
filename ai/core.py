from sklearn import preprocessing
from model import constructor, actions

class AI(object):

    def __init__(self):
        """Initializes the Controller."""
        self.model, self.method, self.kind = constructor()
        print "Using %s classification algorithm with %s data" % (self.method, self.kind)

    def predict(self, data):
        """Predict some action."""
        data = preprocessing.normalize(data, norm='l2')
        prediction = self.model.predict(data)[0]
        proba = self.model.predict_proba(data)[0][prediction]
        return (actions[prediction], proba)
