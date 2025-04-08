import streamlit as st
import os
from groq import Groq
from PIL import Image

st.set_page_config(page_title='Demo Chat',page_icon='🤖')
avatar = {"assistant": "🤖", "user": "🌀"}


if 'history' not in st.session_state:
    st.session_state.history=[]

st.sidebar.header('Groq API 변수입력')
input_api_key = st.sidebar.text_input('당신의 groq api키를 입력해주세요.',type="password")
input_model_type = st.sidebar.selectbox('api model 선택해주세요.',['llama3-70b-8192','deepseek-r1-distill-qwen-32b'])



# 환경 변수로부터 API 키 가져오기
if not input_api_key:
    st.error("API키를 입력해야만 서비스를 이용 할 수 있습니다.")
    st.stop()
else :
    st.session_state.messages = [{"role": "assistant", "content": "Hi. I'm Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. Ask me anything."}]

# Groq 클라이언트 초기화
client = Groq(api_key=input_api_key)

def get_response(question):
    """ Groq API 함수 """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": question}
        ],
        #model="llama3-70b-8192",
        #model="qwen-qwq-32b",
        #model="deepseek-r1-distill-qwen-32b"
        model=input_model_type
    )
    return chat_completion.choices[0].message.content



# Streamlit UI
st.title('💬Groq API 데모')

# 사용자 입력
#user_input = st.text_input("질문을 입력해주세요:")

#if st.button('회신'):
#    with st.spinner('회신중...'):
#        response = get_response(user_input)
#        st.write(response)

user_input = st.chat_input("질문을 입력해주세요.")

if user_input:
    with st.chat_message('user',avatar='🌀'):
        st.write(user_input)
    
    with st.chat_message('assistant',avatar='🤖'):
        response = get_response(user_input)
        st.write(response)

if user_input and user_input not in st.session_state.history:
    st.session_state.history.append(user_input)


st.sidebar.header('history')
for question in st.session_state.history:
    st.sidebar.write(question)

cat_img =Image.open('cat.jpg')
st.sidebar.image(cat_img)