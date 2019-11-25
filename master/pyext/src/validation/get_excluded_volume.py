import pandas as pd
import glob
import sys,os,math
import numpy as np
import pandas as pd
import validation
import ihm
import ihm.reader
import re,pickle
import multiprocessing as mp

class get_excluded_volume(validation.get_input_information):
    def __init__(self,mmcif_file):
        super().__init__(mmcif_file)
        self.ID=str(validation.get_input_information.get_id(self))
        self.nos=validation.get_input_information.get_number_of_models(self)
        
    def get_all_spheres (self):
        Model_object=[b for i in self.system.state_groups for j in i for a in j for b in a]
        model_dict={i+1:j._spheres for i,j in enumerate(Model_object)}
        return model_dict
    
    def get_nCr(self,n,r):
        f=math.factorial
        return (f(n)/(f(r)*f(n-r)))

    def get_violation_percentage(self,models_spheres_df,viols):
        number_of_violations=sum(list(viols.values()))
        number_of_combinations=self.get_nCr(models_spheres_df.shape[1],2)
        return (1-number_of_violations/number_of_combinations)*100

    def get_violation_normalized(self,models_spheres_df,viols):
        number_of_violations=sum(list(viols.values()))
        normalization_constant=models_spheres_df.shape[1]*math.log(models_spheres_df.shape[1],10)
        return (1-number_of_violations/normalization_constant)*100

    def get_xyzr(self,spheres):
        model_spheres={i+1:[j.x,j.y,j.z,j.radius] for i,j in enumerate(spheres)}
        model_spheres_df=pd.DataFrame(model_spheres, index=['X','Y','Z','R'])
        return model_spheres_df

    def get_xyzr_complete(self,model_ID,spheres):
        model_spheres={i+1:[j.x,j.y,j.z,j.radius,j.asym_unit._id,model_ID] for i,j in enumerate(spheres)}
        model_spheres_df=pd.DataFrame(model_spheres, index=['X','Y','Z','R','Chain_ID','Model_ID'])
        print (model_spheres_df.head())
        print (model_spheres_df.tail())
        return model_spheres_df

    def get_violation_dict(self,model_spheres_df):
        viols={}
        for i,col in model_spheres_df.iteritems():
            if i< model_spheres_df.shape[1]:
                sphere_R=model_spheres_df.iloc[-1,i:]
                remaining=model_spheres_df.iloc[:-1,i:]
                subt_alone=remaining.sub(col[:-1], axis=0)
                final_df=np.square(subt_alone)
                final_df.loc['sqrt']=np.sqrt(final_df.sum(axis=0))
                final_df.loc['R_tot']=sphere_R.add(col[[-1]].tolist()[0]).to_list()
                final_df.loc['distances']=final_df.loc['sqrt']-final_df.loc['R_tot']
                final_df.loc['violations']=final_df.loc['distances'].apply(lambda x: 1 if x <0 else 0)
                viols[i]=final_df.loc['violations'].sum(axis=0)
        return viols 
    
    def get_exc_vol_for_models(self,model_dict):
        excluded_volume={'Models':[],'Excluded Volume Satisfaction':[], 'Number of violations':[]}
        for i, j in model_dict.items():
            excluded_volume['Models'].append(i)
            df=self.get_xyzr(j)
            excluded_volume['Excluded Volume Satisfaction'].append(round(self.get_violation_percentage(df,self.get_violation_dict(df)),2))
            excluded_volume['Number of violations'].append(sum(list(self.get_violation_dict(df).values())))
        f_exv=open(os.path.join(os.getcwd(),'static/results/',self.ID+'exv.txt'),'w+')
        print (excluded_volume['Models'], file=f_exv)
        print (excluded_volume['Excluded Volume Satisfaction'],file=f_exv)
        print (excluded_volume['Number of violations'], file=f_exv)
        return excluded_volume

    def get_exc_vol_for_models_normalized(self,model_dict):
        excluded_volume={'Models':[],'Excluded Volume Satisfaction':[]}
        for i, j in model_dict.items():
            excluded_volume['Models'].append(i)
            df=self.get_xyzr(j)
            satisfaction=self.get_violation_normalized(df,self.get_violation_dict(df))
            excluded_volume['Excluded Volume Satisfaction'].append(round(satisfaction,2))
        return excluded_volume

    def get_exc_vol_given_sphere_parallel(self,sphere_list):
        df=self.get_xyzr(sphere_list)
        violation_dict=self.get_violation_dict(df)
        satisfaction=round(self.get_violation_percentage(df,violation_dict),2)
        violations=sum(list(violation_dict.values()))
        return (satisfaction,violations)

    def run_exc_vol_parallel(self,model_dict):
        list_of_sphere_list=list(model_dict.values())
        pool=mp.Pool(processes=len(list(model_dict.keys())))
        complete_list=pool.map(self.get_exc_vol_given_sphere_parallel,list(model_dict.values()))
        excluded_volume={'Models':list(model_dict.keys()),'Excluded Volume Satisfaction':[i[0] for i in complete_list], 'Number of violations':[i[1] for i in complete_list]}

        #excluded_volume={'Models':list(model_dict.keys()),'Excluded Volume Satisfaction':[i[0] for i in complete_list], 'Number of violations':[(int(i[1]),int((i[1]/(1-0.01*i[0])))) for i in complete_list]}
        f_exv=open(os.path.join(os.getcwd(),'static/results/',self.ID+'exv.txt'),'w+')
        print (excluded_volume['Models'], file=f_exv)
        print (excluded_volume['Excluded Volume Satisfaction'],file=f_exv)
        print (excluded_volume['Number of violations'], file=f_exv)
        return excluded_volume

    def exv_readable_format(self,exv):
        fin_string=''
        for i in exv['Models']:
            fin_string+'Model-'+str(i)+': '+'Number of violations-' + str(exv['Number of violations'])
        return fin_string


