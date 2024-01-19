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
# # 01 - First Exploration

# %% [markdown]
# First exploration of the data.

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

from dataclasses import dataclass

# %%
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
# from gbs.etl.extract import Extract

# %% [markdown]
# ### Data

# %%
# !tree -L 1 ./

# %%
# !tree -L 3 data/

# %%
data_dir = "./data/source/"

# %%
crops = pd.read_csv(os.path.join(data_dir, "crops/crops.csv"))
crops.head()

# %%
country_specs = pd.read_csv(
    os.path.join(data_dir, "country_specs/country_specs.csv")
)
country_specs.head()

# %%
_path = "./data/source/production/"

fn_list = [
    os.path.join(_path, f) for f in os.listdir(_path) if f.endswith(".csv")
]
fn_list


# %%
@dataclass
class Production:
    """Production data for a crop in a country in a year"""

    areacodes = pd.read_csv(
        os.path.join(_path, "production_crops_livestock_e_areacodes.csv"),
    )
    data_normalized = pd.read_csv(os.path.join(_path, "data_normalized.csv"))
    flags = pd.read_csv(
        os.path.join(_path, "production_crops_livestock_e_flags.csv"),
    )
    itemcodes = pd.read_csv(
        os.path.join(_path, "production_crops_livestock_e_itemcodes.csv"),
    )


# %% [markdown]
# ## Exploration 

# %% [markdown]
# ### Country Specs 

# %% [markdown]
# #### Display

# %%
country_specs.head(10)

# %%
country_specs.tail(10)

# %%
country_specs.sample(10)

# %% [markdown]
# #### Structure

# %%
country_specs.shape

# %%
country_specs.columns

# %%
country_specs.dtypes

# %%
country_specs.info()

# %%
crops.dtypes.value_counts()

# %%
for dtype in ["object", "float", "int"]:
    selected_dtype = country_specs.select_dtypes(include=[dtype])
    display(selected_dtype.columns)

# %%
_num = country_specs.select_dtypes(include=["number"])
_num

# %%
_num_cols = _num.columns.tolist()
[i for i in _num_cols if ("code" not in i) and ("id" not in i)]

# %% [markdown]
# #### Nan

# %%
crops.isna().sum()

# %%
tmp = crops.isna().mean().round(2)
tmp[tmp > 0.00]

# %%
len(tmp[tmp > 0.00]) / len(tmp)

# %%
tmp = crops.isna().mean(axis=1).round(2)
tmp.value_counts().sort_index()

# %%
msno.matrix(country_specs)

# %% [markdown]
# **Conclusion**
#
# - delete is_EU27 and is_south_america

# %%
drop_cols = ["is_EU27", "is_south_america"]
country_specs = country_specs.drop(columns=drop_cols)
msno.matrix(country_specs)

# %%
tmp = country_specs.isna().mean(axis=1).round(2)
tmp.value_counts().sort_index()

# %%
threshold = 0.2
tmp[tmp >= threshold]

# %%
drop_idxs = tmp[tmp > threshold].index
country_specs.loc[drop_idxs, :]

# %% [markdown]
# **Conclusion**
#
# - countries with Nan rate > 0.3 are Island or -100k pop (Monaco, Antigua)

# %%
country_specs = country_specs.drop(
    index=drop_idxs, columns=drop_cols, errors="ignore"
)
msno.matrix(country_specs)

# %%
num_cols = country_specs.select_dtypes(
    include=["float", "int"]
).columns.tolist()

num_cols = [i for i in num_cols if "code" not in i]

categ_cols = [
    "alpha_3_code",
    "FAO_country_name",
    "exiobase_region_name",
    "globio_country_code",
    "globio_country_name",
    "USS30_region_name",
]


country_specs = country_specs.loc[:, num_cols + categ_cols]

# %%
country_specs

# %% [markdown]
# #### Data Inspection

# %%
country_specs.FAO_country_name.value_counts()

# %%
country_specs.FAO_country_name.nunique()

# %%
country_specs.USS30_region_name.value_counts()

# %%
country_specs.FAO_country_name.value_counts().value_counts()

# %%
country_specs.groupby("exiobase_region_name").FAO_country_name.count()

# %% [markdown]
# ### Crops 

# %% [markdown]
# #### Wheat Selection

# %%
feature = "Wheat"
crops = crops.loc[crops.item_name == feature, :]
crops.head()

# %%
item_cols = [i for i in crops.columns if "item" in i]
item_cols

# %%
crops.drop(columns=item_cols, inplace=True, errors="ignore")
crops.head()

# %% [markdown]
# #### Display

# %%
crops.head(10)

# %%
crops.tail(10)

# %%
crops.sample(10)

# %% [markdown]
# #### Structure

# %%
crops.drop(columns="id", inplace=True, errors="ignore")

# %%
crops.shape

# %%
crops.columns

# %%
crops.dtypes

# %%
crops.info()

# %%
crops.dtypes.value_counts()

# %%
for dtype in ["object", "float", "int"]:
    selected_dtype = crops.select_dtypes(include=[dtype])
    display(selected_dtype.columns)

# %%
_num = crops.select_dtypes(include=["number"])
_num

# %%
_feat_cols = [i for i in _num.columns if "msa" in i]
_feat_cols

# %% [markdown]
# #### Separation Static/Dynamic

# %%
categ_cols = [i for i in crops.columns if "msa" not in i]
static_cols = [i for i in crops.columns if "static" in i]
dynamic_cols = [i for i in crops.columns if "dynamic" in i]

display(categ_cols)
display(static_cols)
display(dynamic_cols)

# %%
crops_static = crops.loc[:, categ_cols + static_cols]
crops_static.head()

# %%
crops_dynamic = crops.loc[:, categ_cols + dynamic_cols]
crops_dynamic

# %% [markdown]
# ##### [ !!! ]
# In the report we do have the separation between : 
# - terestrial static, 
# - terestrial dynamic 
# - aquatic static

# %% [markdown]
# #### Summize

# %% [markdown]
# crops_static

# %%
crops_static

# %%
sum_static = crops_static.iloc[:, 1:].sum(axis=1)
sum_static

# %%
crops_static = crops_static.iloc[:, :1]
crops_static["sum_static"] = sum_static.values

# %% [markdown]
# #### Data Inspection

# %%
crops_static.describe()

# %%
crops.globio_country_code.value_counts()

# %%
crops.globio_country_code.nunique()

# %% [markdown]
# #### Merge Country Specs and crops

# %%
country_specs

# %%
tmp = country_specs.loc[:, ["globio_country_code", "globio_country_name"]]
tmp.index = tmp.globio_country_code
tmp.drop(columns="globio_country_code", inplace=True)
tmp.index.name = None
tmp = tmp.to_dict().get("globio_country_name")
tmp

# %%
crops_static["globio_country_name"] = crops_static.globio_country_code.apply(
    lambda i: tmp.get(i, np.nan)
)
crops_static

# %% [markdown]
# #### Nan

# %%
crops_static.isna().sum()

# %% [markdown]
# ### Production

# %% [markdown]
# #### Table Analysis

# %%
Production.areacodes

# %%
Production.flags

# %%
flags = {
    k: v
    for k, v in zip(
        Production.flags.Flag.values, Production.flags.Description.values
    )
}
flags

# %%
Production.itemcodes

# %%
data = Production.data_normalized
data

# %%
data["Flag_value"] = data.Flag.apply(lambda i: flags[i])
data

# %%
data.columns

# %% [markdown]
# #### Feature selection

# %%
cols = [
    # "Area Code",
    # "Area Code (M49)",
    "Area",
    # "Item Code",
    # "Item Code (CPC)",
    "Item",
    # "Element Code",
    "Element",
    # "Year Code",
    "Year",
    "Unit",
    "Value",
    # "Flag",
    # "Note",
    "Flag_value",
]

# %%
data = data.loc[:, cols]
data

# %%
data.Element.nunique()

# %%
data.Element.value_counts()

# %%
data.Item.value_counts()

# %%
data_weat = data.loc[data.Item.str.lower().str.contains("wheat"), :]
data_weat

# %%
data_weat_2019 = data_weat.loc[data_weat.Year == 2019, :]
data_weat_2019

# %%
data_weat_2019_h = data_weat_2019.loc[data_weat_2019.Unit == "ha", :]

# %%
data_weat_2019_h

# %%
data_weat_2019_h.columns

# %%
cols = [
    "Area",
    # "Item",
    # "Element",
    # "Year",
    # "Unit",
    "Value",
    "Flag_value",
]

data_weat_2019_h = data_weat_2019_h.loc[:, cols]
data_weat_2019_h

# %% [markdown]
# #### Display 

# %%
data_weat_2019_h.head(10)

# %%
data_weat_2019_h.tail(10)

# %%
data_weat_2019_h.sample(10)

# %% [markdown]
# #### Structure

# %%
data_weat_2019_h.shape

# %%
data_weat_2019_h.info()

# %% [markdown]
# #### Nan

# %%
data_weat_2019_h.isna().sum()

# %% [markdown]
# ## Final Merge

# %% [markdown]
# ### Keys Analysis

# %%
data_weat_2019_h.sort_values("Area", inplace=True, ascending=True)
data_weat_2019_h.rename(
    columns={"Value": "km2"}, inplace=True, errors="ignore"
)
data_weat_2019_h

# %% [markdown]
# ##### [!!!] 
# > BE CARREFULLL KM2 is supposed and not checked ! 

# %%
crops_static.sort_values("globio_country_name", ascending=True, inplace=True)
crops_static.head()

# %%
country_specs.sort_values("FAO_country_name", ascending=True, inplace=True)
country_specs

# %%
crops_static.shape

# %%
data_weat_2019_h.shape

# %%
country_specs.shape

# %% [markdown]
# ### Data vs country

# %%
merge1 = pd.merge(
    left=country_specs,
    right=data_weat_2019_h,
    left_on="FAO_country_name",
    right_on="Area",
    how="outer",
    indicator=True,
)

merge1

# %%
merge1.rename(columns={"_merge": "_merge_1"}, inplace=True)
merge1

# %% [markdown]
# ### Merge1 v crops 

# %%
merge2 = pd.merge(
    left=merge1,
    right=crops_static,
    left_on="globio_country_name",
    right_on="globio_country_name",
    how="outer",
    indicator=True,
)

merge2

# %%
merge2.rename(columns={"_merge": "_merge_2"}, inplace=True)
merge2

# %%
merge2.loc[merge2.loc[:, "_merge_2"] == "both", :].head()

# %%
merge2.loc[merge2.loc[:, "_merge_2"] == "both", :].head()

# %%
final = merge2.loc[merge2.loc[:, "_merge_2"] == "both", :]

# %% [markdown]
# ### Select Features 

# %%
final.head()

# %%
final.columns

# %%
cols = [
    # "exiobase_region_id",
    "alpha_3_code",
    "FAO_country_name",
    # "exiobase_region_name",
    # "globio_country_code_x",
    "globio_country_name",
    "USS30_region_name",
    "Area",
    "km2",
    "Flag_value",
    # "_merge_1",
    # "globio_country_code_y",
    "sum_static",
    # "_merge_2",
]

# %%
final = final.loc[:, cols]
final.head()

# %%
final["msa.km2"] = final.km2 * final.sum_static
final.head()

# %% [markdown]
# ## Feature Engineering

# %% [markdown]
# ### Population

# %%
fn = "./data/source/population/API_SP.POP.TOTL_DS2_en_csv_v2_6298256.csv"

# %%
pop = pd.read_csv(fn)
pop.head()

# %%
pop = pop.loc[:, pop.columns.tolist()[:2] + ["2019"]]
pop.head()

# %%
pop.rename(columns={"2019": "population"}, inplace=True)
pop.head()

# %% [markdown]
# ### Gdp

# %%
fn = "./data/source/gdp/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_6298251.csv"

# %%
gdp = pd.read_csv(fn)
gdp.head()

# %%
gdp = gdp.loc[:, gdp.columns.tolist()[:2] + ["2019"]]
gdp

# %%
gdp.rename(columns={"2019": "gdp_per_capita"}, inplace=True)
gdp

# %% [markdown]
# ### Merge both

# %%
pop_gdp = pd.merge(
    left=pop, right=gdp, on=["Country Name", "Country Code"], how="outer"
)
pop_gdp

# %%
test_3_codes = ["AUT", "BEL, BGR"]

pop_gdp.loc[pop_gdp.loc[:, "Country Name"].str.contains("Bel"), :]

# %%
pop_gdp.loc[pop_gdp.loc[:, "Country Name"].str.contains("Bul"), :]

# %%
final_gdp_pop = pd.merge(
    left=final,
    right=pop_gdp,
    left_on="alpha_3_code",
    right_on="Country Code",
    how="left",
)
final_gdp_pop.head()

# %% [markdown]
# ### Final Selection

# %%
final_gdp_pop.columns

# %%
cols = [
    # "exiobase_region_id",
    # "alpha_3_code",
    # "FAO_country_name",
    # "exiobase_region_name",
    # "globio_country_code_x",
    # "globio_country_name",
    "USS30_region_name",
    # "Area",
    "km2",
    # "Flag_value",
    # "_merge_1",
    # "globio_country_code_y",
    "sum_static",
    # "_merge_2",
    "msa.km2",
    "Country Name",
    "Country Code",
    "population",
    "gdp_per_capita",
]

# %%
final_gdp_pop = final_gdp_pop.loc[:, cols]
final_gdp_pop.head()

# %%
final_gdp_pop.columns = [
    i.lower().replace(" ", "_") for i in final_gdp_pop.columns
]
final_gdp_pop.head()

# %%
final_gdp_pop.columns

# %%
cols = [
    "uss30_region_name",
    "country_name",
    "country_code",
    "km2",
    "sum_static",
    "msa.km2",
    "population",
    "gdp_per_capita",
]

# %%
final_gdp_pop = final_gdp_pop.loc[:, cols]
final_gdp_pop.rename(
    columns={
        "uss30_region_name": "region",
        "sum_static": "sum_msa_static",
        "msa.km2": "msa.km2",
    },
    errors="ignore",
    inplace=True,
)

# %% [markdown]
# ## Export 

# %%
final_gdp_pop.to_csv("./data/final/final.csv", index=False)
