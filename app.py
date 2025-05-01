import streamlit as st
import time
import string
import ast

# Default settings

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

# Data
temp_0 = string.Template("""
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

temp_1 = string.Template("""
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

def make_plan(plan_dic):
    plan = []
    for training in plan_dic:
        name = training["name"]      
        for num in range(training["start_count"], -1, -1):
            plan.append(["運動開始まで", num, 0, name])
        for sets_num in range(1, training["sets"]+1):
            for p in training["plan"]:
                for count in range(p["time"]+1):
                    if p["count"] == 1:
                        plan.append([p["text"], count, sets_num, name])
                    elif p["count"] == -1:
                        start_count = p["time"]
                        plan.append([p["text"], start_count - count, sets_num, name])
                    else:
                        plan.append([p["text"], "　", sets_num, name])
    return plan

# Streamlit
## Sidebar
plan = []
with st.sidebar:
    st.write("**かかと上げ下ろし**")
    sets_num_0 = st.number_input(f"セット数（回）[ {SETS_0_MIN}~{SETS_0_MAX} ]",
                                 min_value=SETS_0_MIN, max_value=SETS_0_MAX, value=SETS_0_DEF,
                                 step=SETS_STEP_0, key=0)
    time_num_0 = st.number_input(f"キープ時間（秒） [ {TIME_0_MIN}~{TIME_0_MAX} ]",
                                 min_value=TIME_0_MIN, max_value=TIME_0_MAX, value=TIME_0_DEF,
                                 step=TIME_STEP_0, key=1)
    st.write("")
    st.write("**片足立ち**")
    sets_num_1 = st.number_input(f"セット数（回） [ {SETS_1_MIN}~{SETS_1_MAX} ]",
                                 min_value=SETS_1_MIN, max_value=SETS_1_MAX, value=SETS_1_DEF,
                                 step=SETS_STEP_1, key=2)
    time_num_1 = st.number_input(f"キープ時間（秒） [ {TIME_1_MIN}~{TIME_1_MAX} ]",
                                 min_value=TIME_1_MIN, max_value=TIME_1_MAX, value=TIME_1_DEF,
                                 step=TIME_STEP_1, key=3)

    if "started" not in st.session_state:
        st.session_state.started = False
    if st.button("スタート"):
        st.session_state.started = True

        plan_data = [
            ast.literal_eval(temp_0.substitute(sets_num=sets_num_0, time_num=time_num_0)),
            ast.literal_eval(temp_1.substitute(sets_num=sets_num_1, time_num=time_num_1))
        ]
        plan = make_plan(plan_data)

# Main
main_msg = st.empty()

if st.session_state.started:
    end_msg = st.empty()
    for counter in range(len(plan)):
        text, count, sets, name = plan[counter]
        main_msg.markdown(
            f"""
            <h1 style='color: red;'>{text}</h1>
            <div style='text-align: center;'>
                <span style='font-size: 72px; color: lightgreen;'>{count}</span>
            </div>
            <h1 style='color: lightblue;'>{name}　{sets}</h1>
            """,
            unsafe_allow_html=True
        )
        time.sleep(1)
    end_msg.markdown(f"<h1>お疲れさまでした</h1>", unsafe_allow_html=True)
    st.session_state.started = False
