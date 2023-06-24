import os
import yaml
# from decouple import config

class OcrConfigEnv():
    
    def __init__(self, config_data: dict):
        
        print('OcrConfigEnv is created')
        
        self.banned_keyword_list = config_data['banned_keyword_list']
        self.analysis_keyword_list = config_data['analysis_keyword_list']

class RdsConfigEnv():
    
    def __init__(self, config_data: dict):
        
        print('RdsConfigEnv is created')
        
        self.ENGINE = config_data['RDS_CONFIG']['ENGINE']
        self.HOST = config_data['RDS_CONFIG']['HOST']
        self.PORT = config_data['RDS_CONFIG']['PORT']
        self.USER = config_data['RDS_CONFIG']['USER']
        self.PASSWORD = config_data['RDS_CONFIG']['PASSWORD']
        self.DATABASE_NAME = config_data['RDS_CONFIG']['DATABASE_NAME']

class JwtConfigEnv():

    def __init__(self, config_data: dict):
        
        print('JwtConfigEnv is created')
        
        self.SECRET_KEY = config_data['JWT_CONFIG']['SECRET_KEY']
        self.ALGORITHM = config_data['JWT_CONFIG']['ALGORITHM']

class ConfigProvider():
    
    def __init__(self):
        print('ConfigProvider is created')
        
        config_data = self._load_yaml('config.yml')
        
        self.ocrConfig = OcrConfigEnv(config_data)
        self.rdsConfig = RdsConfigEnv(config_data)
        self.jwtConfing = JwtConfigEnv(config_data)
        self.api_key = config_data['api_key']    
    
    
    def _load_yaml(self, path):
        try: 
            abs_path = os.getcwd()
            
            with open(os.path.join(abs_path, path), encoding='utf-8') as stream:
                return yaml.safe_load(stream)
                
        except yaml.YAMLError as yaml_e:
            raise Exception('잘못된 형식의 YAML 입니다.')
            
        except Exception as e:
            print(e)
            raise Exception('파일을 찾지 못했습니다.')


configProvider = ConfigProvider()
        
if __name__ == "__main__":
    from sys import argv
    
    configModel = ConfigProvider()
    print(configModel.ocrConfig.banned_keyword_list)
    print(configModel.ocrConfig.analysis_keyword_list)