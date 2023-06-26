import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta

# Module
from src.modules.provider.config_provider import configProvider

MINUTE = 60

class JwtProvider():
    
    def __init__(self):
        jwtConfig = configProvider.jwtConfing
        self.SECRET_KEY = jwtConfig.SECRET_KEY
        self.ALGORITHM = jwtConfig.ALGORITHM
    
    def encode(self, payload: dict):
        
        return jwt.encode({
          **payload,
          'exp': datetime.utcnow() + timedelta(seconds = 30 * MINUTE)
        },
            self.SECRET_KEY,
            self.ALGORITHM
        )
        
    def verify(self, token: str):
        
        try:
            
            
            result = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM],
                options={'verify_exp': True}
            )
            
            return result
        
        except ExpiredSignatureError as e:
            raise 'ExpiredSignatureError'
        
        except InvalidTokenError as e:
            raise 'InvalidTokenError'
        
        except Exception as e:
            pass
        
if __name__ == '__main__':
    
    payload = {'a': 'b'}
    
    jwtProvider = JwtProvider()
    token = jwtProvider.encode(payload)
    print(InvalidTokenError)
    
    # # from time import sleep
    
    # # token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhIjoiYiJ9.xbT0UUDjFmX0hhOG-boWIzHyfqvKsYraqJj5A86-zCQ'
    
    # # sleep(6)
    payload = jwtProvider.verify(token)
    print(payload)
    print(type(payload))