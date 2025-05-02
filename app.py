import streamlit as st
import time
import ast
import ex_template

# Initialize & Setting
## Session State
if "started" not in st.session_state:
    st.session_state.started = False
## Exercise 0
EX_NAME_0 = "かかと上げ下ろし"
SETS_0_DEF, TIME_0_DEF = 10, 5
SETS_0_MIN, SETS_0_MAX = 5, 50
TIME_0_MIN, TIME_0_MAX = 5, 60
SETS_STEP_0, TIME_STEP_0 = 5, 5
## Exercise 1
EX_NAME_1 = "片足立ち"
SETS_1_DEF, TIME_1_DEF = 5, 60
SETS_1_MIN, SETS_1_MAX = 5, 50
TIME_1_MIN, TIME_1_MAX = 30, 180
SETS_STEP_1, TIME_STEP_1 = 5, 30
## Template
tmpl_ex0 = ex_template.tmpl_ex0
tmpl_ex1 = ex_template.tmpl_ex1
tmpl_msg = ex_template.tmpl_msg

# Function
def make_exercise_list(training_plan):
    """
    トレーニング計画を元に「トレーニング指示リスト」を作成する関数
    :param training_plan: トレーニング計画（JSON風）
    :return: トレーニング指示リスト
    """
    ex_lst = []
    for training in training_plan:
        name = training["name"]      
        for num in range(training["start_count"], -1, -1):
            ex_lst.append(["運動開始まで", num, 0, name])
        for sets_num in range(1, training["sets"]+1):
            for p in training["plan"]:
                for count in range(p["time"]+1):
                    if p["count"] == 1:
                        ex_lst.append([p["text"], count, sets_num, name])
                    elif p["count"] == -1:
                        start_count = p["time"]
                        ex_lst.append([p["text"], start_count - count, sets_num, name])
                    else:
                        ex_lst.append([p["text"], "　", sets_num, name])
    ex_lst.append(["　", "　", "", "お疲れさまでした"])
    return ex_lst

# Streamlit
## Sidebar
with st.sidebar:
    training_0 = st.checkbox(f"**{EX_NAME_0}**", value=True)
    sets_num_0 = st.number_input(f"セット数（回）[ {SETS_0_MIN} ~ {SETS_0_MAX} ]",
                                 min_value=SETS_0_MIN, max_value=SETS_0_MAX, value=SETS_0_DEF,
                                 step=SETS_STEP_0)
    time_num_0 = st.number_input(f"キープ時間（秒） [ {TIME_0_MIN} ~ {TIME_0_MAX} ]",
                                 min_value=TIME_0_MIN, max_value=TIME_0_MAX, value=TIME_0_DEF,
                                 step=TIME_STEP_0)
    st.write("")
    training_1 = st.checkbox(f"**{EX_NAME_1}**", value=True)
    sets_num_1 = st.number_input(f"セット数（回） [ {SETS_1_MIN} ~ {SETS_1_MAX} ]",
                                 min_value=SETS_1_MIN, max_value=SETS_1_MAX, value=SETS_1_DEF,
                                 step=SETS_STEP_1)
    time_num_1 = st.number_input(f"キープ時間（秒） [ {TIME_1_MIN} ~ {TIME_1_MAX} ]",
                                 min_value=TIME_1_MIN, max_value=TIME_1_MAX, value=TIME_1_DEF,
                                 step=TIME_STEP_1)

## Main
### Layout
main_msg = st.empty()
main_btn = st.empty()

### Start
main_msg.markdown("<h1 style='color: lightblue;'>運動しましょう</h1><br><br>",
                  unsafe_allow_html=True)
if main_btn.button("スタート"):
    st.session_state.started = True

### Operation
if st.session_state.started:
    # トレーニング計画
    training_plan = [] # トレーニング計画（JSON風）
    if training_0: # かかと上げ下ろし
        training_plan.append(ast.literal_eval(
            tmpl_ex0.substitute(sets_num=sets_num_0, time_num=time_num_0)
        ))
    if training_1: # 片足立ち
        training_plan.append(ast.literal_eval(
            tmpl_ex1.substitute(sets_num=sets_num_1, time_num=time_num_1)
        ))
    exercise_list = make_exercise_list(training_plan) # 「トレーニング指示リスト」作成

    # トレーニング開始
    st.session_state.started = False
    main_btn.empty() # ボタンを消す
    for exercise in exercise_list: # 「トレーニング指示リスト」に従い表示
        text, count, sets, name = exercise
        main_msg.markdown(
            tmpl_msg.substitute(text=text, count=count, sets=sets, name=name),
            unsafe_allow_html=True
        )
        time.sleep(1)
