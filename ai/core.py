

from svm import construct_model
from svm import actions

class AI(object):

    def __init__(self, kind="svm"):
        """Initializes the Controller."""
        self.model = construct_model(kind)

    def predict(self, data):
        """Predict some action."""
        prediction = self.model.predict(data)[0]
        proba = self.model.predict_proba(data)[0][prediction]
        return (actions[prediction], proba)
