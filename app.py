from flask import Flask, render_template, url_for, request, redirect, jsonify, session
import csv
import pandas as pd
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float, Date
import os
import json
import requests
from bs4 import BeautifulSoup

db_uri = os.getenv("DATABASE_URI", "sqlite:///budgetapp.sqlite")
engine = create_engine( db_uri )

app=Flask (__name__)


# read transactions and save to sqlite
#go = pd.read_csv('final-bank-activities.csv')

# save to database
#go.to_sql('transactions', engine, if_exists='replace')

# changed engine to python 
#categories = pd.read_csv("Categories.csv", engine="python")
#categories.to_sql('categories', engine, if_exists='replace')

@app.route ('/')
def homepage():
    return render_template ("index.html")

@app.route ('/spending/')
@app.route ('/spending/<date>')
def spending( date='201807'):

    conn = engine.connect()
    query = "select * from expense where strftime('%Y%m',date) = '{}' and Amount IS NOT NULL".format( date )
    results = conn.execute( query ).fetchall()
    s = "select * from summary where strftime('%Y%m',date) = '{}' and Amount IS NOT NULL".format( date )
    summary = conn.execute( s ).fetchall()
    sum = "select sum(amount) from summary where strftime('%Y%m',date) = '{}' and Amount IS NOT NULL".format( date )
    sum_results = round( conn.execute( sum ).fetchone()[0] , 3 )
    m = "select distinct(date) from summary"
    months = conn.execute( m ).fetchall()
    return render_template ("spending.html", data = results, summary = summary, sum=sum_results )


@app.route('/budget')
def budget():

    date = '201807'
    conn = engine.connect()
    query = "select * from expense where strftime('%Y%m',date) = '{}' and Amount IS NOT NULL".format(date)
    results = conn.execute( query ).fetchall()
    s = "select category,amount from summary where strftime('%Y%m',date) = '{}' and Amount IS NOT NULL".format( date )
    summary = conn.execute( s ).fetchall()
    cat = []
    amt = []
    for i in summary:
        cat.append( i["Category"])
        amt.append( i["Amount"] )

    budget = "select * from budget"
    budget_data = conn.execute( budget ).fetchall()
    print( budget_data )
    budget_cat = []
    budget_amt = []
    for a in budget_data:
        budget_cat.append( a["category"] )
        budget_amt.append( a["amount"] )

    print(" Inside GET {}".format( budget_amt ) )
    return render_template("budget.html", data=results, cat=cat, amt=amt, budget_amt=budget_amt, budget_cat=budget_cat )


@app.route('/save-budget', methods=[ "POST"])
def save_budget():

        # form fields
        don = request.form['don']
        ent = request.form['ent']
        gas = request.form['gas']
        gro = request.form['gro']
        shop = request.form['shop']
        ins = request.form['ins']
        misc = request.form['misc']
        rent = request.form['rent']
        rest = request.form['rest']
        trans = request.form['trans']
        travel = request.form['travel']
        util = request.form['util']

        conn = engine.connect()

        # save to db
        values = { "Donation": don, "Entertainment": ent, "Gas": gas, "Groceries": gro, "Shopping": shop, "Insurance": ins, 
                   "Misc": misc, "Mortgage":rent, "Restaurant": rest, "Transportation": trans, "Travel": travel, "Utilities": util }
        for k,v in values.items():
                query = "UPDATE budget set amount = '{}' where category = '{}'".format( v, k )
                print( query )
                conn.execute( query )

        return redirect(url_for('budget'))


@app.route ('/login' , methods = [ 'GET','POST'])
def login():

    # get transactions from database
    conn = engine.connect()
    query = 'select * from transactions'
    results = conn.execute( query ).fetchall()
    for i in results:
        date = i["Date"]
        desc = i["Description"]
        amt = i ["Amount"]

        #print(date, desc, amt)
    
    # get categories from database
    query = 'select * from categories'
    categories = conn.execute( query ).fetchall()
    for i in categories:
    	print(i)

    if request.method == 'GET':
    	return render_template('home.html', data=results, cat=categories )

    if request.method == 'POST':
	    # get login and password
	    login = request.form['login']
	    pwd = request.form['pwd']

	    # if login is successful redirect to home.html
	    if login == 'team' and pwd == '0000':
	       return render_template('home.html', data=results, cat=categories )
	    # if login fails stay on index.html
	    else:
	       return render_template('index.html', data=False )

@app.route('/coupons/')
def coupons():

    url = 'https://www.couponsurfer.com/rss4.xml'
    r = requests.get( url )
    soup = BeautifulSoup( r.content, "xml" )
    items = soup.find_all('item')
    
    titles = []
    links = []
    desc = []
    guid = []
    for i in items:
        titles.append( i.title.text )
        links.append( i.link.text )
        desc.append( i.description.text )
        guid.append( i.guid.text )
    
    # image = ''
    # for a in guid:
    #     r = requests.get( a )
    #     soup = BeautifulSoup( r.content, "html.parser" )
    #     image = soup.find(class_="imgoverlay").find('img')['src']

    return render_template("coupons.html", data=zip( titles, links, desc, guid ) )

@app.route('/income/')
def income():

    conn = engine.connect()
    query = "select amount from income"
    results = conn.execute( query ).fetchone()[0]

    year_income = """ 
    SELECT strftime('%m', date) as valMonth, 
    SUM(amount) as valTotalMonth 
    FROM  expense 
    WHERE strftime('%Y', date)='2017' or strftime('%Y', date)='2018' GROUP BY valMonth
    """

    income = conn.execute( year_income ).fetchall()

    total = conn.execute("select sum(amount) from expense").fetchone()[0]

    return render_template('income.html', data=results, income=income, total=total )

@app.route('/save-income', methods=[ "POST"])
def save_income():

        # form fields
        income = request.form['income']

        conn = engine.connect()

        # save to db
        query = "UPDATE income set amount = '{}'".format( income )
        print( query )
        conn.execute( query )

        return redirect(url_for('income'))

@app.route('/resources/')
def resources():

    return render_template('resources.html')



if __name__ == '__main__':
    app.run( debug= True)



""" 
changes - add request, redirect in app.py
add form action url and method in index.html
add method to app.route /home
add logic for login contrl 
"""