class Antena:
    def __init__(self, centro_poblado, latitud, longitud, tecnologias):
        self.centro_poblado = centro_poblado
        self.latitud = latitud
        self.longitud = longitud
        self.tecnologias = tecnologias

    def __repr__(self):
        return f"Antena({self.centro_poblado}, {self.latitud}, {self.longitud}, {self.tecnologias})"