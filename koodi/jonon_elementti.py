class Jonon_elementti:

    # prioriteettijonon elementti

    def __init__(self, elementti, prioriteetti):
        self.__elementti = elementti
        self.__prioriteetti = prioriteetti

    @property
    def elementti(self):
        return self.__elementti

    @property
    def prioriteetti(self):
        return self.__prioriteetti
