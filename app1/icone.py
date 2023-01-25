import pandas as pd

def atribui_icone(df):

    icone_url_1 = "https://upload.wikimedia.org/wikipedia/commons/b/be/Farm-Fresh_car.png"
    icone_1 = {

        "url": icone_url_1,
        "width": 242,
        "height": 242,
        "anchorY": 242,
    }

    icone_url_2 = "https://upload.wikimedia.org/wikipedia/commons/c/cc/Farm-Fresh_car_add.png"
    icone_2 = {

        "url": icone_url_2,
        "width": 242,
        "height": 242,
        "anchorY": 242,
    }

    icone_url_3 = "https://upload.wikimedia.org/wikipedia/commons/0/09/Farm-Fresh_car_delete.png"
    icone_3 = {

        "url": icone_url_3,
        "width": 242,
        "height": 242,
        "anchorY": 242,
    }

    icone_url_4 = "https://upload.wikimedia.org/wikipedia/commons/8/8e/Farm-Fresh_autos.png"
    icone_4 = {

        "url": icone_url_4,
        "width": 242,
        "height": 242,
        "anchorY": 242,
    }

    icone_url_5 = "https://upload.wikimedia.org/wikipedia/commons/e/ec/Farm-Fresh_emotion_dead.png"
    icone_5 = {

        "url": icone_url_5,
        "width": 242,
        "height": 242,
        "anchorY": 242,
    }

    icone_url_6 = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Question_mark_white.png/120px-Question_mark_white.png"
    icone_6 = {

        "url": icone_url_6,
        "width": 242,
        "height": 242,
        "anchorY": 242,
    }

    df["icone"] = None
    i = 0
    while i < len(df):
    #for i in df.index:
        if df['most_severe_injury'][i] == 'NO INDICATION OF INJURY':
            df["icone"][i] = icone_1
        elif df['most_severe_injury'][i] == 'NONINCAPACITATING INJURY':
            df["icone"][i] = icone_2
        elif df['most_severe_injury'][i] == 'REPORTED, NOT EVIDENT':
            df["icone"][i] = icone_3
        elif df['most_severe_injury'][i] == 'INCAPACITATING INJURY':
            df["icone"][i] = icone_4
        elif df['most_severe_injury'][i] == 'FATAL':
            df["icone"][i] = icone_5
        else:
            df["icone"][i] = icone_6
        i += 1
    return df

