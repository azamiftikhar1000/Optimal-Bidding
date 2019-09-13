import pandas as pd
import sys
import numpy as np
filename = '21.csv'
solart = pd.read_csv('Solar.csv',header=None)  # Add appropriate paths for each file
demandt = pd.read_csv('Demand.csv',header=None)
pricet = pd.read_csv('Price.csv',header=None)
battery = 0
bid = pd.read_csv(filename,header=None)
price = 0
c = -1
hour = 0
if bid.values.shape==(1200,2):
	for s in bid.values:
	  c=c+1
	  quant = demandt.values[c/24][c%24]-solart.values[c/24][c%24]
	  if c<=5:
	  	print bid.values[c][1],s[0]
	  if s[0]>=pricet.values[c/24][c%24]:
	    if quant<0:
	      quant = 0
	    bid_quanty = bid.values[c][1]
	    if bid_quanty>=quant:
	      diff = bid_quanty-quant
	      if diff>5:
		diff = 5
	      battery+=diff
	      if battery>25:
		battery=25
	      price+=bid_quanty*s[0]
	    else:
	      diff = quant-bid_quanty
	      a = 4
	      if 0.8*battery<a:
	      	a=0.8*battery
	      if diff<a:
	      	a=diff
	      mini = a
	      diff-=mini
	      battery-=mini/0.8
	      price+=bid_quanty*s[0]+diff*7
	  else:
	    bid_quanty = 0
	    diff = quant
	    a = 4
	    if 0.8*battery<a:
	    	a=0.8*battery
	    if diff<a:
	    	a=diff
	    mini = a
	    diff-=mini
	    battery-=mini/0.8
	    price+=diff*7

	print price


	# if results.values[ID][1]==-1 or ID==23:
	# 	results.at[ID,'Score'] = price
	# else:
	# 	if results.values[ID][1] > price:
	# 		results.at[ID,'Score'] = price  

	# print results.values[ID][1]

	# results.to_csv('results.csv',index=False)