"""
Ultra high performance, secure metadata server

Performance highlights
- Completely asynchronous IO
- Uses Starlette framework

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

from pydantic import BaseModel

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

#############
# VARIABLES #
#############
ACCESS_FLAGS_SAVE_FILE = os.getenv('ACCESS_FLAGS_SAVE_FILE', 'access-flags.json')
AUTHORIZATION_SECRET = os.getenv('AUTHORIZATION_SECRET', 'secret')

###########
# THE APP #
###########
app = Starlette()

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
@app.route(
        path='/access-flags',
        methods=['GET', 'PUT'],
        include_in_schema=False
)
async def access_flags(request: Request):
    # Allow authenticated requests to change the AccessFlags
    # Must be PUT request
    if request.method == 'PUT':
        # Introduce a moving part to the Authorization header
        # -> Prevents the authorization header that worked one time from working always
        now = datetime.now()
        salt = hashlib.sha512(f'{now.year}{now.month}{now.day}{now.hour}{now.minute}'.encode('utf-8')).hexdigest()
        expected_string = f'{AUTHORIZATION_SECRET}{salt}'

        # Authorization header must be correct
        # secrets.compare_digest is the secure, cryptographically safe way to compare strings
        if (authorization := request.headers.get('Authorization', '')) and secrets.compare_digest(authorization, expected_string):
            try:
                # Get the body of the request, validate it, and that is the new AccessState
                request.app.state.access_flags = AccessFlags.validate(json.loads(await request.body()))
                
                # Save the new state
            except:
                return Response(status_code=HTTPStatus.BAD_REQUEST)
        else:
            # Even though the method is allowed, this will help to hide the capability to set the AccessState over HTTP
            return Response(status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    
    # Return the AccessState as a JSON response
    return Response(
        content=request.app.state.access_flags.json(),
        media_type='application/json',
        status_code=HTTPStatus.OK
    )

#############
# LIFECYCLE #
#############
@app.on_event('startup')
def load_access_flags():
    try:
        app.state.access_flags = AccessFlags.parse_file(ACCESS_FLAGS_SAVE_FILE)
    except:
        app.state.access_flags = AccessFlags()
    

@app.on_event('shutdown')
def save_access_flags():
    with open(ACCESS_FLAGS_SAVE_FILE, 'wt') as fp:
        fp.write(app.state.access_flags.json())
