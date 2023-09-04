from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

class Block(BaseModel):
    type: str
    data: dict

def is_valid_blocks(blocks):
    for block in blocks:
        try:
            block_info = Block(**block)
        except ValidationError:
            return False
        
    return True