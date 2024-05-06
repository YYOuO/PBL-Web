import pygsheets
import pandas as pd


class DataProcessing:
    def __init__(self):
        self.url = "https://docs.google.com/spreadsheets/d/1JLw1k_IuHSJHRqAhb1iGBz71NolPH_Z24BoRMCqqlVE/"
        gc = pygsheets.authorize(service_account_file="./auth.json")
        sheet = gc.open_by_url(self.url)
        self.worksheet = sheet.worksheet_by_title("5月")
        self.df_batter = (
            pd.DataFrame(
                self.worksheet.range("A1:M12", returnas="matrix")[1:],
                columns=self.worksheet.range("A1:M12", returnas="matrix")[0],
            )
            .fillna(0)
            .replace("", 0)
        )
        self.df_pitcher = (
            pd.DataFrame(
                self.worksheet.range("W1:AG12", returnas="matrix")[1:],
                columns=self.worksheet.range("W1:AG12", returnas="matrix")[0],
            )
            .fillna(0)
            .replace("", 0)
        )
        self.df_pitcher = self.df_pitcher.apply(pd.to_numeric, errors="ignore")
        self.df_batter = self.df_batter.apply(pd.to_numeric, errors="ignore")
        self.df_list = {"pitcher": self.df_pitcher, "batter": self.df_batter}

    def update(self, data: dict, typee: str):
        name = data["名字"]
        dfff = self.df_list[typee]
        index = dfff.index[dfff["名字"] == name]
        dfff["局數"] = dfff["局數"].astype(float)
        dfff.iloc[index] += pd.Series(data)
        dfff.loc[index, "名字"] = data["名字"]
        print(dfff.iloc[index])
        if typee == "batter":
            self.worksheet.set_dataframe(dfff, "A1")
        elif typee == "pitcher":
            self.worksheet.set_dataframe(dfff, "W1")

    def get_users(self):
        user_list = self.df_pitcher["名字"].to_list()
        return user_list[1:]
