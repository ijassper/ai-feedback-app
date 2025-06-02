app_code = """
import streamlit as st
import openai

# 환경변수 또는 사용자 입력으로 API 키 설정
openai.api_key = st.text_input("🔑 OpenAI API 키를 입력하세요", type="password")

st.set_page_config(page_title="AI 기준 비교 피드백 앱")
st.title("📚 교수학습 계획서 기준 비교 피드백")

# 기준 파일 불러오기
try:
    with open("standard.txt", "r", encoding="utf-8") as f:
        standard_text = f.read()
except:
    st.error("기준 자료 파일이 없습니다. 먼저 업로드하거나 생성해 주세요.")
    standard_text = ""

# 사용자 입력
user_input = st.text_area("📝 교수학습 및 평가 계획서를 입력하세요", height=200)

# 피드백 버튼
if st.button("🤖 피드백 받기"):
    if not openai.api_key:
        st.warning("API 키를 입력해 주세요.")
    elif not user_input.strip():
        st.warning("계획서를 입력해 주세요.")
    else:
        with st.spinner("AI가 피드백을 작성 중입니다..."):
            prompt = f\"""[기준 자료]
{standard_text}

[사용자 입력]
{user_input}

위 기준 자료에 비추어 사용자 입력이 기준을 얼마나 충족하는지 평가하고 부족한 부분이 있다면 피드백을 제공해 주세요.\"""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                feedback = response["choices"][0]["message"]["content"]
                st.subheader("📌 AI 피드백 결과")
                st.write(feedback)
            except Exception as e:
                st.error(f"오류 발생: {e}")
"""

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)
