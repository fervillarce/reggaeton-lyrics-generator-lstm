import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy
import pandas


st.title("Let's generate reggaeton")
st.write('Bienvenido a donde las letras de reggaeton se hacen realidad')

seed = st.text_input('Escribe una frase', value='Mami ya tu sabe')
sentence = 'que yo te quiero perrial'
st.write(seed, sentence)

st.balloons()