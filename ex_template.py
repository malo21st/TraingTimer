import string

# かかと上げ下ろし
tmpl_ex0 = string.Template("""
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

# 片足立ち
tmpl_ex1 = string.Template("""
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

# メイン画面　メッセージ
tmpl_msg = string.Template("""
<h1 style='color: red;'>${text}</h1>
<div style='text-align: center;'>
    <span style='font-size: 72px; color: lightgreen;'>${count}</span>
</div>
<h1 style='color: lightblue;'>${name}　${sets}</h1>
""")
