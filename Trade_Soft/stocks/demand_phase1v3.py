import quandl, math 
import numpy as np
import pandas as pd
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from django.conf import settings
#connects to quandl and extracts the dataframe
def df_initialization():
	s="NSE/"
	print(s+str(sys.argv[1]))
	df = quandl.get(s+str(sys.argv[1]),authtoken="Exr53XDym_ASzGYMsQcF") #Exr53XDym_ASzGYMsQcF,jR46fDURnSV3hiHmjyyi
	return df
#classifies the every day's candles into Green Exciting,Green Boring,Red Exciting,Red Boring
def candle_classification(df,time_duration):
	df = df[['Open',  'High',  'Low',  'Close']]
	df=df.iloc[::-1]
	df['Candle_Label'] = '-'
	df['Highest_of_body']=float(0)
	df['Height_of_lowest']= float(0)
	i = 0 
	df=df[:time_duration]
	#df=df[2:time_duration+2]
	for O,C,H,L in zip(df['Open'], df['Close'],df['High'],df['Low']):
		df['Height_of_lowest'][i]=float(df['Low'][i])                  #low of the candle
		if C==O:
			df['Highest_of_body'][i]=float(df['Close'][i])
			df['Candle_Label'][i]="Green Boring Candle"
	   
	   
		elif C>O:
			df['Highest_of_body'][i]=float(df['Close'][i])			   #Highest of the body of the candle
			if ((C-O)>(H-C)+(O-L)):
				df['Candle_Label'][i]="Green Exciting Candle"
			
			
			else:
				df['Candle_Label'][i]="Green Boring Candle"
			
			
		else:
			df['Highest_of_body'][i]=float(df['Open'][i])			    #Highest of the body of the candle
			if((O-C)>(H-O)+(C-L)):
				df['Candle_Label'][i]="Red Exciting Candle"
			
			
			else:
				df['Candle_Label'][i]="Red Boring Candle"

		i+=1
	df = df[['Open',  'High',  'Low',  'Close','Candle_Label','Highest_of_body','Height_of_lowest']]		
	return	df
#writing the dataframe to a csv file
def write_to_csv(df,filename,time_duration):
	#time_duration=365
	if(time_duration==0):						#setting the default time duration to 365 days
		time_duration=365
	df=df[:time_duration]
	df.to_csv(filename, sep='\t', encoding='utf-8')
	#print(df.head(time_duration))

#finding the first critical point 
def first_critical_point_finder(df):
	pointer1=-1;pointer2=-1;pointer3=-1;flag=0
	for i in range(len(df['Candle_Label'])-1):
		if (df['Candle_Label'][i]=="Green Exciting Candle" and (df['Candle_Label'][i+1]=="Green Boring Candle" or df['Candle_Label'][i+1]=="Red Boring Candle") and flag==0):
			pointer1=i
			flag=1
		elif(flag ==1 and (df['Candle_Label'][i]=="Red Boring Candle" or df['Candle_Label'][i]=="Green Boring Candle")):
			pointer2=i
		elif(flag==1 and (df['Candle_Label'][i]=="Green Exciting Candle" or df['Candle_Label'][i]=="Red Exciting Candle") ):
			pointer3=i
			flag=2
			break
	if((df['Candle_Label'][len(df['Candle_Label'])-1]=="Green Exciting Candle" or df['Candle_Label'][len(df['Candle_Label'])-1]=="Red Exciting Candle") and flag==1 and i==len(df['Candle_Label'])-2 and (df['Candle_Label'][i]=="Red Boring Candle" or df['Candle_Label'][i]=="Green Boring Candle")):
		flag=2
		pointer2=i
		pointer3=len(df['Candle_Label'])-1
	signal=0
	if(flag==2):
		signal=1
		#print "Zone found" 
		#print "Pointer1:{:d}".format(pointer1)
		#print "Pointer2:{:d}".format(pointer2)
		#print "Pointer3:{:d}".format(pointer3)
	else:
		signal=0
		print "Zone not found"
	return signal,pointer1,pointer2,pointer3

def Entry_StopLoss_Target_finder(df,pointer1,pointer2,pointer3):
	max_height_of_body=0
	for i in range(pointer1+1,pointer3):
		if(max_height_of_body<df['Highest_of_body'][i]):
			max_height_of_body=df['Highest_of_body'][i]

	print "Entry(max_height_of_body):{:02f}".format(max_height_of_body)
	Entry=max_height_of_body

	least_height_of_lowests=float("inf")
	for i in range(pointer1,pointer3):
		if(least_height_of_lowests>df['Height_of_lowest'][i]):
			least_height_of_lowests=df['Height_of_lowest'][i]

	print "Stop Loss(least_height_of_lowests):{:02f}".format(least_height_of_lowests)
	Stop_Loss=least_height_of_lowests

	Target2X= (Entry-Stop_Loss)*2+Entry
	print "Target2X:{:02f}".format(Target2X)

	Target3X= (Entry-Stop_Loss)*3+Entry
	print "Target3X:{:02f}".format(Target3X)
	return Entry,Stop_Loss

if __name__ == "__main__":
	df=df_initialization()
	df=candle_classification(df,21)
	write_to_csv(df,"StockPrice_Table.csv",1000)
	signal,p1,p2,p3=first_critical_point_finder(df)
	if(signal==1):
		Entry,Stop_Loss=Entry_StopLoss_Target_finder(df,p1,p2,p3)



