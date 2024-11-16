class Antena:
    def __init__(self, centro_poblado, latitud, longitud, tecnologias):
        self.centro_poblado = centro_poblado
        self.latitud = latitud
        self.longitud = longitud
        self.tecnologias = tecnologias

    def __repr__(self):
        return f"Antena:\n {self.centro_poblado},\n {self.latitud},\n {self.longitud},\n {self.tecnologias}"