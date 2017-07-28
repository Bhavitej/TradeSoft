import quandl, math
import numpy as np
import pandas as pd
from pandas import DataFrame
import re
import sys
reload(sys)
import os
from django.conf import settings
import datetime
from datetime import timedelta
sys.setdefaultencoding('utf-8')
from supply_phase1v3 import df_initialization,write_to_csv
def get_monthdataset(month_dataset,count,day_df,start,end):
	month_open=day_df['Open'].iloc[end]
	month_close=day_df['Close'].iloc[start]
	month_low=float("inf")
	month_high=float("inf")*(-1)
	for i in range(start,end):
		if(month_low>day_df['Low'].iloc[i]):
			month_low=day_df['Low'].iloc[i]
		if(month_high<day_df['High'].iloc[i]):
			month_high=day_df['High'].iloc[i]
	month_dataset.append([month_high,month_low,month_open,month_close])
	count+=1
	return month_dataset,count
def get_day(date):
	return date.weekday()
def month_candle_classification(month_df):
	month_df = month_df[['Open',  'High',  'Low',  'Close']]
	month_df['Candle_Label'] = '-'
	month_df['Least_of_body']=float(0)
	month_df['Height_of_highest']= float(0)
	i = 0 
	for O,C,H,L in zip(month_df['Open'], month_df['Close'],month_df['High'],month_df['Low']):
		month_df['Height_of_highest'].iloc[i]=float(month_df['High'].iloc[i])
		if C==O:
			month_df['Least_of_body'].iloc[i]=float(month_df['Open'].iloc[i])
			month_df['Candle_Label'].iloc[i]="Green Boring Candle"
	   
	   
		elif C>O:
			month_df['Least_of_body'].iloc[i]=float(month_df['Open'].iloc[i])
			if ((C-O)>(H-C)+(O-L)):
				month_df['Candle_Label'].iloc[i]="Green Exciting Candle"
			
			
			else:
				month_df['Candle_Label'].iloc[i]="Green Boring Candle"
			
			
		else:
			month_df['Least_of_body'].iloc[i]=float(month_df['Close'].iloc[i])
			if((O-C)>(H-O)+(C-L)):
				month_df['Candle_Label'].iloc[i]="Red Exciting Candle"
			
			
			else:
				month_df['Candle_Label'].iloc[i]="Red Boring Candle"

		i+=1
	month_df = month_df[['Open',  'High',  'Low',  'Close','Candle_Label','Least_of_body','Height_of_highest']]		
	return	month_df
def first_critical_point_finder(month_df):
	pointer1=-1;pointer2=-1;pointer3=-1;flag=0
	for i in range(len(month_df['Candle_Label'])-1):
		if (month_df['Candle_Label'].iloc[i]=="Red Exciting Candle" and (month_df['Candle_Label'].iloc[i+1]=="Green Boring Candle" or month_df['Candle_Label'].iloc[i+1]=="Red Boring Candle") and flag==0):
			pointer1=i
			flag=1
		elif(flag ==1 and (month_df['Candle_Label'].iloc[i]=="Red Boring Candle" or month_df['Candle_Label'].iloc[i]=="Green Boring Candle")):
			pointer2=i
		elif(flag==1 and (month_df['Candle_Label'].iloc[i]=="Green Exciting Candle" or month_df['Candle_Label'].iloc[i]=="Red Exciting Candle") ):
			pointer3=i
			flag=2
			break
	if((month_df['Candle_Label'].iloc[len(month_df['Candle_Label'])-1]=="Green Exciting Candle" or month_df['Candle_Label'].iloc[len(month_df['Candle_Label'])-1]=="Red Exciting Candle") and flag==1 and i==len(month_df['Candle_Label'])-2 and (month_df['Candle_Label'].iloc[i]=="Red Boring Candle" or month_df['Candle_Label'].iloc[i]=="Green Boring Candle")):
		flag=2
		pointer2=i
		pointer3=len(month_df['Candle_Label'])-1
	signal=0
	if(flag==2):
		signal=1
	else:
		signal=0
		print "Zone not found"
	return signal,pointer1,pointer2,pointer3
def Entry_StopLoss_Target_finder(month_df,pointer1,pointer2,pointer3):
	least_height_of_body=float("inf")
	for i in range(pointer1+1,pointer3):
		if(least_height_of_body>month_df['Least_of_body'].iloc[i]):
			least_height_of_body=month_df['Least_of_body'].iloc[i]

	print "Entry(least_height_of_body):{:02f}".format(least_height_of_body)
	Entry=least_height_of_body

	max_height_of_highests=float(0)
	for i in range(pointer1,pointer3):
		if(max_height_of_highests<month_df['Height_of_highest'].iloc[i]):
			max_height_of_highests=month_df['Height_of_highest'].iloc[i]

	print "Stop Loss(max_height_of_highests):{:02f}".format(max_height_of_highests)
	Stop_Loss=max_height_of_highests

	Target2X= (Entry-Stop_Loss)*2+Entry
	print "Target2X:{:02f}".format(Target2X)

	Target3X= (Entry-Stop_Loss)*3+Entry
	print "Target3X:{:02f}".format(Target3X)
	return Entry,Stop_Loss
def Param1(month_df_init,pp1,Entry):
	High=(float("inf"))*(-1)
	score=0
	for i in range(0,pp1):
		if(High<month_df_init['Height_of_highest'].iloc[i]):
			High=month_df_init['Height_of_highest'].iloc[i]
	if(Entry>High):
		score+=1
	else:
		score+=0
	return score,High
def best_critical_point_finder(month_df,file_name):
	sum=0
	p3=0
	it=1
	#target=open(file_name, "w+")
	target = open(os.path.join(settings.MEDIA_ROOT, file_name), 'w+')
	month_df_init=month_df.copy(deep=True)
	#print(df_init.head(100))
	while 1==1:
		month_df=month_df[p3:]
		signal,p1,p2,p3=first_critical_point_finder(month_df)
		if signal==0:
			target.write("Final Results:\nZone not found\n")
			return -1,-1,-1
		else:
			print "Iteration {:d}:".format(it)
			target.write("\nIteration {:d}:\n".format(it))
			print "Zone found"
			target.write("Zone found\n")
			pp1=p1+sum;pp2=p2+sum;pp3=p3+sum
			print "Pointer1:{:0d}\nPointer2:{:0d}\nPointer3:{:0d}".format(p1+sum,p2+sum,p3+sum)
			target.write("Pointer1:{:0d}\nPointer2:{:0d}\nPointer3:{:0d}\n".format(p1+sum,p2+sum,p3+sum))
			sum+=p3
			Entry,Stop_Loss=Entry_StopLoss_Target_finder(month_df,p1,p2,p3)
			target.write("Entry:{:0f}\nStopLoss{:0f}\n".format(Entry,Stop_Loss))
		fresh_score,High=Param1(month_df_init,pp1,Entry)
		print "Fresh_score:{:d}\n".format(fresh_score)
		target.write("Fresh_score={:d}\nHigh_till_that_point={:f}\n".format(fresh_score,High))
		if(fresh_score==1):
			print "Desired Zone found"
			target.write("\nDesired Zone found\n")
			print "Final values:\nEntry={:f}\nStop Loss={:f}\n".format(Entry,Stop_Loss)
			target.write("Final values:\nEntry={:f}\nStop Loss={:f}\nFresh_score={:d}\nHigh_till_that_point={:f}\n".format(Entry,Stop_Loss,fresh_score,High))
			return Entry,Stop_Loss,sum

		it+=1
	return -1,-1,-1

def get_month_Entry_StopLoss(day_df,time_duration,stock_code):
	day_df=day_df.iloc[::-1]
	day_df=day_df.reset_index()
	day_df = day_df[['Date','Open', 'High',  'Low',  'Close']]
	dummy=get_day(day_df['Date'][0])
	mon_date=day_df['Date'][0] - timedelta(days=dummy)
	fri_date=mon_date+timedelta(days=6)
	last_fri_date=fri_date-timedelta(days=7)
	#print dummy,mon_date
	monthnum=(day_df['Date'][0].date()).month
	yearnum=(day_df['Date'][0].date()).year
	daynum=(day_df['Date'][0].date()).day
	if((day_df['Date'][0] + timedelta(days=1)).date().month==monthnum+1 or (day_df['Date'][0] + timedelta(days=1)).date().year==yearnum+1):
		months=monthnum
	elif(((day_df['Date'][0] + timedelta(days=3)).date().month==monthnum+1 or(day_df['Date'][0] + timedelta(days=3)).date().year==yearnum+1) and dummy==4):
		months=monthnum
	elif(((day_df['Date'][0] + timedelta(days=2)).date().month==monthnum+1 or(day_df['Date'][0] + timedelta(days=2)).date().year==yearnum+1) and dummy==5):
		months=monthnum
	else:
		months=monthnum-1
	days=0
	flag=0
	count=0
	start=-2
	end=-2
	month_dataset=[]
	it=0
	for it in range(time_duration):
		if(day_df['Date'].iloc[it].date().month==months):
			break
	day_df=day_df[it:]
	print(day_df['Date'].iloc[0])
	print('----------------')
	while days<=time_duration:
		if(day_df['Date'].iloc[days].date().month==months and flag==0):
			start=days
			end=days
			days+=1
			flag=1
		elif(day_df['Date'].iloc[days].date().month==months and flag==1):
			end=days
			days+=1
		else:
			print months
			months-=1
			if(months==0):
				months=12
			flag=0
			if(start!=-2 and end!=-2 ):
				month_dataset,count=get_monthdataset(month_dataset,count,day_df,start,end)
			print start," ",end," ",count
	month_df=pd.DataFrame(month_dataset,columns=['High','Low','Open','Close'])
	month_df=month_candle_classification(month_df)
	s1=str("Supply_Monthly_files/"+"Supply_monthly_"+stock_code+".txt")
	s2=str("Supply_Monthly_files/"+"Supply_monthly_"+stock_code+".csv")
	Entry,Stop_Loss,sum=best_critical_point_finder(month_df,s1)
	#write_to_csv(month_df,s2,count)
	return Entry,Stop_Loss,sum
def supply_month_execute(stock_code,time_duration):
	s="NSE/"
	print(s+str(stock_code))
	df = quandl.get(s+str(stock_code),authtoken="Exr53XDym_ASzGYMsQcF") #Exr53XDym_ASzGYMsQcF,jR46fDURnSV3hiHmjyyi
	Desired_Entry,Desired_Stop_Loss,sum= get_month_Entry_StopLoss(df,time_duration,stock_code)
	return Desired_Entry,Desired_Stop_Loss
	
if __name__ == "__main__":
	df=df_initialization()
	get_month_Entry_StopLoss(df,1000,str(sys.argv[1]))
