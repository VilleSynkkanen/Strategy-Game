class Jonon_elementti:

    # prioriteettijonon elementti

    def __init__(self, elementti, prioriteetti):
        self._elementti = elementti
        self._prioriteetti = prioriteetti

    @property
    def elementti(self):
        return self._elementti

    @property
    def prioriteetti(self):
        return self._prioriteetti
