

from svm import construct_svm
from svm import actions

class AI(object):

    def __init__(self, kind="SVM"):
        """Initializes the Controller."""
        self.model = construct_svm()

    def predict(self, data):
        """Predict some action."""
        prediction = self.model.predict(data)[0]
        proba = self.model.predict_proba(data)[0][prediction]
        return (actions[prediction], proba)
