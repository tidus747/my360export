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
import re

import adsk.core
import adsk.fusion
import adsk.cam

import apper
from apper import AppObjects

import config

def save_folder_dialog(appObjects):
    # Set styles of file dialog.
    folderDlg = appObjects.ui.createFolderDialog()
    folderDlg.title = 'Fusion Choose Folder Dialog' 
    
    # Show folder dialog
    dlgResult = folderDlg.showDialog()
    if dlgResult == adsk.core.DialogResults.DialogOK:
        return folderDlg.folder
    else:
        return -1 

def get_valid_filename(filename):
    s = str(filename).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def update_name_inputs(command_inputs, selection):
    command_inputs.itemById('write_version').isVisible = False

    if selection == 'Document Name':
        command_inputs.itemById('write_version').isVisible = True

def export_components(full_export, output_folder, file_types):
    ao = AppObjects()
    app = adsk.core.Application.get()
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)

    try:
        rootComp = design.rootComponent

        if(full_export):
            occurrences = rootComp.occurrences.asList
            for i in range(0, occurrences.count):
                #TODO The export of a design needs to be better managed at several levels
                occ = occurrences.item(i)
                output_name = get_valid_filename(occ.name) # TODO It is necessary to add the possibility of writing the version of the element
                export_element(occ.component,output_folder, file_types, output_name)
        else: 

            export_element(design.rootComponent,output_folder, file_types, design.parentDocument.name)
        
        ao.ui.messageBox("The export of the elements has been completed!")
    # TODO add handling
    except ValueError as e:
        ao.ui.messageBox(str(e))

    except AttributeError as e:
        ao.ui.messageBox(str(e))

def export_element(element, folder, file_types, output_name):
    ao = AppObjects()
    export_mgr = ao.export_manager

    export_functions = [export_mgr.createIGESExportOptions,
                        export_mgr.createSTEPExportOptions,
                        export_mgr.createSATExportOptions,
                        export_mgr.createSMTExportOptions,
                        export_mgr.createFusionArchiveExportOptions,
                        export_mgr.createSTLExportOptions]
    export_extensions = ['.igs', '.step', '.sat', '.smt', '.f3d', '.stl']

    for i in range(file_types.count-2):
        if file_types.item(i).isSelected:
            dest_dir = "{}{}\\".format(folder,export_extensions[i][1:])
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            export_name = dest_dir + output_name + export_extensions[i]
            export_name = dup_check(export_name)
            export_options = export_functions[i](export_name,element)
            export_mgr.execute(export_options)

    if file_types.item(file_types.count - 2).isSelected:
        dest_dir = "{}f3d\\".format(folder)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        export_name = dest_dir + output_name + '.f3d'
        export_name = dup_check(export_name)
        export_options = export_mgr.createFusionArchiveExportOptions(export_name, element)
        export_mgr.execute(export_options)

    if file_types.item(file_types.count - 1).isSelected:
        dest_dir = "{}stl\\".format(folder)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        stl_export_name = dest_dir + output_name + '.stl'
        stl_options = export_mgr.createSTLExportOptions(element, stl_export_name)
        export_mgr.execute(stl_options)

def dup_check(name):
    if os.path.exists(name):
        base, ext = os.path.splitext(name)
        base += '-dup'
        name = base + ext
        dup_check(name)
    return name


class ExportCurrentDesignCommand(apper.Fusion360CommandBase):

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs,
                         changed_input, input_values):
        if changed_input.id == 'name_option_id':
            update_name_inputs(inputs, changed_input.selectedItem.name)

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ao = AppObjects()

        # Get input values from the dialog box
        output_folder = input_values['output_folder']
        file_types = inputs.itemById('file_types_input').listItems
        full_export = input_values['full_export']
    
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Make sure we have a folder not a file for the export
        if not output_folder.endswith(os.path.sep):
            output_folder += os.path.sep

        # Create the base folder for this output if doesn't exist (Only in the case of using the default folder) 
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        export_components(full_export, output_folder, file_types)

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        '''Create the dialog input'''
        ao = AppObjects()

        filename = save_folder_dialog(ao)
        if filename == -1:
            filename = apper.get_default_dir(config.app_name)

        inputs.addStringValueInput('output_folder', 'Output Folder:', filename)

        drop_input_list = inputs.addDropDownCommandInput('file_types_input', 'Export Types',
                                                         adsk.core.DropDownStyles.CheckBoxDropDownStyle)
        drop_input_list = drop_input_list.listItems
        drop_input_list.add('IGES', False)
        drop_input_list.add('STEP', True)
        drop_input_list.add('SAT', False)
        drop_input_list.add('SMT', False)
        drop_input_list.add('F3D', False)
        drop_input_list.add('STL', False)

        full_export_input = inputs.addBoolValueInput('full_export', 'Export all elements separately?', True, '', True)
        full_export_input.isVisible = True
