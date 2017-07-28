import quandl, math
import numpy as np
import pandas as pd
import re
import sys
reload(sys)
import os
from django.conf import settings
sys.setdefaultencoding('utf-8')
from supply_phase1v3 import df_initialization,candle_classification,write_to_csv,first_critical_point_finder,Entry_StopLoss_Target_finder
from supply_weekly_phase1v1 import get_week_Entry_StopLoss
from supply_monthly_phase1v1 import get_month_Entry_StopLoss
def best_critical_point_finder(df,file_name,weekly_stoploss,monthly_stoploss):
	sum=0
	p3=0
	it=1
	score=0
	trend_score=Param2(df)
	#target=open(file_name, "w+")
	target = open(os.path.join(settings.MEDIA_ROOT, file_name), 'w+')
	df_init=df.copy(deep=True)
	#print(df_init.head(100))
	while 1==1:
		df=df[p3:]
		signal,p1,p2,p3=first_critical_point_finder(df)
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
			Entry,Stop_Loss=Entry_StopLoss_Target_finder(df,p1,p2,p3)
			target.write("Entry:{:0f}\nStopLoss{:0f}\n".format(Entry,Stop_Loss))
		score=0
		fresh_score,High=Param1(df_init,pp1,Entry)
		Gap_up_score=Param3(df,p1,p2,p3)
		time_spend_score=Param4(p1,p2)
		High_score,Low=Param5(df_init,pp1,Entry,Stop_Loss)
		curve_score=Param6(weekly_stoploss,monthly_stoploss,Stop_Loss)
		score=fresh_score+trend_score+Gap_up_score+time_spend_score+High_score+curve_score
		print "score:{:d}\n".format(score)
		target.write("score:{:d}\nFresh_score={:d}\nHigh_till_that_point={:f}\ntrend_score={:d}\nGap_up_score={:d}\ntime_spend_score={:d}\nHigh_score={:d}\nLow_till_that_point={:f}\nWeekly_stoploss:{:f}\nMonthly_stoploss:{:f}\nCurve_Score:{:f}\n".format(score,fresh_score,High,trend_score,Gap_up_score,time_spend_score,High_score,Low,weekly_stoploss,monthly_stoploss,curve_score))
		if(score>=8 and fresh_score==1):
			print "Desired Zone found"
			target.write("\nDesired Zone found\n")
			print "Final values:\nEntry={:f}\nStop Loss={:f}\nscore={:d}".format(Entry,Stop_Loss,score)
			target.write("Final values:\nEntry={:f}\nStop Loss={:f}\nscore={:d}\nFresh_score={:d}\nHigh_till_that_point={:f}\ntrend_score={:d}\nGap_up_score={:d}\ntime_spend_score={:d}\nHigh_score={:d}\nLow_till_that_point={:f}\nWeekly_stoploss:{:f}\nMonthly_stoploss:{:f}\nCurve_Score:{:f}\n".format(Entry,Stop_Loss,score,fresh_score,High,trend_score,Gap_up_score,time_spend_score,High_score,Low,weekly_stoploss,monthly_stoploss,curve_score))
			return Entry,Stop_Loss,sum

		it+=1
	return -1,-1,-1

def Param1(df_init,pp1,Entry):
	High=(float("inf"))*(-1)
	score=0
	for i in range(0,pp1):
		if(High<df_init['Height_of_highest'][i]):
			High=df_init['Height_of_highest'][i]
	if(Entry>High):
		score+=1
	else:
		score+=0
	return score,High

def Param2(df):
	sum=0
	score=0
	for i in range(0,50):
		sum+=df['Close'][i]
	avg_latest=sum/50

	sum=0
	for i in range(7,57):
		sum+=df['Close'][i]
	avg_before_seven_days=sum/50

	if(avg_before_seven_days>=avg_latest):
		score+=1
	else:
		score+=0
	return score

def Param3(df,p1,p2,p3):
	score=0
	if(p1>0 and df['Candle_Label'][p1-1]=="Red Exciting Candle"):
		score+=1
	else:
		score+=0
	if(max(df['Open'][p1], df['Close'][p1])<min(df['Open'][p1+1], df['Close'][p1+1])):
		score+=1
	return score

def Param4(p1,p2):
	score=0
	if(p2-p1<3):
		score+=2
	elif(p2-p1>=3 and p2-p1<6):
		score+=1
	else:
		score+=0
	return score

def Param5(df_init,pp1,Entry,Stop_loss):
	score=0
	Low=(float("inf"))
	for i in range(0,pp1):
		if(Low>df_init['Low'][i]):
			Low=df_init['Low'][i]
	if(Entry + (Entry-Stop_loss)*6 >=Low):
		score+=2
	elif(Entry + (Entry-Stop_loss)*4>=Low):
		score+=1
	else:
		score+=0
	return score,Low

def Param6(weekly_stoploss,monthly_stoploss,Stop_Loss):
	score=0
	if(weekly_stoploss>=Stop_Loss and weekly_stoploss!=-1):
		score+=1
	if(monthly_stoploss>=Stop_Loss and monthly_stoploss!=-1):
		score+=1
	return score

def supply_execute_function(stock_code):
	s="NSE/"
	df = quandl.get((s+stock_code),authtoken="Exr53XDym_ASzGYMsQcF") #Exr53XDym_ASzGYMsQcF,jR46fDURnSV3hiHmjyyi
	maxdur=min(len(df.index)-35,1000)
	weekly_entry,weekly_stoploss,sum=get_week_Entry_StopLoss(df,maxdur,stock_code)
	monthly_entry,monthly_stoploss,sum= get_month_Entry_StopLoss(df,maxdur,stock_code)
	df=candle_classification(df,maxdur)
	stock_code=stock_code+"_supply"
	file_name="Supply_Daywise_files/"+stock_code+".txt"
	Desired_Entry,Desired_Stop_Loss,sum=best_critical_point_finder(df,file_name,weekly_stoploss,monthly_stoploss)
	#file_name="./Supply_Daywise_files/"+stock_code+".csv"
	#write_to_csv(df,file_name,sum+1)
	return Desired_Entry,Desired_Stop_Loss,monthly_entry,monthly_stoploss,weekly_entry,weekly_stoploss

if __name__ == "__main__":
	df=df_initialization()
	weekly_entry,weekly_stoploss,sum=get_week_Entry_StopLoss(df,1000,str(sys.argv[1]))
	monthly_entry,monthly_stoploss,sum= get_month_Entry_StopLoss(df,1000,str(sys.argv[1]))
	df=candle_classification(df,1000)
	Desired_Entry,Desired_Stop_Loss,sum=best_critical_point_finder(df,str(sys.argv[1])+".txt",weekly_stoploss,monthly_stoploss)
	if(Desired_Entry==-1 and Desired_Stop_Loss==-1 and sum==-1):
		print "Final Results:\nZone not found"
	write_to_csv(df,"StockPrice_Table.csv",sum+1)
