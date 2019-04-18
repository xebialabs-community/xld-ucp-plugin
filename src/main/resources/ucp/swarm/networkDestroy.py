#!/usr/bin/env python
#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
from http.http_connection import HttpConnection
from http.http_request import HttpRequest
from http.http_entity_builder import HttpEntityBuilder
from ucp.swarm.structs import generateNetwork, generateToken

import json

HTTP_SUCCESS = [200,201,202,204]

conn = HttpConnection(
    previousDeployed.container.url,
    previousDeployed.container.username,
    previousDeployed.container.password
)
req = HttpRequest(conn)

# Get Session Token
body = json.dumps(generateToken(previousDeployed))
resp = req.post(
    "/id/login",
    HttpEntityBuilder.create_string_entity(body),
    contentType='application/json'
)
if resp.getStatus() not in HTTP_SUCCESS:
    resp.errorDump()
    raise Exception(resp)
sessionToken = json.loads(resp.getResponse())['sessionToken']

# Destroy network
resp = req.delete(
    "/networks/%s" % previousDeployed.ucpId,
    contentType='application/json',
    headers={
        "Authorization": "Bearer %s" % sessionToken
    }
)
resp.errorDump()
if resp.getStatus() not in HTTP_SUCCESS:
    raise Exception(resp)

print "Removed network with ID %s" % previousDeployed.ucpId
