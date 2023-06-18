import os
import yaml
# from decouple import config

class OcrConfigModel():
    
    def __init__(self, config_data: dict):
        
        self.banned_keyword_list = config_data['banned_keyword_list']
        self.analysis_keyword_list = config_data['analysis_keyword_list']


class ConfigProvider():
    
    def __init__(self):
        print('ConfigModel is created')
        
        config_data = self.load_yaml('/config.yml')
        
        self.ocrConfig = OcrConfigModel(config_data)
        self.api_key = config_data['api_key']
    
    def load_yaml(self, path):
        try: 
            abs_path = os.getcwd()
            with open(abs_path + path) as stream:
                return yaml.safe_load(stream)
                
        except yaml.YAMLError as yaml_e:
            raise Exception('잘못된 형식의 YAML 입니다.')
            
        except Exception as e:
            raise Exception('파일을 찾지 못했습니다.')

configProvider = ConfigProvider()
        
if __name__ == "__main__":
    from sys import argv
    
    configModel = ConfigProvider()
    print(configModel.ocrConfig.banned_keyword_list)
    print(configModel.ocrConfig.analysis_keyword_list)