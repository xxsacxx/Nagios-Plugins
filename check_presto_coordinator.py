#!/usr/bin/env python
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2017-09-22 15:45:06 +0200 (Fri, 22 Sep 2017)
#
#  https://github.com/harisekhon/nagios-plugins
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn
#  and optionally send me feedback to help steer this or other code I publish
#
#  https://www.linkedin.com/in/harisekhon
#

"""

Nagios Plugin to check a Presto SQL node is configured as a coordinator

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import traceback
srcdir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.join(srcdir, 'pylib')
sys.path.append(libdir)
try:
    # pylint: disable=wrong-import-position
    from harisekhon.utils import UnknownError, support_msg_api
    from harisekhon import RestNagiosPlugin
except ImportError as _:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.1'


# pylint: disable=too-few-public-methods
class CheckPrestoCoordinator(RestNagiosPlugin):

    def __init__(self):
        # Python 2.x
        super(CheckPrestoCoordinator, self).__init__()
        # Python 3.x
        # super().__init__()
        self.name = 'Presto'
        self.default_port = 8080
        self.auth = False
        self.json = True
        self.path = '/v1/service/presto/general'
        self.msg = 'Presto SQL node coordinator = '

    def parse_json(self, json_data):
        presto_service = None
        for service in json_data['services']:
            if service['type'] == 'presto':
                presto_service = service
        if not presto_service:
            raise UnknownError('presto service not found in list of services. {0}'.format(support_msg_api()))
        is_coordinator = presto_service['properties']['coordinator']
        self.msg += "'{0}'".format(is_coordinator)
        if is_coordinator != 'true':
            self.critical()


if __name__ == '__main__':
    CheckPrestoCoordinator().main()
