from datascience import *
import numpy as np
import pandas as pd

import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual, Output

from wordcloud import WordCloud as wc, STOPWORDS
from collections import Counter

import matplotlib.pyplot as plt
import seaborn as sns

cases = Table.read_table("../data/nb4/secretariat-cases.csv")
cases = cases.with_column("Municipality", [i.title() for i in cases["Municipality"]])
cases_df = cases.to_df()
family_violence = Table.read_table("../data/nb3/domestic_violence_colombia_police.csv")

municipalities = list(Counter(cases["Municipality"]).keys())
f_cities = list(Counter(family_violence['City']).keys())
f_city_options, mun_options = [], {}
for mun in municipalities:
    for city in f_cities:
        if mun in city or mun == city or mun == 'Suán' and city == 'Suan':
            f_city_options.append(city)
            mun_options[city] = mun

def run():
    new_time = pd.to_datetime(cases_df["Month/Year"], format="%y-%b")
    cases_df["M/Y Datetime"] = new_time

    # Extracting types of violence & plotting
    def append_col(keyword, df):
        df[f'{keyword} violence claim'] = ""
        arr = []
        for i in df.index:
            if keyword in df['Type of violence'][i]:
                arr.append(1)
            elif 'All of the above' in df['Type of violence'][i]:
                arr.append(1)
            else:
                arr.append(0)
        df[f'{keyword} violence claim'] = arr

    append_col("Psychological", cases_df)
    append_col("Physical", cases_df)
    append_col("Sexual", cases_df)
    append_col("Financial", cases_df)

    datetime_cases = cases_df.groupby("M/Y Datetime").agg(sum).reset_index()

    fig1 = plt.figure(figsize=(15, 8))
    ax = fig1.add_subplot(1, 1, 1)
    sns.lineplot(data=datetime_cases, x="M/Y Datetime", y="Psychological violence claim", ax=ax, label='Psychological')
    sns.lineplot(data=datetime_cases, x="M/Y Datetime", y="Physical violence claim", ax=ax, label='Physical')
    sns.lineplot(data=datetime_cases, x="M/Y Datetime", y="Sexual violence claim", ax=ax, label='Sexual')
    sns.lineplot(data=datetime_cases, x="M/Y Datetime", y="Financial violence claim", ax=ax, label='Financial')

    plt.legend(title="Types of violence")
    plt.xlabel("Year-Month")
    plt.ylabel("Number of Ocurrences")
    plt.title("Change in Number of Assaults Reported (to Secretariat) from June 2017-June 2019 (by type");
    plt.show();

def run_two():
    def city_filter(city):
        city_table = family_violence.where("City", are.containing(city)).group(["Year", "Gender"], sum);
        city_table = city_table.where("Year", are.between_or_equal_to(2017, 2019))

        total_crimes_against_women = city_table.where("Gender", "Female")
        total_crimes_against_men = city_table.where("Gender", "Male");
        
        plt.figure(figsize=(11, 6))
        sns.lineplot("Year", "Total sum", data=total_crimes_against_women, color="m", label="Women")
        sns.lineplot("Year", "Total sum", data=total_crimes_against_men, color="k", label="Men")
        
        plt.xlabel("Year")
        plt.xticks([2017, 2018, 2019])
        plt.ylabel("Total Number of Crimes")
        plt.title(f'Change in the Number of Reported (to Police) Intrafamilial Crimes from 2015-2021 by Gender in {city}')
        plt.legend()
        plt.show()
        
        cases_df = cases.to_df()
        new_time = pd.to_datetime(cases_df["Month/Year"], format="%y-%b")
        cases_df["M/Y Datetime"] = new_time
        mun = mun_options[city]
        cases_df = cases_df[cases_df["Municipality"] == mun] 

        # Extracting types of violence & plotting
        def append_col(keyword, df):
            df[f'{keyword} violence claim'] = ""
            arr = []
            for i in df.index:
                if keyword in df['Type of violence'][i]: arr.append(1)
                elif 'All of the above' in df['Type of violence'][i]: arr.append(1)
                else: arr.append(0)
            df[f'{keyword} violence claim'] = arr

        append_col("Psychological", cases_df)
        append_col("Physical", cases_df)
        append_col("Sexual", cases_df)
        append_col("Financial", cases_df)

        datetime_cases = cases_df.groupby("M/Y Datetime").agg(sum).reset_index()

        fig1 = plt.figure(figsize=(11, 6))
        ax = fig1.add_subplot(1, 1, 1)
        sns.lineplot(data=datetime_cases, x="M/Y Datetime", y="Psychological violence claim", ax=ax, label='Psychological')
        sns.lineplot(data=datetime_cases, x="M/Y Datetime", y="Physical violence claim", ax=ax, label='Physical')
        sns.lineplot(data=datetime_cases, x="M/Y Datetime", y="Sexual violence claim", ax=ax, label='Sexual')
        sns.lineplot(data=datetime_cases, x="M/Y Datetime", y="Financial violence claim", ax=ax, label='Financial')

        plt.legend(title="Types of violence")
        plt.xlabel("Year-Month")
        plt.ylabel("Number of Ocurrences")
        plt.title(f"Change in Number of Assaults in {city} Reported (to Secretariat) from June 2017-June 2019 (by type)")



    city_dropdown = widgets.Dropdown(
        options = f_city_options,
        value = f_city_options[0],
        description = "City:"
    )


    interact(city_filter, city = city_dropdown);