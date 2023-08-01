from datetime import datetime
import hashlib
import os
import httpx
from starlette_admin.contrib.sqla import ModelView
from starlette.requests import Request
from abc import abstractmethod


AUTHORIZATION_STRING = os.getenv('AUTHORIZATION_STRING', 'secret')

from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

class AdminGlobalView(ModelView):
    def can_create(self, request: Request) -> bool: return False
    def can_edit(self, request: Request) -> bool: return True
    def can_delete(self, request: Request) -> bool: return False
    
    def current_object(self):
        response = httpx.get(f"{os.environ['META_SERVER_URL']}/access-flags")
        return response.json()
        
    @abstractmethod
    async def find_all(
        self,
        request: Request,
        skip: int = 0,
        limit: int = 100,
        where: Union[Dict[str, Any], str, None] = None,
        order_by: Optional[List[str]] = None,
    ) -> Sequence[Any]:
        
        seq: Sequence[bool] = [self.current_object()]
        return seq
        
    @abstractmethod
    async def count(
        self,
        request: Request,
        where: Union[Dict[str, Any], str, None] = None,
    ) -> int:
        return 1 # Never more than 1 one instance of globals
        
        
    @abstractmethod
    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        obj = self.current_object()

        for key, value in data.items():
            obj[key] = bool(value)

        # Key algorithm as specified in the meta project
        now = datetime.now()
        salt = hashlib.sha512(f'{now.year}{now.month}{now.day}{now.hour}{now.minute}').hexdigest()
        expected_string = f'{AUTHORIZATION_STRING}{salt}'

        httpx.put(f"{os.environ['META_SERVER_URL']}/access-flags", json=obj, headers={
            'Authorization': expected_string
        })

        return obj
        
    @abstractmethod
    async def find_by_pk(self, request: Request, pk: Any) -> Any:
        return self.current_object() # Only 1 object to find