import numpy as np
import altair as alt
import pandas as pd
import streamlit as st

st.header('st.write')

st.write('Hello, *Wolrd!* :sunglasses:')

st.write(1234)

df = pd.DataFrame({
    '첫 번째 컬럼': [1,2,3,4],
    '두 번째 컬럼':[10,20,30,40]
    })
st.write(df)

st.write('아래는 DataFrame입니다.',df,'위는 dataframe입니다.')

df2 = pd.DataFrame(
    np.random.randn(200,3),
    columns=['a','b','c'])
c=alt.Chart(df2).mark_circle().encode(
    x='a',y='b',size='c',color='c',tooltip=['a','b','c'])
st.write(c)