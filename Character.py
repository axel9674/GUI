class Character:
    def __init__(self, user, password, server, premium, mission_string, allineamento, enabled):
        self.user = user
        self.password = password
        self.server = server
        self.premium = premium
        self.mission_string = mission_string
        self.allineamento = allineamento
        self.enabled = enabled

    def __getitem__(self, param):
        return getattr(self, param)
