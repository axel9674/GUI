class Character:
    def __init__(self, username, password, server, premium, mission_string, allineamento, enabled):
        self.user = username
        self.password = password
        self. server = server
        self.premium = premium
        self.missionString = mission_string
        self.allineamento = allineamento
        self.enabled = enabled

    def __getitem__(self, param):
        return getattr(self, param)
