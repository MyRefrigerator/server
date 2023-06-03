import sys
import yaml

def get_config():
    with open('./config.yml') as stream:
        try:
            yaml_data = yaml.safe_load(stream)
            return yaml_data
            
        except yaml.YAMLError as exc:
            print(exc)
            
if __name__ == "__main__":
    from sys import argv
        
    script_name = argv[0]
    print(f'\n[{script_name}] __name__ / {__name__}\n')
    
    config = get_config()
    
    print(config)       #
    print(type(config)) # <class 'dict'>