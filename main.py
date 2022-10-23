import streamlit as st
#from sklearn.ensemble import GradientBoostingClassifier
import pickle
import numpy as np
import pandas as pd
from matminer.featurizers.conversions import StrToComposition
from matminer.featurizers.composition import ElementProperty
from matminer.featurizers.conversions import CompositionToOxidComposition
from matminer.featurizers.composition import OxidationStates

ep_feat = ElementProperty.from_preset(preset_name="magpie")
os_feat = OxidationStates()

to_predict=pd.DataFrame(columns=["compound","nat_form","nelem"])

def make_descriptor_single(df,cmpd):
    next_num=df.shape[0]
    data=pd.DataFrame(columns=["compound","nat_form","nelem"])
    data.loc[next_num,"compound"]=cmpd
    data= StrToComposition().featurize_dataframe(data, "compound")
    data = ep_feat.featurize_dataframe(data, col_id="composition")
    data = CompositionToOxidComposition().featurize_dataframe(data, "composition")
    data = os_feat.featurize_dataframe(data, "composition_oxid")
    data.loc[next_num,"nelem"]=len(data["composition"][0].as_dict().keys())
    data.loc[next_num,"nat_form"]=sum(data["composition"][0].as_dict().values())
    df=pd.concat([df,data],axis=0)
    return df
  
to_predict=make_descriptor_single(to_predict,"Mn2CoCrP2")
st.write(to_predict)
