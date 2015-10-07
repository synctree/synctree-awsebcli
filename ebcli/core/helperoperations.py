# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from cement.utils.misc import minimal_logger
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from ..core import io, fileoperations
from ..operations import commonops
from ..lib import utils, elasticbeanstalk
from ..objects.exceptions import NotInitializedError, InvalidSyntaxError, \
    NotFoundError

LOG = minimal_logger(__name__)

_marker = object()
_selected_app = None

def get_application_name(default=_marker):
    global _selected_app
    try:
        result = fileoperations.get_config_setting('global', 'application_name')
    except NotInitializedError:
        result = _get_application_name_interactive()

    if result is not None:
        _selected_app = result
        return result

    # get_config_setting should throw error if directory is not set up
    LOG.debug('Directory found, but no config or app name exists')
    if default is _marker:
        raise NotInitializedError

    _selected_app = default
    return default


def _get_application_name_interactive():
    app_list = commonops.get_application_names()
    file_name = fileoperations.get_current_directory_name()
    new_app = False
    if len(app_list) > 0:
        io.echo()
        io.echo('Select an application to use')
        try:
            default_option = app_list.index(file_name) + 1
        except ValueError:
            default_option = len(app_list)
        app_name = utils.prompt_for_item_in_list(app_list, default=default_option)

    return app_name

def get_environment_name():
    environments = [env.name for env in elasticbeanstalk.get_app_environments(_selected_app)]
    io.echo()
    io.echo('Select an environment to use')
    return utils.prompt_for_item_in_list(environments)
