# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Copyright (c) 2022 by Ivan Rodriguez-Mendez.                                ~
#  :license: Apache2, see LICENSE for more details.                            ~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#----------------------------------------------------------------------------
# Created By  : Ivan Rodriguez-Mendez
# Original version by: Patrick Rainsberry
# Created Date: 11/05/2022
# version ='0.2'
# ---------------------------------------------------------------------------
""" Add-in for exporting elements in different formats (on fusion 360)""" 
# ---------------------------------------------------------------------------
# This file is a component of My360Export. 
# ---------------------------------------------------------------------------

import os
import sys
from importlib import reload

import adsk.core
import traceback

from.startup import setup_app, cleanup_app, get_app_path
setup_app(__file__)

try:
    import config
    import apper

    # Get the command functions 
    from .commands.ExportAllCommand import ExportAllCommand
    from .commands.CloseAllCommand import CloseAllCommand
    from .commands.GetCurrentDesignInfoCommand import GetCurrentDesignInfoCommand
    from .commands.ExportCurrentDesignCommand import ExportCurrentDesignCommand

    my_addin = apper.FusionApp(config.app_toolbar, config.company_name, False)
    my_addin.root_path = get_app_path(__file__)
    reload(config)

    my_addin.add_command(
        'Export Active Project',
        ExportAllCommand,
        {
            'cmd_description': 'Exports all Fusion Documents in the currently active project',
            'cmd_id': 'export_cmd_1',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': config.app_tools_name,
            'cmd_resources': 'command_icons/ExportAll',
            'command_visible': True,
            'command_promoted': True,

        }
    )

    my_addin.add_command(
        'Close All Docs',
        CloseAllCommand,
        {
            'cmd_description': 'Close All Docs',
            'cmd_id': config.close_cmd_id,
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': config.app_tools_name,
            'cmd_resources': 'command_icons/CloseAll',
            'command_visible': True,
            'command_promoted': True,

        }
    )

    my_addin.add_command(
        'Get current design info',
        GetCurrentDesignInfoCommand,
        {
            'cmd_description': 'Get current design information',
            'cmd_id': config.get_info_cmd_id,
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': config.app_tools_name,
            'cmd_resources': 'command_icons/GetCurrentDesignInfo',
            'command_visible': True,
            'command_promoted': True,

        }
    )

    my_addin.add_command(
        'Export all the elements from the current design',
        ExportCurrentDesignCommand,
        {
        'cmd_description': 'Export all the elements from the current design',
        'cmd_id': config.export_current_cmd_id,
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': config.app_tools_name,
        'cmd_resources': 'command_icons/ExportCurrentDesign',
        'command_visible': True,
        'command_promoted': True,

        }
    )

except:
    app = adsk.core.Application.get()
    ui = app.userInterface
    ui.messageBox('Initialization Failed: {}'.format(traceback.format_exc()))

debug = False

def run(context):
    my_addin.run_app()

def stop(context):
    my_addin.stop_app()
    cleanup_app(__file__)
