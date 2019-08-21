###################################
# Script to run validation and write
# to HTML and PDF 
# ganesans - Salilab - UCSF
# ganesans@salilab.org
###################################
import pytz
import jinja2
import sys

import pandas as pd
import glob
import sys,os
import numpy as np
from create_report import *
import pdfkit
import datetime
#############################
# Features to add:
# 1) Flask and server support
#############################

config = pdfkit.configuration(wkhtmltopdf='/home/ganesans/PDB-dev/master/pyext/wkhtmltox/bin/wkhtmltopdf')
options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
}
sys.path.append('/home/ganesans/PDB-dev/master/pyext/src/table')
sys.path.append('/home/ganesans/PDB-dev/master/pyext/src/table/images')
d=datetime.datetime.now();t=pytz.timezone("America/Los_Angeles");d1=t.localize(d)
timestamp=d1.strftime("%B %d, %Y --  %I:%M %p")

# Create directory
dirName = 'Output'
try:
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

################################################
# Define variables
################################################

mmcif_file = sys.argv[1]
name=mmcif_file.split('.')[0].split('_')[0]


################################################
# Get information
################################################

I = get_input_information(mmcif_file)




################################################
# Write files
################################################
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(date=timestamp,
                            ID=I.get_id(),
                            Molecule=I.get_struc_title(),
                            Title=I.get_title(),
                            Authors=I.get_authors(),
                            Entry_list=dict_to_JSlist(I.get_entry_composition()),
                            number_of_molecules=I.get_number_of_molecules(),
                            number_of_chains=I.get_number_of_chains(),
                            number_of_software=I.get_software_length(),
                            soft_list=dict_to_JSlist(I.get_software_comp()), 
                            residues=I.get_residues())

with open('Output/ValidationReport_'+sys.argv[1]+'.html',"w") as fh:
    fh.write(outputText)

pdfkit.from_file('Output/ValidationReport_'+sys.argv[1]+'.html', 'Output/ValidationReport_'+sys.argv[1]+'.pdf' ,configuration=config, options=options)

