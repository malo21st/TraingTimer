import streamlit as st
import time

# Data
plan_data = [
{
    "name": "かかと",
    "sets": 10,
    "start_count": 5,
    "plan": [
        {
            "text": "かかと上げて！",
            "time": 1,
            "count": 0,
        },
        {
            "text": "キープ！",
            "time": 3,
            "count": -1,
        },
        {
            "text": "下げて",
            "time": 1,
            "count": 0,
        },
    ],
},
{
    "name": "かたあし",
    "sets": 5,
    "start_count": 5,
    "plan": [
        {
            "text": "右足上げて！",
            "time": 1,
            "count": 0,
        },
        {
            "text": "キープ！",
            "time": 60,
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
            "time": 60,
            "count": -1,
        },
        {
            "text": "下げて",
            "time": 1,
            "count": 0,
        },
    ],
}
]

def make_plan(plan_dic):
    plan = []
    for training in plan_dic:
        name = training["name"]      
        for num in range(training["start_count"], -1, -1):
            plan.append(["カウントダウン", num, 0, name])
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

plan = make_plan(plan_data)

# Streamlit
## View
if "started" not in st.session_state:
    st.session_state.started = False
if st.button("スタート"):
    st.session_state.started = True

main_msg = st.empty()

## Logic
counter = 0
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
        counter += 1
    end_msg.markdown(f"<h1>お疲れさまでした</h1>", unsafe_allow_html=True)
    st.session_state.started = False
