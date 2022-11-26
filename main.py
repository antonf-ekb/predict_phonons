import streamlit as st
import pickle
import numpy as np
import pandas as pd
from PIL import Image
from matminer.featurizers.conversions import StrToComposition
from matminer.featurizers.composition import ElementProperty
from matminer.featurizers.conversions import CompositionToOxidComposition
from matminer.featurizers.composition import OxidationStates

def calculate_values(cmpd):
    # import models
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

    #make descriptor from the compound formula
    to_predict = pd.DataFrame(columns=["compound","nat_form","nelem"])
    try:
        to_predict.loc[0,"compound"] = cmpd
        to_predict = StrToComposition().featurize_dataframe(to_predict, "compound")
        to_predict = ep_feat.featurize_dataframe(to_predict, col_id="composition")
        to_predict = CompositionToOxidComposition().featurize_dataframe(to_predict, "composition")
        to_predict = os_feat.featurize_dataframe(to_predict, "composition_oxid")
        to_predict.loc[0,"nelem"] = len(to_predict["composition"][0].as_dict().keys())
        to_predict.loc[0,"nat_form"] = sum(to_predict["composition"][0].as_dict().values())
        X_to_predict = scaler.transform(to_predict.drop(['composition','composition_oxid'], axis=1).set_index('compound').values)

        #make prediction
        conductivity = round(np.exp(model_kappa.predict(X_to_predict))[0],2)
        compression_modulest = round(model_bulk.predict(X_to_predict)[0])
        shift_modulus = round(model_shear.predict(X_to_predict)[0])
        return [conductivity, compression_modulest, shift_modulus]
    except:
        return [0]


def main():
    # description of the sidebar
    st.sidebar.title("Как это работает")

    img = Image.open("picture.png")
    st.sidebar.image(img, width = 180)
    st.sidebar.write('На основе данных о свойствах элементов, входящих в состав соединения, таких как как:'
                     ' положение элемента в Периодической системе Менделеева, \
                       его масса, ковалентный радиус, электроотрицательность и т. д. формируется \
                       дескриптор, уникальный для каждого соединения. ')
    st.sidebar.write('Предварительно данный дескриптор \
                       был рассчитан для ~5000 соединений, данные по свойствам которых заимствовались \
                       из открытой базы данных AFLOWlib [https://aflow.org/search/]. На этой основе были обучены \
                       регрессионные модели в рамках метода градиентного бустинга. ')
    st.sidebar.write('Данное приложение рассчитывает \
                       дескриптор для задаваемого вами состава, что позволяет предсказать его свойства с помощью \
                       обученных моделей.  ')

    # description of the main unit
    st.title("Предсказание теплопроводности и упругих модулей кристаллических материалов")
    st.subheader("")
    cmpd = st.text_input("Введите химическую формулу соединения:",help="Введите формулу без пробелов",placeholder="Mn2CoCrP2" )
    if (st.button("Предсказать")):
        result = calculate_values(cmpd)
        if len(result) == 1:
            st.error("Проверьте правильность ввода формулы!")
        else:
            st.write("Решеточная теплопроводность: " + str(result[0]) + " Вт/(м*К)")
            st.write("Модуль всестороннего сжатия: " + str(result[1]) + " ГПа")
            st.write("Модуль сдвига: " + str(result[2]) + " ГПа")

if __name__=="__main__":
    main()