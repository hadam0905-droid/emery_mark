
import streamlit as st
import random
from PIL import Image

st.set_page_config(page_title="군 계급 맞추기", page_icon="🎖️")

# 원본 계급장 사진 불러오기
image = Image.open("2015010609533000000024079.jpg")

# 한국군 계급장 리스트
# 각 항목: 계급 이름, 사진 자르기 좌표, 정답으로 인정할 별칭
ranks = [
    {"name": "이병", "crop": (155, 840, 190, 885), "aliases": ["이등병"]},
    {"name": "일병", "crop": (155, 800, 190, 840), "aliases": ["일등병"]},
    {"name": "상병", "crop": (155, 755, 190, 800), "aliases": ["상등병"]},
    {"name": "병장", "crop": (155, 715, 190, 755), "aliases": []},

    {"name": "하사", "crop": (105, 675, 190, 715), "aliases": []},
    {"name": "중사", "crop": (105, 630, 190, 675), "aliases": []},
    {"name": "상사", "crop": (105, 590, 190, 630), "aliases": []},
    {"name": "원사", "crop": (105, 550, 190, 590), "aliases": []},

    {"name": "준위", "crop": (105, 505, 190, 550), "aliases": []},

    {"name": "소위", "crop": (105, 462, 190, 505), "aliases": []},
    {"name": "중위", "crop": (105, 420, 190, 462), "aliases": []},
    {"name": "대위", "crop": (105, 380, 190, 420), "aliases": []},

    {"name": "소령", "crop": (105, 335, 190, 378), "aliases": []},
    {"name": "중령", "crop": (105, 295, 190, 335), "aliases": []},
    {"name": "대령", "crop": (105, 255, 190, 295), "aliases": []},

    {"name": "준장", "crop": (105, 205, 190, 250), "aliases": []},
    {"name": "소장", "crop": (105, 165, 190, 205), "aliases": []},
    {"name": "중장", "crop": (105, 125, 190, 165), "aliases": []},
    {"name": "대장", "crop": (105, 85, 190, 125), "aliases": []},
    {"name": "원수", "crop": (105, 45, 190, 85), "aliases": ["국가원수"]}
]


# 계급장 10개 무작위 추출 함수
def draw_ranks(rank_list, remaining):
    selected = random.sample(
        remaining,
        min(10, len(remaining))
    )

    new_remaining = [
        i for i in remaining if i not in selected
    ]

    return selected, new_remaining


# 답안 정리 함수
def normalize(answer):
    return answer.strip().replace(" ", "").lower()


# 게임 초기화
if "remaining" not in st.session_state:
    st.session_state.remaining = list(range(len(ranks)))
    st.session_state.batch, st.session_state.remaining = draw_ranks(
        ranks, st.session_state.remaining
    )
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.correct = False
    st.session_state.batch_number = 1
    st.session_state.finished = False


# 화면 제목
st.title("🎖️ 군 계급 맞추기 게임")
st.write("계급장 사진을 보고 올바른 군 계급을 입력하세요!")

st.divider()


# 게임 진행
if not st.session_state.finished:

    current_index = st.session_state.batch[
        st.session_state.index
    ]

    current_rank = ranks[current_index]

    # 진행 상황 표시
    st.subheader(
        f"문제 {len(ranks) - len(st.session_state.remaining) - len(st.session_state.batch) + st.session_state.index + 1} / {len(ranks)}"
    )

    st.write(f"현재 점수: {st.session_state.score}점")

    # 계급장 사진 출력
    st.subheader("이 계급장의 계급은?")
    
    rank_image = image.crop(current_rank["crop"])

    st.image(
        rank_image,
        width=300
    )

    # 답안 입력
    with st.form(key=f"answer_{st.session_state.batch_number}_{st.session_state.index}"):

        answer = st.text_input(
            "계급 이름을 입력하세요.",
            placeholder="예: 이병"
        )

        submit = st.form_submit_button("정답 확인")

        if submit and not st.session_state.answered:

            if answer.strip() == "":
                st.warning("답을 입력해주세요.")

            else:
                user_answer = normalize(answer)

                accepted_answers = [
                    normalize(current_rank["name"])
                ] + [
                    normalize(a) for a in current_rank["aliases"]
                ]

                # 정답 및 오답 판별
                if user_answer in accepted_answers:
                    st.session_state.feedback = "정답! +1점 🎉"
                    st.session_state.score += 1
                    st.session_state.correct = True

                elif user_answer != "":
                    st.session_state.feedback = "오답! 다음 문제를 푸시오."
                    st.session_state.correct = False

                st.session_state.answered = True

    # 정답 확인 결과 출력
    if st.session_state.answered:

        if st.session_state.correct:
            st.success(st.session_state.feedback)

        else:
            st.error(st.session_state.feedback)

        # 다음 문제 버튼
        if st.button("다음 문제"):

            st.session_state.index += 1
            st.session_state.answered = False

            # 현재 10문제를 모두 풀었을 경우
            if st.session_state.index >= len(st.session_state.batch):

                if len(st.session_state.remaining) > 0:

                    # 남은 계급장에서 새로운 10문제 추출
                    st.session_state.batch, st.session_state.remaining = draw_ranks(
                        ranks, st.session_state.remaining
                    )

                    st.session_state.index = 0
                    st.session_state.batch_number += 1

                else:
                    # 모든 계급장 출제 완료
                    st.session_state.finished = True

            st.rerun()


# 모든 문제를 풀었을 경우
else:

    st.balloons()

    st.title("🏆 게임 종료!")

    st.success("모든 군 계급 문제를 풀었습니다!")

    st.subheader(
        f"최종 점수: {st.session_state.score} / {len(ranks)}점"
    )

    st.write(
        f"정답 개수: {st.session_state.score}개"
    )

    st.write(
        f"오답 개수: {len(ranks) - st.session_state.score}개"
    )

    if st.button("다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
