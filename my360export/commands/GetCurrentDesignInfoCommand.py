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

import adsk.core
import adsk.fusion
import adsk.cam

import apper
from apper import AppObjects

import config

# Performs a recursive traversal of an entire assembly structure.
def traverseAssembly(occurrences, currentLevel, inputString):
    for i in range(0, occurrences.count):
        occ = occurrences.item(i)
        inputString += spaces(currentLevel * 5) + "[{}] - ".format(currentLevel) + occ.name + '\n'
        
        if occ.childOccurrences:
            inputString = traverseAssembly(occ.childOccurrences, currentLevel + 1, inputString)
    return inputString

# Returns a string containing the especified number of spaces.
def spaces(spaceCount):
    result = ''
    for i in range(0, spaceCount):
        result += ' '

    return result

class GetCurrentDesignInfoCommand(apper.Fusion360CommandBase):

    def on_execute(self, command, inputs, args, input_values):
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('No active Fusion design', 'No Design')
            return

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Write the first line
        resultString = "-"*80 + "\n"
        
        # Create the title for the output.
        resultString += 'Root ({}) - Number of components: {}\n'.format(design.parentDocument.name,rootComp.occurrences.asList.count)
        
        # Call the recursive function to traverse the assembly and build the output string.
        resultString = traverseAssembly(rootComp.occurrences.asList, 1, resultString)

        # Display the result.
        # Write the results to the TEXT COMMANDS window.
        textPalette = ui.palettes.itemById('TextCommands')
        if not textPalette.isVisible:
            textPalette.isVisible = True

        resultString += "-"*80 + "\n"
        textPalette.writeText(resultString)
