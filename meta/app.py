"""
Ultra high performance, secure metadata server

Performance highlights
- Completely asynchronous IO
- Uses Starlette framework
- File pointers are always open

Security highlights
- Secure authorization comparison
- PUT method masking
- Frequently changing authorization password
- Pydantic validation
"""

import hashlib
from http import HTTPStatus
import json
import os
import secrets
from datetime import datetime

import aiofiles
from aiofiles.threadpool.text import AsyncTextIOWrapper
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response

#############
# VARIABLES #
#############
ACCESS_FLAGS_SAVE_FILE = os.getenv('ACCESS_FLAGS_SAVE_FILE', 'access-flags.json')
access_flags_reader: AsyncTextIOWrapper = None
access_flags_writer: AsyncTextIOWrapper = None

AUTHORIZATION_STRING = os.getenv('AUTHORIZATION_STRING', 'secret')

#################################
# ACCESS FLAGS MODEL DEFINITION #
#################################
class AccessFlags(BaseModel):
    api_enabled: bool = True
    ai_endpoints_enabled: bool = True
    user_creation_endabled: bool = True
    item_creation_enabled: bool = True


#########################
# ACCESS STATE ENDPOINT #
#########################
async def access_flags(request: Request):
    # This function is built for fault-tolerancy and prioritizes for the default state of AccessFlags (all features enabled)
    # It will always make sure that the file is not corrupted, and if it is, it will default to AccessFlags defaults
    try:
        state = AccessFlags.validate(json.loads(await access_flags_reader.read()))
    except:
        state = AccessFlags()

    # Allow authenticated requests to change the AccessFlags
    # Must be PUT request
    if request.method == 'PUT':
        # Introduce a moving part to the Authorization header
        # -> Prevents the authorization header that worked one time from working always
        now = datetime.now()
        salt = hashlib.sha512(f'{now.year}{now.month}{now.day}{now.hour}{now.minute}').hexdigest()
        expected_string = f'{AUTHORIZATION_STRING}{salt}'

        # Authorization header must be correct
        # secrets.compare_digest is the secure, cryptographically safe way to compare strings
        if (authorization := request.headers.get('Authorization', '')) and secrets.compare_digest(authorization, expected_string):
            try:
                # Get the body of the request, validate it, and that is the new AccessState
                state = AccessFlags.validate(json.loads(await request.body()))
                
                # Save the new state
                await access_flags_writer.write(state.json())
                await access_flags_writer.flush()
            except:
                return Response(status_code=HTTPStatus.BAD_REQUEST)
        else:
            # Even though the method is allowed, this will help to hide the capability to set the AccessState over HTTP
            return Response(status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    
    # Return the AccessState as a JSON response
    return Response(
        content=state.json(),
        media_type='application/json',
        status_code=HTTPStatus.OK
    )

#############
# LIFECYCLE #
#############
async def open_files():
    global access_flags_reader, access_flags_writer

    need_to_initialize_file = not os.path.exists(ACCESS_FLAGS_SAVE_FILE)  # check before opening a writer and the file is created
    access_flags_writer = await aiofiles.open(ACCESS_FLAGS_SAVE_FILE, 'wt')  # open an async file writer

    # Write the default AccessState to the file if it needs to be initialized
    if need_to_initialize_file:
        await access_flags_writer.write(AccessFlags().json())
        await access_flags_writer.flush()

    access_flags_reader = await aiofiles.open(ACCESS_FLAGS_SAVE_FILE, 'rt')  # open an async file reader

async def close_files():
    await access_flags_reader.close()
    await access_flags_writer.close()

###########
# THE APP #
###########
app = Starlette(
    routes=[
        Route('/access-flags', access_flags, methods=['GET', 'PUT'])
    ],
    on_shutdown=[
        close_files
    ],
    on_startup=[
        open_files
    ]
)