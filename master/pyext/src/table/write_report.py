###################################
# Script to write PDB-DEV Validation into a PDF
#
#
# ganesans - Salilab - UCSF
# ganesans@salilab.org
###################################

import pandas as pd
import glob
import os
import sys
import numpy as np
from datetime import datetime 
from datetime import timedelta
import pytz
import pdfkit
import wkhtmltopdf

config = pdfkit.configuration(wkhtmltopdf='/home/ganesans/PDB-dev/master/pyext/wkhtmltox/bin/wkhtmltopdf')

sys.path.append('/home/ganesans/PDB-dev/master/pyext/src/table')
from create_report import *
################################################
# Define variables
################################################
mmcif_file = sys.argv[1]
name=mmcif_file.split('.')[0].split('_')[0]
d=datetime.now();t=pytz.timezone("America/Los_Angeles");d1=t.localize(d)
timestamp=d1.strftime("%B %d, %Y --  %I:%M %p")

################################################
# Edit dictionaries
# Entries is dictionaries can be edited to add
# other custom information
################################################
I = get_input_information(mmcif_file)
I.get_databases()
#ID=I.get_id().split('_')[0]+' ' +I.get_id().split('_')[1]
I.get_struc_title()
Input_info=I.get_entry_composition()
print (I.get_number_of_molecules())
################################################
# Convert ordered dictionaries 
# into lists
################################################
#Input_info_dict=dict_to_list(Input_info)
Input_info_dict=[['Id', ['1', '1']]]
print (Input_info_dict)

################################################
# Compile all information
# 
################################################
variable_dict = {'date':timestamp,
                 'ID':I.get_id(),
                 'Molecule': I.get_struc_title(),
                 'title':I.get_title(),
                 'authors':I.get_authors(),
                 'input_information':Input_info_dict,
                 'number_of_molecules':I.get_number_of_molecules(),
                 'number_of_atoms': 22}

################################################
# Generate tex, pdf file
################################################
template = utils.get_template('/home/ganesans/PDB-dev/master/pyext/src/table/template.tex')
utils.compile_pdf_from_template(template, variable_dict, './ValidationReport_'+sys.argv[1]+'.pdf')

exit()
