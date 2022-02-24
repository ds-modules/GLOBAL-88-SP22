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

def barplot():
    def variable_filter(variable):
        plt.figure(figsize=(9, 5))
        
        if (variable == options[0]):
            date = cases.group("Month/Year")
            plt.xticks(rotation=45)
            sns.barplot(y=date.column(0), x=date.column(1), orientation="horizontal");
            plt.xlabel("Number of Ocurrences")
            plt.ylabel("Month/Year")
        
        elif (variable == options[1]):
            victim = cases.group("Victim of the conflict?")
            sns.barplot(x=victim.column(0), y=victim.column(1));
            plt.ylabel("Number of Ocurrences")
            plt.xlabel("Victim of the conflict?")
            
        elif (variable == options[2]):
            municipality = cases.group("Municipality")
            plt.xticks(rotation=45)
            sns.barplot(y=municipality.column(0), x=municipality.column(1), orientation="horizontal");
            plt.xlabel("Number of Ocurrences")
            plt.ylabel("Municipality")
            
        elif (variable == options[3]):
            complaint = cases.group("Previous complaints?")
            sns.barplot(x=complaint.column(0), y=complaint.column(1));
            plt.ylabel("Number of Ocurrences")
            plt.xlabel("Previous complaints?")
            
        elif (variable == options[4]):
            setting = cases.group("Violence setting")
            sns.barplot(x=setting.column(0), y=setting.column(1));
            plt.ylabel("Number of Ocurrences")    
            plt.xlabel("Violence setting?")
            
        elif (variable == options[5]):
            violence_type = cases.group("Type of violence")
            plt.xticks(rotation=45)
            sns.barplot(y=violence_type.column(0), x=violence_type.column(1), orientation="horizontal");
            plt.xlabel("Number of Ocurrences")
            plt.ylabel("Type of Violence")
            
        elif (variable == options[6]):
            referral = cases.group("Referral")
            plt.xticks(rotation=45)
            sns.barplot(y=referral.column(0), x=referral.column(1), orientation="horizontal");
            plt.xlabel("Number of Ocurrences")
            plt.ylabel("Referral")
            
        elif (variable == options[7]):
            entity = cases.group("Entity referred to")
            plt.xticks(rotation=45)
            sns.barplot(y=entity.column(0), x=entity.column(1), orientation='horizontal');
            plt.xlabel("Number of Ocurrences")
            plt.ylabel("Entity referred to")
    
    barplot_output = widgets.Output()        
    options = cases_df.columns.delete(3)
    variable_dropdown = widgets.Dropdown(options = options, description = "Variable:");

    interact(variable_filter, variable = variable_dropdown)

    plt.show(); 

def lineplot():
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
    plt.title("Change in Number of Assaults Reported (to Secretariat) from June 2017-June 2019 (by type)");
    plt.show();

def comparable_lineplot():
    municipalities = list(Counter(cases["Municipality"]).keys())
    f_cities = list(Counter(family_violence['City']).keys())
    f_city_options, mun_options = [], {}
    for mun in municipalities:
        for city in f_cities:
            if mun in city or mun == city or mun == 'Suán' and city == 'Suan':
                f_city_options.append(city)
                mun_options[city] = mun

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

def wordcloud():
    text = ''
    stopwords = set(STOPWORDS)

    for word in cases.column("Reason for Consultation"):
        tokens = word.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
            text += " ".join(tokens)+" "


    wordcloud = wc(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    min_font_size = 5).generate(text.lower())
                    
    plt.figure(figsize = (10, 10), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")

    plt.show()