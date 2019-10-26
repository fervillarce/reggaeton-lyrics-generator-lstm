import nicky
import streamlit as st


def get_prediction(seed):
    return nicky.predict(seed)

st.title("El generadol de reggaeton")
st.write('Cuidado, esta red neuronal ha sido entrenada con canciones reales de reggaeton; puede contener contenido explícito :P')

seed = st.text_input('Escribe una frase', value='Mami ya tu sabe')
#sentence = 'que yo te quiero perrial'
sentence = get_prediction(seed)
st.write(seed, sentence)

#st.balloons()