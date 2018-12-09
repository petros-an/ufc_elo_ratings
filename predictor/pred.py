import pandas
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer, accuracy_score
N_NEIGHBORS = 3
def dist(a,b):
	return (sum([(a[i] - b[i]) ** 2 for i in range(len(a))]))**(0.5)

def get_balance(A,B):
	bal = 0
	#make fight row and inverse row
	Avect,Bvect = list(fighters.loc[A]),list(fighters.loc[B])
	row,invrow = Avect + Bvect, Bvect + Avect
	rowNN = list(classifier.kneighbors([row],return_distance=True))
	invNN = list(classifier.kneighbors([invrow],return_distance=True))
	for i in range(N_NEIGHBORS):
		cur_fight_res = fights.loc[rowNN[1][0][i]]['winner']
		cur_fight_dist = rowNN[0][0][i]
		bal += cur_fight_res/cur_fight_dist
	for i in range(N_NEIGHBORS):
		cur_fight_res = fights.loc[invNN[1][0][i]]['winner'] 
		cur_fight_dist = invNN[0][0][i]
		bal -= cur_fight_res/cur_fight_dist
	return bal

class predictor:
	def __init__(self,k):
		self.k = N_NEIGHBORS
		self.knn = KNeighborsClassifier(n_neighbors = N_NEIGHBORS)
	def fit(self,X,y):
		self.knn.fit(X,y)
	def get_params(self,deep=False):
		return {'k':self.k}
	def predict(self,F,distance=dist):
		res = []
		for f in F:
			print f
			A,B = f[0],f[1]
			print A,B
			b = get_balance(A,B)
			if b > 0:
				res.append(-1)
			else:
				res.append(1)

fighters = pandas.read_csv('fighters_data.csv',index_col=0)
fights = pandas.read_csv('fight_data.csv')
classifier = KNeighborsClassifier(n_neighbors = N_NEIGHBORS)
X = [list(x[2:-1]) for x in fights.values]
labels = [x[-1] for x in fights.values]
classifier.fit(X,labels)
print get_balance("Brian Ortega","Max Holloway")
#P = predictor(0)
#scores = cross_val_score(P, X=X, y=labels, cv=2, scoring=make_scorer(accuracy_score))
#print scores
