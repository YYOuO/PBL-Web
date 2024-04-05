import pygsheets
import pandas as pd


class DataProcessing:
    def __init__(self):
        self.url = "https://docs.google.com/spreadsheets/d/1JLw1k_IuHSJHRqAhb1iGBz71NolPH_Z24BoRMCqqlVE/"
        gc = pygsheets.authorize(service_account_file="./auth.json")
        sheet = gc.open_by_url(
            "https://docs.google.com/spreadsheets/d/1JLw1k_IuHSJHRqAhb1iGBz71NolPH_Z24BoRMCqqlVE/"
        )
        self.worksheet = sheet.worksheet_by_title("借我用一下")
        self.df_batter = (
            pd.DataFrame(
                self.worksheet.range("A1:M11", returnas="matrix")[1:],
                columns=self.worksheet.range("A1:M11", returnas="matrix")[0],
            )
            .fillna(0)
            .replace("", 0)
        )
        self.df_pitcher = (
            pd.DataFrame(
                self.worksheet.range("A13:K23", returnas="matrix")[1:],
                columns=self.worksheet.range("A13:K23", returnas="matrix")[0],
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
        dfff.iloc[index] += pd.Series(data)
        dfff.loc[index, "名字"] = data["名字"]
        print(dfff.iloc[index])
        if typee == "batter":
            self.worksheet.set_dataframe(dfff, "A1")
        elif typee == "pitcher":
            self.worksheet.set_dataframe(dfff, "A13")