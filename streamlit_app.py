import streamlit as st
import os
from groq import Groq
from PIL import Image
import mariadb
from dotenv import load_dotenv

load_dotenv()

# 환경 변수 가져오기
host = os.getenv("DATABASE_HOST")
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
database = os.getenv("DATABASE_NAME")


st.set_page_config(page_title='Demo Chat',page_icon='🤖')
avatar = {"assistant": "🤖", "user": "🌀"}

st.sidebar.header('Groq API 변수입력')
input_api_key = st.sidebar.text_input('당신의 groq api키를 입력해주세요.', type="password")
input_model_type = st.sidebar.selectbox('api model 선택해주세요.', ['llama3-70b-8192', 'deepseek-r1-distill-qwen-32b'])

# 환경 변수로부터 API 키 가져오기
if not input_api_key:
    st.error("API키를 입력해야만 서비스를 이용 할 수 있습니다.")
    st.stop()
else:
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi. I'm Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. Ask me anything."}]

# MariaDB 연결 설정
conn = mariadb.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cur = conn.cursor()

# Groq 클라이언트 초기화
client = Groq(api_key=input_api_key)

def get_response(question):
    """ Groq API 함수 """
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": question}],
        model=input_model_type
    )
    return chat_completion.choices[0].message.content

# Streamlit UI
st.title('💬Groq API 데모')

# 사용자 입력
user_input = st.chat_input("질문을 입력해주세요.")

if 'history' not in st.session_state:
    st.session_state.history = []

if 'selected_seq' not in st.session_state:
    st.session_state.selected_seq = None

if user_input:
    with st.chat_message('user', avatar='🌀'):
        st.write(user_input)
    
    with st.chat_message('assistant', avatar='🤖'):
        response = get_response(user_input)
        st.write(response)

    # DB에 질문/답변 INSERT
    insert_sql = "INSERT INTO tb_conversation (API_KEY, USER_INPUT, RESPONSE) VALUES (?, ?, ?)"
    cur.execute(insert_sql, (input_api_key, user_input, response))
    conn.commit()

# 항상 DB에서 현재 기록 조회
select_sql = "SELECT SEQ, USER_INPUT FROM tb_conversation WHERE API_KEY = ? ORDER BY SEQ ASC LIMIT 5 "
cur.execute(select_sql, (input_api_key,))
rows = cur.fetchall()

# 사이드바 - 히스토리
st.sidebar.header('History')

for seq, user_input in rows:
    # 텍스트처럼 보이는 버튼 만들기 (마우스 올리면 손가락 모양)
    if st.sidebar.button(user_input, key=f"user_input_{seq}"):
        st.session_state.selected_seq = seq

# 사용자가 사이드바에서 뭘 클릭했다면
if st.session_state.selected_seq:
    cur.execute("SELECT USER_INPUT, RESPONSE FROM tb_conversation WHERE SEQ = ?", (st.session_state.selected_seq,))
    data = cur.fetchone()

    if data:
        selected_user_input, selected_response = data
        st.subheader(f"🌀: {selected_user_input}")
        st.write(f"🤖: {selected_response}")

# 고양이 이미지
cat_img = Image.open('cat.jpg')
st.sidebar.image(cat_img)
