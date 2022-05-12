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

import apper
from apper import AppObjects


class CloseAllCommand(apper.Fusion360CommandBase):

    def on_execute(self, command, inputs, args, input_values):
        ao = AppObjects()
        document = ao.document

        if document.isSaved:
            document.close(False)

            close_command = ao.ui.commandDefinitions.itemById(self.cmd_id)
            close_command.execute()

