import streamlit as st
import time
import string
import ast

# Initialize & Setting

if "started" not in st.session_state:
    st.session_state.started = False

## かかと上げ下ろし
SETS_0_DEF = 10
TIME_0_DEF = 5
SETS_0_MIN, SETS_0_MAX = 5, 50
TIME_0_MIN, TIME_0_MAX = 5, 60
SETS_STEP_0, TIME_STEP_0 = 5, 5

## 片足立ち
SETS_1_DEF = 5
TIME_1_DEF = 60
SETS_1_MIN, SETS_1_MAX = 5, 50
TIME_1_MIN, TIME_1_MAX = 30, 180
SETS_STEP_1, TIME_STEP_1 = 5, 30

## Template
tmpl_0 = string.Template("""
{
    "name": "かかと",
    "sets": ${sets_num},
    "start_count": 5,
    "plan": [
        {
            "text": "かかと上げて！",
            "time": 1,
            "count": 0,
        },
        {
            "text": "キープ！",
            "time": ${time_num},
            "count": -1,
        },
        {
            "text": "下げて",
            "time": 1,
            "count": 0,
        },
    ],
}
""")

tmpl_1 = string.Template("""
{
    "name": "かたあし",
    "sets": ${sets_num},
    "start_count": 5,
    "plan": [
        {
            "text": "右足上げて！",
            "time": 1,
            "count": 0,
        },
        {
            "text": "キープ！",
            "time": ${time_num},
            "count": -1,
        },
        {
            "text": "下げて",
            "time": 1,
            "count": 0,
        },
        {
            "text": "左足上げて！",
            "time": 1,
            "count": 0,
        },
        {
            "text": "キープ！",
            "time": ${time_num},
            "count": -1,
        },
        {
            "text": "下げて",
            "time": 1,
            "count": 0,
        },
    ],
}
""")

tmpl_msg = string.Template("""
            <h1 style='color: red;'>${text}</h1>
            <div style='text-align: center;'>
                <span style='font-size: 72px; color: lightgreen;'>${count}</span>
            </div>
            <h1 style='color: lightblue;'>${name}　${sets}</h1>
""")

# Function
# トレーニング計画を作成する関数
def make_plan(training_plan):
    plan_lst = []
    for training in training_plan:
        name = training["name"]      
        for num in range(training["start_count"], -1, -1):
            plan_lst.append(["運動開始まで", num, 0, name])
        for sets_num in range(1, training["sets"]+1):
            for p in training["plan"]:
                for count in range(p["time"]+1):
                    if p["count"] == 1:
                        plan_lst.append([p["text"], count, sets_num, name])
                    elif p["count"] == -1:
                        start_count = p["time"]
                        plan_lst.append([p["text"], start_count - count, sets_num, name])
                    else:
                        plan_lst.append([p["text"], "　", sets_num, name])
    plan_lst.append(["　", "　", "", "お疲れさまでした"])
    return plan_lst

# Streamlit
## Sidebar
with st.sidebar:
    training_0 = st.checkbox("**かかと上げ下ろし**", value=True)
    sets_num_0 = st.number_input(f"セット数（回）[ {SETS_0_MIN}~{SETS_0_MAX} ]",
                                 min_value=SETS_0_MIN, max_value=SETS_0_MAX, value=SETS_0_DEF,
                                 step=SETS_STEP_0)
    time_num_0 = st.number_input(f"キープ時間（秒） [ {TIME_0_MIN}~{TIME_0_MAX} ]",
                                 min_value=TIME_0_MIN, max_value=TIME_0_MAX, value=TIME_0_DEF,
                                 step=TIME_STEP_0)
    st.write("")
    training_1 = st.checkbox("**片足立ち**", value=True)
    sets_num_1 = st.number_input(f"セット数（回） [ {SETS_1_MIN}~{SETS_1_MAX} ]",
                                 min_value=SETS_1_MIN, max_value=SETS_1_MAX, value=SETS_1_DEF,
                                 step=SETS_STEP_1)
    time_num_1 = st.number_input(f"キープ時間（秒） [ {TIME_1_MIN}~{TIME_1_MAX} ]",
                                 min_value=TIME_1_MIN, max_value=TIME_1_MAX, value=TIME_1_DEF,
                                 step=TIME_STEP_1)

## Main
### Layout
main_msg = st.empty()
start_btn = st.empty()

### Start
main_msg.markdown("<h1 style='color: lightblue;'>運動しましょう</h1>",
                  unsafe_allow_html=True)

if start_btn.button("スタート"):
    st.session_state.started = True

### Operation
if st.session_state.started:
    # トレーニング計画
    training_plan = [] # トレーニング計画（JSON風）
    if training_0: # かかと上げ下ろし
        training_plan.append(ast.literal_eval(
            tmpl_0.substitute(sets_num=sets_num_0, time_num=time_num_0)
        ))
    if training_1: # 片足立ち
        training_plan.append(ast.literal_eval(
            tmpl_1.substitute(sets_num=sets_num_1, time_num=time_num_1)
        )) 
    training_list = make_plan(training_plan) # １秒毎の指示リストを作成
    # トレーニング開始
    st.session_state.started = False
    start_btn.empty()
    for training in training_list: # １秒毎の指示リストに従い表示
        text, count, sets, name = training
        main_msg.markdown(
            tmpl_msg.substitute(text=text, count=count, sets=sets, name=name),
            unsafe_allow_html=True
        )
        time.sleep(1)
