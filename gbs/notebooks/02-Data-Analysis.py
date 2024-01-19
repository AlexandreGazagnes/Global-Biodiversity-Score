# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 02 - Data Analysis

# %% [markdown]
# Data Analysis on final DF

# %% [markdown]
# ## Preliminaires 

# %% [markdown]
# ### System 

# %%
# cd ../

# %%
pwd

# %% [markdown]
# ### Imports

# %%
import os, sys, logging
from IPython.display import display, HTML

# %%
import numpy as np
import pandas as pd

# %%
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import missingno as msno

# %%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# %%
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

# %% [markdown]
# ### Data

# %%
df = pd.read_csv("data/final/final.csv")

# %% [markdown]
# ## First Tour

# %% [markdown]
# ### Display

# %%
df.head()

# %%
df.tail()

# %%
df.sample(10)

# %% [markdown]
# ### Structure

# %%
df.shape

# %%
df.info()

# %%
df.dtypes

# %%
df.dtypes.value_counts()

# %%
df.nunique()

# %% [markdown]
# ### Missing Values

# %%
df

# %%
df.isna().sum(axis=1)

# %%
tmp = df.isna().sum(axis=1)
tmp[tmp == 0]

# %%
df = df.loc[tmp[tmp == 0].index]
df

# %% [markdown]
# ### Data Inspection

# %%
df.describe().round(4)

# %%
df = df.loc[df["country_name"] != "Malta", :]
df

# %% [markdown]
# ## EDA

# %% [markdown]
# ### Numercials

# %%
corr = df.select_dtypes(np.number).corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(
    corr, mask=mask, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f", annot=True
)

# %%
sns.pairplot(df, corner=True)

# %%
sns.pairplot(df, corner=True, hue="region")

# %%
for c in df.select_dtypes(np.number).columns:
    fig = px.box(df, x="region", y=c)
    fig.show()

# %% [markdown]
# ### Clustering

# %%
X_num = df.select_dtypes(np.number)
Xs = StandardScaler().fit_transform(X_num)
Xs = pd.DataFrame(Xs, columns=X_num.columns)
Xs.head()

# %%
score_list = []
for k in range(2, 10):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(Xs)
    labels = kmeans.predict(Xs)
    score_list.append(
        {
            "k": k,
            "interia": kmeans.inertia_,
            "bd": davies_bouldin_score(Xs, labels),
            "silhouette": silhouette_score(Xs, labels),
        }
    )

# %%
score_list = pd.DataFrame(score_list)
score_list

# %%
for kpi in score_list.columns.to_list()[1:]:
    fig = px.line(score_list, x="k", y=kpi, title=kpi)
    fig.show()

# %%
k = 6

kmeans = KMeans(n_clusters=k)
kmeans.fit(Xs)
labels = kmeans.predict(Xs)
df["cluster"] = labels
df.cluster = df.cluster.apply(lambda x: f"c_{x}")
df

# %%
df.sort_values(by="cluster", inplace=True, ascending=True)

for label in df.cluster.unique().tolist():
    print(f"Cluster {label}")
    print("____________________")
    display(df.loc[df.cluster == label, :])
    display(df.loc[df.cluster == label, :].describe().round(4))

# %%
for col in df.select_dtypes(np.number).columns.to_list():
    fig = px.box(df, x="cluster", y=col, title=col)
    fig.show()

# %% [markdown]
# **[!!!]**
#
# Please not that Cluserting stability is not formally tested here. 
# We can asume that the clusters are **not** stable enough for our purpose.

# %% [markdown]
# ### Maps

# %%
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world.head()

# %%
eu_countries = df["country_code"].values.tolist()
eu = world[world["iso_a3"].isin(eu_countries)]
eu.head()

# %%
merged_data = eu.merge(df, left_on="iso_a3", right_on="country_code")
merged_data.head()

# %%
fig = px.choropleth(
    merged_data,
    geojson=merged_data.geometry,
    locations=merged_data.index,
    color="cluster",
    color_continuous_scale="Viridis",
    scope="europe",
    # labels={"your_GDP_column": "GDP"},
)
fig.show()

# %%
fig = px.choropleth(
    merged_data,
    geojson=merged_data.geometry,
    locations=merged_data.index,
    color="msa.km2",
    color_continuous_scale="Viridis",
    scope="europe",
    labels={"your_GDP_column": "GDP"},
)
fig.show()

# %%
