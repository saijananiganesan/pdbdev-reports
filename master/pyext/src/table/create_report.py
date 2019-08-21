###################################
# Script to :
# 1)generate information from PDB-DEV file
#
#
#
# ganesans - Salilab - UCSF
# ganesans@salilab.org
###################################

import ihm
import ihm.reader
import pandas as pd
import utils
import glob
import os
import numpy as np
import re
import pandas as pd

#########################
#Useful functions
#########################
def dict_to_list(d):
    L = []
    for k,v in d.items():
        if isinstance(v, list):
            L.append([k,v])
        else:
            L.append([k,[v]])
    return L

def dict_to_JSlist(d):
    L = []
    if len(list(d.keys()))>0:
        L.append(list(d.keys()))
        target=list(d.values())
        for i in range(len(target[0])):
            ltt=[]
            for j in target:
                ltt.append(j[i])
            L.append(ltt)
    return L

def islistempty(inlist):
    if isinstance (inlist,list):
        return all(map(islistempty,inlist))
    return False

def cat_list_string(listn):
    result=' '
    for i in range(len(listn)):
        if i==0:
            result += str(listn[i])
        else:
            result += ','
            result += str(listn[i])
    return result

#########################
#Get information from IHM reader
#########################

class get_input_information(object):
    def __init__(self,mmcif_file):
        self.mmcif_file = mmcif_file
        self.datasets = {}
        self.entities = {}
        self.model = ihm.model.Model
        self.system, = ihm.reader.read(open(self.mmcif_file),
                                  model_class=self.model)
    def get_databases(self):
        dbs=self.system.orphan_datasets
        return dbs

    def get_id(self):
        if self.system.id is 'model':
            id=self.get_id_from_entry()
        else:
            id=self.system.id.split('_')[0]+self.system.id.split('_')[1]
        return id

    def get_id_from_entry(self):
        sf=open(self.mmcif_file,'r')
        for i,ln in enumerate(sf.readlines()):
            line =ln.strip().split(' ')
            if '_entry' in line[0]:
                entry_init=line[-1]
                entry=entry_init.split('_')[0]+entry_init.split('_')[1]
        return entry

    def get_title(self):
        cit=self.system.citations
        tit=cit[0].title
        return tit

    def get_authors(self):
        cit=self.system.citations
        aut=cit[0].authors
        for i in range(0,len(aut)):
            if i==0:
                authors=str(aut[i])
            else:
                authors+=';'+str(aut[i])
        return authors

    def get_struc_title(self):
        strc=self.system.title
        if strc is None:
            e=self.system.entities
            mol_name=e.description
        else:
            mol_name=strc
        return mol_name

    def get_number_of_molecules(self):
        return self.system.entities[0].number_of_molecules

    def get_number_of_chains(self):
        chain=[];used=[]
        lists= self.system.orphan_assemblies
        for k in self.system.orphan_assemblies:
            for l in k:
                chain.append(l._id)
            unique=[used.append(x) for x in chain if x not in used]
        return len(used)

    def get_residues(self):
        residues=[]
        lists= self.system.orphan_assemblies
        for k in self.system.orphan_assemblies:
            for l in k:
                if l.seq_id_range[0] is not None:
                    residues.append(l.seq_id_range[1]-l.seq_id_range[0]+1)
                elif l.seq_id_range[0] is None:
                    residues.append('None Listed')
        return cat_list_string(residues)

    def get_entry_composition(self):
        entry_comp={'Molecule ID':[],'Molecule Name':[],'Chain ID':[],'Total Residues':[]}
        lists= self.system.orphan_assemblies
        liste=self.system.entities
        print (len(lists), len(liste))
        for i in liste:
            entry_comp['Molecule Name'].append(i.description)
            print (i,i.description)
        if len(liste)<len(lists[0]):
            val=entry_comp['Molecule Name']
            valf=val*len(lists[0])
            entry_comp['Molecule Name']=valf
        k=lists[0]
        for l in k:
            print (l._id)
            entry_comp['Molecule ID'].append(k._id)
            entry_comp['Chain ID'].append(l._id)
            if l.seq_id_range[0] is not None:
                entry_comp['Total Residues'].append(l.seq_id_range[1]-l.seq_id_range[0]+1)
            elif l.seq_id_range[0] is None:
                entry_comp['Total Residues'].append('None Listed')
        return entry_comp


    def get_software_length(self):
        lists=self.system.software
        if lists is None:
            return 0
        else:
            return len(lists)

    def get_software_comp (self):
        software_comp={'ID':[],'Software Name':[],'Software Version':[],'Software Classification':[]}
        lists=self.system.software
        if len(lists)>0:
            for i in lists:
                software_comp['ID'].append(i._id)
                software_comp['Software Name'].append(i.name)
                if str(i.version) is '?':
                    vers='None'
                else:
                    vers=str(i.version)
                software_comp['Software Version'].append(vers)
                software_comp['Software Classification'].append(i.classification)
            final_software_composition=software_comp
        else:
            final_software_composition={}
        return final_software_composition

    def get_dataset_length(self):
        lists=self.system.orphan_datasets
        if lists is None:
            return 0
        else:
            return len(lists)

    def get_dataset_comp (self):
        dataset_comp={'ID':[],'Dataset Type':[],'Database Name':[],'Data Access Code':[]}
        lists=self.system.orphan_datasets
        if len(lists)>0:
            for i in lists:
                try:
                    loc=i.location.db_name
                except AttributeError as error:
                    loc=str('Not Listed')
                try:
                    acc=i.location.access_code
                except AttributeError as error:
                    acc=str('None')
                dataset_comp['ID'].append(i._id)
                dataset_comp['Dataset Type'].append(i.data_type)
                dataset_comp['Database Name'].append(str(loc))
                dataset_comp['Data Access Code'].append(acc)
        return dataset_comp

#########################
#Get information from 
#########################

class get_attributes(object):
    def __init__(self,mmcif_file):
        self.mmcif_file = mmcif_file
        self.categories = []

    

