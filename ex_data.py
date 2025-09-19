import string

# かかと上げ下ろし
_tmpl_ex0 = string.Template("""
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
            "time": ${keep_num},
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

# 片足立ち
_tmpl_ex1 = string.Template("""
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
            "text": "キープ！（右足上げ）",
            "time": ${keep_num},
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
            "text": "キープ！（左足上げ）",
            "time": ${keep_num},
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

# スクワット
_tmpl_ex2 = string.Template("""
{
    "name": "スクワット",
    "sets": ${sets_num},
    "start_count": 5,
    "plan": [
        {
            "text": "腰をゆっくり下げて！",
            "time": 3,
            "count": 0,
        },
        {
            "text": "キープ！",
            "time": ${keep_num},
            "count": -1,
        },
        {
            "text": "ゆっくり上げて",
            "time": 2,
            "count": 0,
        },
        {
            "text": "ひざは伸ばさない",
            "time": 1,
            "count": 0,
        },
    ],
}
""")

_ui_ex0 = {
    "name": "かかと上げ下ろし",
    "available": True,
    "sets_def": 10,
    "sets_min": 5,
    "sets_max": 50,
    "sets_step": 5,
    "keep_def": 10,
    "keep_min": 5,
    "keep_max": 60,
    "keep_step": 5,
    "image": "00_tsumasaki_small.png",
}

_ui_ex1 = {
    "name": "片足立ち",
    "available": True,
    "sets_def": 5,
    "sets_min": 5,
    "sets_max": 50,
    "sets_step": 5,
    "keep_def": 60,
    "keep_min": 30,
    "keep_max": 180,
    "keep_step": 30,
    "image": "01_kataashi_small.png",
}

_ui_ex2 = {
    "name": "スクワット",
    "available": True,
    "sets_def": 10,
    "sets_min": 5,
    "sets_max": 50,
    "sets_step": 5,
    "keep_def": 3,
    "keep_min": 3,
    "keep_max": 15,
    "keep_step": 3,
    "image": "02_squat_small.png",
}

# 運動データリスト
ex_data_list = [
    {"template": _tmpl_ex0, "ui": _ui_ex0,},
    {"template": _tmpl_ex1, "ui": _ui_ex1,},
    {"template": _tmpl_ex2, "ui": _ui_ex2,},
]

# メイン画面　メッセージ
tmpl_msg = string.Template("""
<div style='text-align: center;'>
    <h1 style='color: red;'>${text}</h1>
    <span style='font-size: 72px; color: lightgreen;'>${count}</span>
    <h1 style='color: lightblue;'>${name}　${sets} / ${sets_def}</h1>
</div>
""")
