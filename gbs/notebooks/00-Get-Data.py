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
# # 00-Get-Data

# %% [markdown]
# Just find the data and download it.

# %% [markdown]
# ## System

# %%
# cd ../

# %%
# !pwd

# %% [markdown]
# ## Imports

# %%
# built in modules
import os
import json

# %%
# third party modules
import pandas as pd

# %%
# custom modules
from gbs.etl.urls import Urls
from gbs.helpers import runcmd

# from gbs.etl.extract import Extract

# %% [markdown]
# ## Build Data Directories

# %%
# make data/ directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# %%
# make subdirectories if they don't exist
folder_list = ["source", "tmp", "final"]
for folder in folder_list:
    if not os.path.exists(f"data/{folder}"):
        os.makedirs(f"data/{folder}")

# %%
# make subdirectories if they don't exist
sub_folders = ["crops", "country_specs", "gdp", "population", "production"]
for folder in sub_folders:
    if not os.path.exists(f"data/source/{folder}"):
        os.makedirs(f"data/source/{folder}")

# %% [markdown]
# ## Download Data

# %% [markdown]
# ### Crops

# %%
# download crops
runcmd("wget -O data/source/crops/crops.csv " + Urls.crops)

# %% [markdown]
# ### Country Specs

# %%
# download countries specs
runcmd(
    "wget -O data/source/country_specs/country_specs.csv " + Urls.country_specs
)

# %% [markdown]
# ### Production

# %%
# curl qlc.zip
runcmd(
    f"curl --output ./data/source/production/production.zip '{Urls.production}'"
)

# %% [markdown]
# ### GDP

# %%
# curl qlc.zip
runcmd(f"curl --output ./data/source/gdp/gdp.zip '{Urls.gdp}'")

# %% [markdown]
# ### Population

# %%
# curl pip.zip
runcmd(
    f"curl --output ./data/source/population/population.zip '{Urls.population}'"
)

# %% [markdown]
# ## Manage Files

# %% [markdown]
# ### Production

# %%
# unzip the file
runcmd(
    f"unzip ./data/source/production/production.zip -d ./data/source/production"
)

# %%
# update filenames to lowercase
path = "data/source/production/"
pattern = "Production_Crops_Livestock_E_All_"

for fn in os.listdir(path):
    # clean filename
    cleaned_fn = (
        fn.replace(pattern, "").lower().replace("(", "").replace(")", "")
    )

    # src and dst
    src_ = os.path.join(path, fn)
    dst_ = os.path.join(path, cleaned_fn.replace(pattern.lower(), ""))

    # do rename
    os.rename(src_, dst_)

# %%
os.listdir("data/source/production/")

# %%
# # !rm -rf data/source/production/production.zip

# %% [markdown]
# ### GDP & Popuplation

# %%
# unzip the file
runcmd(
    f"unzip ./data/source/population/population.zip -d ./data/source/population"
)

# %%
# unzip the file
runcmd(f"unzip ./data/source/gdp/gdp.zip -d ./data/source/gdp")

# %% [markdown]
# ## Check Data Integrity

# %% [markdown]
# ### Crops and country specs

# %%
ext = ".csv"
base = "data/source/"

folders = ["crops", "country_specs"]


for folder in folders:
    path = os.path.join(base, folder)

    for fn in os.listdir(path):
        if not fn.endswith(ext):
            continue

        print(fn)

        df = pd.read_csv(os.path.join(path, fn))
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] > 0
        assert df.shape[1] > 0

# %% [markdown]
# ### Population and Gdp

# %%
ext = ".csv"
base = "data/source/"

folders = ["population", "gdp"]

for folder in folders:
    path = os.path.join(base, folder)

    fn = [i for i in os.listdir(path) if i.startswith("API")][0]
    print(fn)

    with open(os.path.join(path, fn)) as f:
        txt = f.readlines()

    txt = txt[4:]

    with open(os.path.join(path, fn), "w") as f:
        f.writelines(txt)

# %%
ext = ".csv"
base = "data/source/"

folders = ["population", "gdp"]

for folder in folders:
    path = os.path.join(base, folder)
    fn = [i for i in os.listdir(path) if i.startswith("API")][0]

    print(fn)

    df = pd.read_csv(os.path.join(path, fn), encoding="latin-1")

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0
    assert df.shape[1] > 0
    df.to_csv(os.path.join(path, fn), index=False, encoding="utf-8")

# %% [markdown]
# ### Production

# %%
ext = ".csv"
base = "data/source/production/"

for fn in os.listdir(base):
    if not fn.endswith(ext):
        continue

    print(fn)

    df = pd.read_csv(os.path.join(base, fn), encoding="latin-1")
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0
    assert df.shape[1] > 0
    df.to_csv(os.path.join(base, fn), encoding="utf-8", index=False)
