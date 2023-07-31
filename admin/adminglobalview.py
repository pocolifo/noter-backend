import os
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Boolean, Integer
from starlette_admin.contrib.sqla import ModelView
from starlette.requests import Request
from starlette.responses import Response
from abc import abstractmethod

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

import redis
rdb = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], username=os.environ['REDIS_USER'], password=os.environ['REDIS_PASS'], decode_responses=True)

class Global(declarative_base()):
    __tablename__ = 'admin'

    pk = Column(Integer, primary_key=True)
    global_api_access = Column(Boolean)
    ai_endpoints = Column(Boolean, default=True)
    item_creation = Column(Boolean, default=True)
    user_creation = Column(Boolean, default=True)

class AdminGlobalView(ModelView):
    def can_create(self, request: Request) -> bool: return False
    def can_edit(self, request: Request) -> bool: return True
    def can_delete(self, request: Request) -> bool: return False
    
    def current_object(self):
        global_api_access = bool(int(rdb.get("global_api_access")))
        ai_endpoints = bool(int(rdb.get("ai_endpoints")))
        item_creation = bool(int(rdb.get("item_creation")))
        user_creation = bool(int(rdb.get("user_creation")))
        
        return Global(pk=0, global_api_access=global_api_access, ai_endpoints=ai_endpoints, item_creation=item_creation, user_creation=user_creation)
        
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
        for key, value in data.items():
            rdb.set(key, int(value))
        return self.current_object()
        
    @abstractmethod
    async def find_by_pk(self, request: Request, pk: Any) -> Any: return self.current_object() # Only 1 object to find