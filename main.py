import streamlit as st
#from sklearn.ensemble import GradientBoostingClassifier
import pickle
import numpy as np
import pandas as pd
from matminer.featurizers.conversions import StrToComposition
from matminer.featurizers.composition import ElementProperty
from matminer.featurizers.conversions import CompositionToOxidComposition
from matminer.featurizers.composition import OxidationStates

with open("dump/scaler", 'rb') as file:
    scaler = pickle.load(file)
with open("dump/model_kappa", 'rb') as file:
    model_kappa = pickle.load(file)

ep_feat = ElementProperty.from_preset(preset_name="magpie")
os_feat = OxidationStates()

to_predict=pd.DataFrame(columns=["compound","nat_form","nelem"])

cmpd="Mn2CoCrP2"

to_predict.loc[0,"compound"]=cmpd
to_predict= StrToComposition().featurize_dataframe(to_predict, "compound")
to_predict = ep_feat.featurize_dataframe(to_predict, col_id="composition")
to_predict = CompositionToOxidComposition().featurize_dataframe(to_predict, "composition")
to_predict= os_feat.featurize_dataframe(to_predict, "composition_oxid")
to_predict.loc[0,"nelem"]=len(to_predict["composition"][0].as_dict().keys())
to_predict.loc[0,"nat_form"]=sum(to_predict["composition"][0].as_dict().values())

def predict(df):
    X_to_predict=scaler.transform(to_predict.drop(['composition','composition_oxid'], axis=1).set_index('compound').values)
    return np.exp(model_kappa.predict(X_to_predict))

st.write(to_predict.loc[0,"nat_form"])
