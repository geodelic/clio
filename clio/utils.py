#
#   Copyright 2013 Geodelic
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License. 
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#

import json
from bson import json_util, BSON

from flask.wrappers import Request, cached_property

def getBoolean(string):
    if string is None:
        return False
    return {
        '1': True, 'yes': True, 'true': True, 'on': True,
        '0': False, 'no': False, 'false': False, 'off': False, '': False, None: False
    }[string.lower()]


class ExtRequest(Request):
    @cached_property
    def json(self):
        """If the mimetype is `application/json` this will contain the
        parsed JSON data.
        """
        if self.mimetype == 'application/bson':
            return BSON(self.data).decode()

        if self.mimetype in ('application/json','application/extjson'):
            if 'ext' in self.mimetype:
                objhook = json_util.object_hook
            else:
                objhook = None

            request_charset = self.mimetype_params.get('charset')
            if request_charset is not None:
                j = json.loads(self.data, encoding=request_charset, object_hook=objhook )
            else:
                j = json.loads(self.data, object_hook=objhook)

            return j


