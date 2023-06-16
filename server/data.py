#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 12:26:55 2023

@author: zkr
"""

import sqlite3
import json

conn=sqlite3.connect('newschema0613_kr.db')
cur=conn.cursor()

cur.execute ('SELECT * FROM User')
results_User= cur.fetchall()

cur.execute('SELECT * FROM Company')
results_Co=cur.fetchall()

cur.execute('SELECT * FROM Subscription')
results_Sub=cur.fetchall()

cur.close()
conn.close()

json_data_User=[]
for row in results_User:
    row_dict_user= {
        'user_id': row[0],
        'name': row[1],
        'email': row[2],
        'password_hashed': row[3]}
    json_data_User.append(row_dict_user)
    
json_data_Co=[]
for row in results_Co:
    row_dict_Co= {
        'co_id': row[0],
        'name': row[1],}
    json_data_Co.append(row_dict_Co)
    
json_data_Sub=[]
for row in results_Sub:
    row_dict_Sub= {
        'Sub_id': row[0],
        'user_id': row[1],
        'co_id': row[2],
        'start_date': row[3],
        'amount': row[4],
        'subscription_cycle': row[5]}
    json_data_Sub.append(row_dict_Sub)

json_data_combine={'User':json_data_User, 'Company':json_data_Co, 'Subscription': json_data_Sub}
with open('data.json', 'w') as json_file:
    json.dump (json_data_combine, json_file)