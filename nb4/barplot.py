from datascience import *
import numpy as np
import pandas as pd

import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual, Output

from wordcloud import WordCloud as wc, STOPWORDS

import matplotlib.pyplot as plt
import seaborn as sns

cases = Table.read_table("../data/nb4/secretariat-cases.csv")
cases = cases.with_column("Municipality", [i.title() for i in cases["Municipality"]])
cases_df = cases.to_df()
options = cases_df.columns.delete(3)

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