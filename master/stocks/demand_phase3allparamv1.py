import quandl, math
import numpy as np
import pandas as pd
import re
import io
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
from demand_phase1v3 import df_initialization,write_to_csv,first_critical_point_finder
from demand_weekly_phase1v1 import get_week_Entry_StopLoss
from demand_monthly_phase1v1 import get_month_Entry_StopLoss
from demand_phase2v1allparam import demand_execute_function

if __name__ == "__main__":
	with io.open("Company_List.txt","r",encoding='utf8') as f:
		contents = f.readlines()
	init=time.time()
	for content in contents:
		t = time.time()
		content=content[:-1]
		print ("%s"%(content))
		demand_execute_function(content)
		print("%s: %f"%(content,time.time()-t))
	print("Total Time Taken: %f"%(time.time()-init))