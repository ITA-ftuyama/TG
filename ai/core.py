

from model import construct_model, actions

class AI(object):

    def __init__(self, kind="svm"):
        """Initializes the Controller."""
        print "Using %s classification algorithm" % kind
        self.model = construct_model(kind)

    def predict(self, data):
        """Predict some action."""
        prediction = self.model.predict(data)[0]
        proba = self.model.predict_proba(data)[0][prediction]
        return (actions[prediction], proba)
