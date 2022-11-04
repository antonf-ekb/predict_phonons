import streamlit as st
import pickle
import numpy as np
import pandas as pd

from matminer.featurizers.conversions import StrToComposition
from matminer.featurizers.composition import ElementProperty
from matminer.featurizers.conversions import CompositionToOxidComposition
from matminer.featurizers.composition import OxidationStates

#import models
with open("dump/scaler", 'rb') as file:
    scaler = pickle.load(file)
with open("dump/model_kappa", 'rb') as file:
    model_kappa = pickle.load(file)
with open("dump/model_bulk", 'rb') as file:
    model_bulk = pickle.load(file)
with open("dump/model_shear", 'rb') as file:
    model_shear = pickle.load(file)

ep_feat = ElementProperty.from_preset(preset_name="magpie")
os_feat = OxidationStates()

st.header("Предсказание теплопроводности и упругих модулей кристаллических материалов")

# cmpd="Mn2CoCrP2"
cmpd = st.text_input("Введите химическую формулу соединения:")

if (st.button("Предсказать")):
    #make descriptor from the compound formula
    to_predict = pd.DataFrame(columns=["compound","nat_form","nelem"])
    try:
        to_predict.loc[0,"compound"]=cmpd
        to_predict = StrToComposition().featurize_dataframe(to_predict, "compound")
        to_predict = ep_feat.featurize_dataframe(to_predict, col_id="composition")
        to_predict = CompositionToOxidComposition().featurize_dataframe(to_predict, "composition")
        to_predict = os_feat.featurize_dataframe(to_predict, "composition_oxid")
        to_predict.loc[0,"nelem"]=len(to_predict["composition"][0].as_dict().keys())
        to_predict.loc[0,"nat_form"]=sum(to_predict["composition"][0].as_dict().values())
        X_to_predict = scaler.transform(to_predict.drop(['composition','composition_oxid'], axis=1).set_index('compound').values)
        #make prediction
        st.write("Решеточная теплопроводность: "+str(round(np.exp(model_kappa.predict(X_to_predict))[0],2)) + " Вт/(м*К)")
        st.write("Модуль всестороннего сжатия: "+str(round(model_bulk.predict(X_to_predict)[0])) + " ГПа")
        st.write("Модуль сдвига: "+str(round(model_shear.predict(X_to_predict)[0])) + " ГПа")
    except:
        st.error("Проверьте правильность ввода формулы!")

