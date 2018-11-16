import os
import math
file = open("data.csv","r")
data = file.readlines()
for i in range(1,len(data)):
	start = data[i].find("\"")
	end = data[i].rfind("\"")
	if start != -1:
		data[i] = data[i][:start] + data[i][end+2:]
	data[i] = data[i].split(',')

headers = data[0].split(',')
del headers[6]
k = 50
f1_ind = headers.index("f1name")
f2_ind = headers.index("f2name")
f1_res_ind = headers.index("f1result")
f2_res_ind = headers.index("f2result")
fighters = {}
for d in data:
	f1_name = d[f1_ind]
	f2_name = d[f2_ind]
	if f1_name not in fighters:
		fighters[f1_name] = 1400
	if f2_name not in fighters:
		fighters[f2_name] = 1400
for d in data:
	f1_name = d[f1_ind]
	f2_name = d[f2_ind]
	f1_res = d[f1_res_ind]
	f2_res = d[f2_res_ind]
	f1_rating = fighters[f1_name]
	f2_rating = fighters[f2_name]
	f1_exp = 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (f1_rating - f2_rating) / 400))
	f2_exp = 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (f2_rating - f1_rating) / 400))
	if f1_res == "win":
		f1_act,f2_act = 1,0
	elif f1_res == "loss":
		f1_act,f2_act = 0,1
	else:
		f1_act,f2_act = 0.5,0.5
	fighters[f1_name] += k * (f1_act - f1_exp)
	fighters[f2_name] += k * (f2_act - f2_exp)
res = [[x, fighters[x]] for x in fighters.keys()]
res = sorted(res,key=lambda x:x[1], reverse = True)
file.close()
file = open("out.txt", "w")
for r in res:
	file.write(str(r[0]) + ":" + str(r[1]) + "\n")
file.close()