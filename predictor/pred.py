import pandas
from sklearn.neighbors import KNeighborsClassifier
def dist(a,b):
	return (sum([(a[i] - b[i]) ** 2 for i in range(len(a))]))**(0.5)
def getnn(V): #returns [distance,key] for nearest neighbors
	mn = [float('Inf'),None]
	for k in fighters.keys():
		x = fighters[k]
		d = dist(V,x)
		if d < mn:
			mn = [d,k]
	return mn

fighters = pandas.read_csv('fighters_data.csv',index_col=0)
fights = pandas.read_csv('fight_data.csv')
classifier = KNeighborsClassifier()


X = [x[:-1] for x in fights.values]
labels = [x[-1] for x in fights.values]
classifier.fit(X,labels)
def predict(A,B):
	bal = 0
	#make fight row and inverse row
	Avect,Bvect = list(fighters.loc[A]),list(fighters.loc[B])
	row,invrow = Avect + Bvect, Bvect + Avect
	print row
	return classifier.predict([row,invrow])
print predict('Conor McGregor',"Khabib Nurmagomedov")