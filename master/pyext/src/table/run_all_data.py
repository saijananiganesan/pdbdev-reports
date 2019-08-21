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
path_dir='/home/ganesans/PDB-dev/master/pyext/src/data/*'
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
#################################################
def get_all_files(path_dir):
    return glob.glob(path_dir)

all_files=get_all_files(path_dir)
################################################
# Run all files
################################################
def run_all():
    for filename in all_files:
        print (filename)
        mmcif_file=filename
        mmcif_output = os.path.basename(filename)
        name=mmcif_file.split('.')[0].split('_')[0]
        I = get_input_information(mmcif_file)
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
                            number_of_datasets=I.get_dataset_length(),
                            Datasets_list=dict_to_JSlist(I.get_dataset_comp()),
                            residues=I.get_residues())

        with open('Output/ValidationReport_'+mmcif_output+'.html',"w") as fh:
            fh.write(outputText)

        pdfkit.from_file('Output/ValidationReport_'+mmcif_output+'.html', 'Output/ValidationReport_'+mmcif_output+'.pdf' ,configuration=config, options=options)

#################################################
# Run one file
################################################
def run_one(mmcif):
    mmcif_file=mmcif
    name=mmcif_file.split('.')[0].split('_')[0]
    I = get_input_information(mmcif_file)
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
                            number_of_datasets=I.get_dataset_length(),
                            Datasets_list=dict_to_JSlist(I.get_dataset_comp()),
                            residues=I.get_residues())

    with open('Output/ValidationReport_'+mmcif_file+'.html',"w") as fh:
        fh.write(outputText)

    pdfkit.from_file('Output/ValidationReport_'+mmcif_file+'.html', 'Output/ValidationReport_'+mmcif_file+'.pdf' ,configuration=config, options=options)

############################################
if __name__ == "__main__":
    run_one(sys.argv[1])
#irun_all()
