import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk


df = pd.read_csv("survey_results_public.csv")
columns = ['MainBranch', 'Age', 'Employment', 'RemoteWork', 'EdLevel', 
           'ConvertedCompYearly', 'JobSat', 'Country']
df_clean = df[columns].copy()
df_clean.dropna(subset=['Employment', 'RemoteWork', 'ConvertedCompYearly', 'JobSat'], inplace=True)
df_clean['ConvertedCompYearly'] = pd.to_numeric(df_clean['ConvertedCompYearly'], errors='coerce')
df_clean = df_clean[(df_clean['ConvertedCompYearly'] > 1000) & (df_clean['ConvertedCompYearly'] < 500000)]

def show_histogram():
    plt.figure(figsize=(8,5))
    plt.hist(df_clean['ConvertedCompYearly'], bins=40, color='skyblue', edgecolor='black')
    plt.title("Histogram of Yearly Compensation")
    plt.xlabel("Salary")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

def show_boxplot():
    plt.figure(figsize=(10,6))
    sns.boxplot(data=df_clean, x='Employment', y='ConvertedCompYearly')
    plt.yscale('log')
    plt.title("Box Plot: Salary by Employment Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_scatter():
    top_countries = df_clean['Country'].value_counts().index[:5]
    df_scatter = df_clean[df_clean['Country'].isin(top_countries)]
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=df_scatter, x='Country', y='ConvertedCompYearly', alpha=0.6)
    plt.title("Scatter Plot: Salary vs Country")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_donut():
    remote_counts = df_clean['RemoteWork'].value_counts()
    plt.figure(figsize=(6,6))
    plt.pie(remote_counts, labels=remote_counts.index, autopct='%1.1f%%', startangle=140, wedgeprops={'width': 0.4})
    plt.title("Donut Chart: Remote Work Distribution")
    plt.tight_layout()
    plt.show()

def show_bar():
    salary_by_job_sat = df_clean.groupby('JobSat')['ConvertedCompYearly'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10,5))
    salary_by_job_sat.plot(kind='bar', color='orange')
    plt.title("Bar Chart: Avg Salary by Job Satisfaction")
    plt.ylabel("Avg Salary")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_heatmap():
    df_corr = df_clean[['ConvertedCompYearly']].copy()
    df_corr['Age_num'] = df_clean['Age'].astype('category').cat.codes
    plt.figure(figsize=(6,4))
    sns.heatmap(df_corr.corr(), annot=True, cmap='coolwarm')
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()

root = tk.Tk()
root.title("Interactive Survey Graphs")
root.geometry("500x450")
root.configure(bg='#f4f4f9')

tk.Label(root, text="Select Graph Type", font=('Helvetica', 18, 'bold'), bg='#f4f4f9').pack(pady=20)


options = [
    "Histogram", "Box Plot", "Scatter Plot", "Donut Chart",
    "Bar Chart", "Heatmap"
]
combo = ttk.Combobox(root, values=options, font=('Helvetica', 12), width=20)
combo.pack(pady=10)

tk.Button(root, text="Generate Graph", font=('Helvetica', 12, 'bold'), bg='#4CAF50', fg='white', 
          activebackground='#45a049', relief='raised', command=lambda: generate_graph(combo.get())).pack(pady=20)

def generate_graph(choice):
    if choice == "Histogram":
        show_histogram()
    elif choice == "Box Plot":
        show_boxplot()
    elif choice == "Scatter Plot":
        show_scatter()
    elif choice == "Donut Chart":
        show_donut()
    elif choice == "Bar Chart":
        show_bar()
    elif choice == "Heatmap":
        show_heatmap()

root.mainloop()

