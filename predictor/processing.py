import pandas
import math
from sklearn.neighbors import KNeighborsClassifier

_Age,_Weight,_Height,_avg_td_att,_avg_sig_str,_fights = range(6)
fighters = {}
df = pandas.read_csv("data.csv")
for index,row in df.iterrows():
	#R
	R_Name = row['R_Name']
	R_Age,R_Weight,R_Height = row['R_Age'],row['R_Weight'],row['R_Height']
	if R_Name not in fighters:
		fighters[R_Name] = [R_Age,R_Weight,R_Height,0,0,0]
	fighters[R_Name][_fights] += 1
	tdatt,sigstr = 0,0
	for i in range(1,6):
		if not math.isnan(row['R__Round'+ str(i) + '_Grappling_Takedowns_Attempts']):
			tdatt += row['R__Round'+ str(i) + '_Grappling_Takedowns_Attempts']
		if not math.isnan(row['R__Round' + str(i) + '_Strikes_Body Significant Strikes_Attempts']):
			sigstr += row['R__Round' + str(i) + '_Strikes_Body Significant Strikes_Attempts']
	fighters[R_Name][_avg_td_att] += tdatt
	fighters[R_Name][_avg_sig_str] += sigstr
	#B
	B_Name = row['B_Name']
	B_Age,B_Weight,B_Height = row['B_Age'],row['B_Weight'],row['B_Height']
	if B_Name not in fighters:
		fighters[B_Name] = [B_Age,B_Weight,B_Height,0,0,0]
	fighters[B_Name][_fights] += 1
	tdatt,sigstr = 0,0
	for i in range(1,6):
		if not math.isnan(row['B__Round'+ str(i) + '_Grappling_Takedowns_Attempts']):
			tdatt += row['B__Round'+ str(i) + '_Grappling_Takedowns_Attempts']
		if not math.isnan(row['R__Round' + str(i) + '_Strikes_Body Significant Strikes_Attempts']):
			sigstr += row['R__Round' + str(i) + '_Strikes_Body Significant Strikes_Attempts']
	fighters[B_Name][_avg_td_att] += tdatt
	fighters[B_Name][_avg_sig_str] += sigstr

for k in fighters.keys():
	fighters[k][_avg_td_att] = int(float(fighters[k][_avg_td_att]) / float(fighters[k][_fights]) *100)
	fighters[k][_avg_sig_str] = int(float(fighters[k][_avg_sig_str]) / float(fighters[k][_fights]) *100)

AgeMX,HeightMX,WeightMX,tdMX,ssMX = 0,0,0,0,0	
for k in fighters.keys():
	cont = False
	for y in fighters[k]:
		if math.isnan(y):
			cont = True
			break
	if cont:
		continue
	AgeMX = max(AgeMX,fighters[k][_Age])
	HeightMX = max(HeightMX,fighters[k][_Height])
	WeightMX = max(WeightMX,fighters[k][_Weight])
	tdMX = max(tdMX,fighters[k][_avg_td_att])
	ssMX = max(ssMX,fighters[k][_avg_sig_str])

for k in fighters.keys():
	cont = False
	for y in fighters[k]:
		if math.isnan(y):
			cont = True
			break
	if cont:
		continue
	fighters[k][_Age] = int(float(fighters[k][_Age]) / float(AgeMX)*100)
	fighters[k][_Height] = int(float(fighters[k][_Height]) / float(HeightMX)*100)
	fighters[k][_Weight] = int(float(fighters[k][_Weight]) / float(WeightMX)*100)
	fighters[k][_avg_td_att] = int(float(fighters[k][_avg_td_att]) / float(tdMX)*100)
	fighters[k][_avg_sig_str] = int(float(fighters[k][_avg_sig_str]) / float(ssMX)*100)

X = []
#fighters_file = open("fighters.csv","w")
for k in fighters.keys():
	valid = True
	for y in fighters[k]:
		if math.isnan(y) or y > 100 or y < 0:
			del fighters[k]
			valid = False
			break
	if valid:
		X.append(fighters[k])
fighters_df = pandas.DataFrame.from_dict(fighters,orient='index')
fighters_df.columns = ["_Age","_Weight","_Height","_avg_td_att","_avg_sig_str","_fights"]
print fighters_df
fighters_df.to_csv("fighters_data.csv",index=True)

F = []
for index,row in df.iterrows():
	if row['B_Name'] not in fighters or row['R_Name'] not in fighters:
		continue
	res = row['winner']
	if res == 'blue':
		res = -1
	elif res == 'red':
		res = 1
	else:
		res = 0
	F.append([row['B_Name'],row['R_Name']] + fighters[row['B_Name']] + fighters[row['R_Name']] + [res])
fights_df = pandas.DataFrame.from_records(F,columns = ['B_Name','R_Name'] + ["B_Age","B_Weight","B_Height","B_avg_td_att","B_avg_sig_str","B_fights"] + ["R_Age","R_Weight","R_Height","R_avg_td_att","R_avg_sig_str","R_fights"] + ["winner"] )
fights_df.to_csv('fight_data.csv',index=False)