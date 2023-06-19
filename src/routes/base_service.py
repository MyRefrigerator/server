from src.modules.provider.rds_provider import RdsProvider

class BaseService():
    
    def __init__(self):
        self.rdsProvider = RdsProvider()