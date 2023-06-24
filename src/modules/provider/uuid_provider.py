from uuid import uuid4, UUID

class UuidProvider():
    
    def getIngredientUuid(self) -> UUID:
        return uuid4()
            
