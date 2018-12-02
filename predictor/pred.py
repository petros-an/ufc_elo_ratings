import pandas
import math

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
	fighters[k][_avg_td_att] = float(fighters[k][_avg_td_att]) / float(fighters[k][_fights]) 
	fighters[k][_avg_sig_str] = float(fighters[k][_avg_sig_str]) / float(fighters[k][_fights]) 

AgeMX,HeightMX,WeightMX,tdMX,ssMX = 0,0,0,0,0	
for k in fighters.keys():
	AgeMX = max(AgeMX,fighters[k][_Age])
	HeightMX = max(HeightMX,fighters[k][_Height])
	WeightMX = max(WeightMX,fighters[k][_Weight])
	tdMX = max(tdMX,fighters[k][_avg_td_att])
	ssMX = max(ssMX,fighters[k][_avg_sig_str])

for k in fighters.keys():
	fighters[k][_Age] = float(fighters[k][_Age]) / float(AgeMX)
	fighters[k][_Height] = float(fighters[k][_Height]) / float(HeightMX)
	fighters[k][_Weight] = float(fighters[k][_Weight]) / float(WeightMX)
	fighters[k][_avg_td_att] = float(fighters[k][_avg_td_att]) / float(tdMX)
	fighters[k][_avg_sig_str] = float(fighters[k][_avg_sig_str]) / float(ssMX)

''' speculative
def predict(A,B):
	bal = 0
	#make fight row and inverse row
	Avect = [fighters[A][_Age],fighters[A][_Weight],fighters[A][_Height],fighters[A][_avg_td_att],fighters[A][_avg_sig_str],fighters[A][_fights]]
	Bvect = [fighters[B][_Age],fighters[B][_Weight],fighters[B][_Height],fighters[B][_avg_td_att],fighters[B][_avg_sig_str],fighters[B][_fights]]
	row,invrow = A + B, B + A
	row_neigh,inv_neigh = getnn(row),getnn(invrow)
	for n in row_neigh:
		factor = 0
		if df['winner'][n[0]] == 'blue':
			factor = 1
		elif df['winner'][n[0]] == 'red':
			factor = -1
		bal += 1/n[1] * factor
	for n in inv_neigh:
		factor = 0
		if df['winner'][n[0]] == 'blue':
			factor = -1
		elif df['winner'][n[0]] == 'red':
			factor = 1
		bal += 1/n[1] * factor
	return A if bal > 0 else B
'''