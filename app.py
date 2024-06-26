from flask import Flask, render_template, request, redirect

from sheet import DataProcessing

app = Flask(__name__)


dp = DataProcessing()


@app.route("/")
def index():
    return redirect("/pitcher")


@app.route("/pitcher", methods=["POST", "GET"])
def pitcher():
    global dp
    home = request.values.get("home", default=1)
    away = request.values.get("away", default=1)
    user_list = dp.get_users()
    return render_template(
        "pitcher.html", user_list=user_list, home=int(home), away=int(away)
    )


@app.route("/batter", methods=["POST", "GET"])
def batter():
    global dp
    home = request.values.get("home", default=1)
    away = request.values.get("away", default=1)
    user_list = dp.get_users()
    return render_template(
        "batter.html", user_list=user_list, home=int(home), away=int(away)
    )


@app.route("/submit", methods=["POST"])
def update():
    form_data = request.form
    typee = request.headers.get("Referer").split("/")[-1]
    number = int(form_data.get("total", default=2))
    data_dict = {}
    dp = DataProcessing()
    for i in range(1, number + 1):
        if typee == "pitcher":
            data_dict = {
                "名字": form_data.get(f"name_{i}"),
                "局數": float(form_data.get(f"Innings_{i}")),
                "失分": int(form_data.get(f"Run_{i}")),
                "被安打": int(form_data.get(f"Hit_{i}")),
                "被全壘打": int(form_data.get(f"HomeRun_{i}")),
                "三振": int(form_data.get(f"StrikeOut_{i}")),
                "四死": int(form_data.get(f"BaseOnBalls_{i}")),
                # "勝": int(form_data.get(f"Win_{i}")),
                # "敗": int(form_data.get(f"Lose_{i}")),
                # "中繼成功": int(form_data.get(f"Hold_{i}")),
                # "救援成功": int(form_data.get(f"Save_{i}")),
            }
            status = str(form_data.get(f"status_{i}"))
            if status == "Win":
                data_dict.update(
                    {
                        "勝": 1,
                        "敗": 0,
                        "中繼成功": 0,
                        "救援成功": 0,
                    }
                )
            elif status == "Lose":
                data_dict.update(
                    {
                        "勝": 0,
                        "敗": 1,
                        "中繼成功": 0,
                        "救援成功": 0,
                    }
                )
            elif status == "Hold":
                data_dict.update(
                    {
                        "勝": 0,
                        "敗": 0,
                        "中繼成功": 1,
                        "救援成功": 0,
                    }
                )
            elif status == "Save":
                data_dict.update(
                    {
                        "勝": 0,
                        "敗": 0,
                        "中繼成功": 0,
                        "救援成功": 1,
                    }
                )
            else:
                data_dict.update(
                    {
                        "勝": 0,
                        "敗": 0,
                        "中繼成功": 0,
                        "救援成功": 0,
                    }
                )
        elif typee == "batter":
            HIT = (
                int(form_data.get(f"Single_{i}"))
                + int(form_data.get(f"Double_{i}"))
                + int(form_data.get(f"Triple_{i}"))
                + int(form_data.get(f"Homerun_{i}"))
            )
            AB = (
                HIT
                + +int(form_data.get(f"StrikeOut_{i}"))
                + int(form_data.get(f"GO_{i}"))
                + int(form_data.get(f"FO_{i}"))
            )
            PA = AB + int(form_data.get(f"BaseOnBalls_{i}"))
            data_dict = {
                "名字": form_data.get(f"name_{i}"),
                "打席": PA,
                "打數": AB,
                "安打": HIT,
                "滾地出局": int(form_data.get(f"GO_{i}")),
                "飛球出局": int(form_data.get(f"FO_{i}")),
                "被三振": int(form_data.get(f"StrikeOut_{i}")),
                "四死": int(form_data.get(f"BaseOnBalls_{i}")),
                "打點": int(form_data.get(f"RBI_{i}")),
                "一壘安打": int(form_data.get(f"Single_{i}")),
                "二壘安打": int(form_data.get(f"Double_{i}")),
                "三壘安打": int(form_data.get(f"Triple_{i}")),
                "全壘打": int(form_data.get(f"Homerun_{i}")),
            }
        dp.update(data_dict, typee)
    return f"<h2>Success</h2> <a href='/{typee}'>Back</a> update:{number}"


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html", error=error), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
