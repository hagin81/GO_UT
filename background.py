
# coding: utf-8

# In[2352]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
import pandas as pd
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float, Date
import os
import json
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.parser import parse
import sqlite3

engine = create_engine('sqlite:///budgetapp.sqlite', echo=True)
conn = engine.connect()

categories = pd.read_csv("Categories.csv", engine="python")

categories.to_sql('categories', engine, if_exists='replace')

# read transactions and save to sqlite
go = pd.read_csv('final-bank-activities.csv')

# save to database
go.to_sql('transactions', engine, if_exists='replace')

engine = create_engine('sqlite:///budgetapp.sqlite', echo=True)



query = "select * from categories" 



results = conn.execute(query).fetchone()


# In[2295]:


columns = results.keys()
columns


# In[2296]:


def get_category(value):
    data = []
    for i in columns:
        value = value.replace("'", " ")
        query = """ select `{c}` from categories where `{c}` like "%{v}%" """.format(c=i, v=value )
        result = conn.execute( query).fetchone()
        if result:
            data.append( i )
    if len(data) > 0:
        return data[0]
    else:
        return 'Miscellaneous'


# In[2297]:


print(get_category("shell"))


final = pd.read_csv("final-bank-activities.csv" , encoding="utf-8")
final.head()


# In[2310]:


final['Description'] = final['Description'].str.replace('"','').replace("'",'')


# In[2311]:


final["Category"] = final["Description"].map(get_category)


# In[2312]:


final.head()


# In[2313]:


#final['Date'] = pd.to_datetime( df['Date'] )


# In[2314]:


#final['Date']


# In[2315]:


final ["Amount"] = final["Amount"].astype(str).replace("$","")


# In[2316]:


#final.to_string()


# In[2317]:


final["Amount" ] = final["Amount"].astype(float)


# In[2318]:


final.groupby("Category")["Amount"].sum()


# In[2319]:


final


# In[2320]:


final["Date"] = pd.to_datetime( final["Date"] )
final


# In[2321]:


final.to_sql("expense",conn, if_exists="replace")


# In[2322]:


final.index = final["Date"]


# In[2323]:


summary = final.groupby("Category").resample('M').sum()


# In[2324]:


summary 


# In[2325]:


summary.to_sql("summary", conn, if_exists="replace")


# In[2326]:


final


# In[2330]:


a = conn.execute("select category,amount from summary where strftime('%Y%m',date) = '201807'").fetchall()


# In[2331]:


list(a)


# In[2335]:


count = 0
for i in a:
    cat = i['Category']
    amt = i['Amount']
    print( count, cat, amt  )
    count += 1


# In[2376]:


# create budget table 
conn = engine.connect()
query = "CREATE TABLE IF NOT EXISTS budget (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, amount FLOAT )"
conn.execute( query )


# In[2377]:


s = conn.execute( "select * from budget").fetchall()


# In[2378]:


data = [ 
( "Donation", 0 ),
( "Entertainment", 0 ),
( "Gas", 0 ),
( "Groceries", 0 ),
( "Insurance", 0 ),
( "Misc", 0 ),
( "Mortgage", 0 ),
( "Restaurant", 0 ),
( "Shopping", 0 ),
( "Transportation", 0 ),
( "Travel", 0 ),
( "Utilities", 0 ) ]


# In[2379]:


for i in data:
    conn.execute("insert into budget ( category, amount ) values (?,?)", i )

# create income table  
conn = engine.connect()
query = "CREATE TABLE IF NOT EXISTS income (id INTEGER PRIMARY KEY AUTOINCREMENT, amount FLOAT )"
conn.execute( query )