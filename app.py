import streamlit as st
import time
import ast
from itertools import product
from PIL import Image
import functools
import ex_data

# Initialize & Setting
## Session State
if "started" not in st.session_state:
    st.session_state.started = False
## Excercise Data & Template
ex_data_list = ex_data.ex_data_list
tmpl_msg = ex_data.tmpl_msg

# Function
def make_exercise_list(training_plan, image_list):
    """
    「トレーニング計画」を元に「トレーニング指示リスト」を作成
    """
    ex_lst = []
    for training, image in zip(training_plan, image_list):
        name = training["name"]      
        sets_def = training["sets"]
        for num in range(training["start_count"], -1, -1):
            ex_lst.append(["運動開始まで", num, 0, name, image, sets_def])
            
        for sets_num, plan in product(range(1, training["sets"] + 1), training["plan"]):
            for count in range(plan["time"] + 1):
                if plan["count"] == 1:
                    ex_lst.append([plan["text"], count, sets_num, name, image, sets_def])
                elif plan["count"] == -1:
                    start_count = plan["time"]
                    ex_lst.append([plan["text"], start_count - count, sets_num, name, image, sets_def])
                else:
                    ex_lst.append([plan["text"], "　", sets_num, name, image, sets_def])
    
    ex_lst.append(["　", "　", "", "お疲れさまでした", "", ""])
    return ex_lst

@functools.cache
def chache_image(img_path):
    return Image.open(img_path)

# Streamlit
## Sidebar
with st.sidebar:
    params_lst = list()
    for ex in ex_data_list:
        ui = ex["ui"]
        will_exercise = st.checkbox(f"**{ui['name']}**", value=ui["available"], key=ui["name"])
        with st.expander("運動強度の変更", expanded=False):
            sets_num = st.number_input(f"セット数（回）[ {ui['sets_min']} ~ {ui['sets_max']} ]",
                                        min_value=ui['sets_min'], max_value=ui['sets_max'], value=ui['sets_def'],
                                        step=ui['sets_step'], key=f"{ui['name']}_sets")
            keep_num = st.number_input(f"キープ時間（秒） [ {ui['keep_min']} ~ {ui['keep_max']} ]",
                                        min_value=ui['keep_min'], max_value=ui['keep_max'], value=ui['keep_def'],
                                        step=ui['keep_step'], key=f"{ui['name']}_keep")
        params_lst.append({"will_exercise": will_exercise, "sets": sets_num, "keep": keep_num})
        st.write("")
    st.markdown("---")
    st.button("やりなおし", key="again", on_click=lambda: st.session_state.clear())

## Main
### Layout
main_msg = st.empty()
main_btn = st.empty()
main_img = st.empty()

### Start
main_msg.markdown("<h1 style='color: lightblue;'>運動しましょう</h1><br><br>",
                  unsafe_allow_html=True)
if main_btn.button("**はじめる**"):
    st.session_state.started = True
main_img.empty() # 画像を消す

### Operation
if st.session_state.started:
    # トレーニング計画
    training_plan = [] # トレーニング計画（JSON風）
    image_list = [] # 画像リスト
    for prm, ex in zip(params_lst, ex_data_list):
        if prm["will_exercise"]:
            training_plan.append(ast.literal_eval(
                ex["template"].substitute(sets_num=prm["sets"], keep_num=prm["keep"])
            ))
            image_list.append(ex["ui"].get("image", False))
    exercise_list = make_exercise_list(training_plan, image_list) # 「トレーニング指示リスト」作成

    # トレーニング開始
    st.session_state.started = False
    main_btn.empty() # ボタンを消す
    for exercise in exercise_list: # 「トレーニング指示リスト」に従い表示
        text, count, sets, name, image, sets_def = exercise
        main_msg.markdown(
            tmpl_msg.substitute(text=text, count=count, sets=sets, name=name, sets_def=sets_def),
            unsafe_allow_html=True
        )
        if image:
            img_path = f"static/{image}" # static/{image}
            img = chache_image(img_path) # 画像をキャッシュ
            main_img.image(img, width=200)
        else:
            main_img.empty() # 画像を消す

        time.sleep(1)
