import scipy.stats
import statstools
import pymongo
import pprint
import numpy
import itertools
import math
# print scipy.stats.ttest_ind(NBA.chi_home, NBA.tor_away, equal_var=False)
def mongo_con_nba():
	# establish a connection to the database
	connection = pymongo.MongoClient("mongodb://localhost")
	# get a handle to the sports database
	db=connection.sports
	nba = db.nba15_16
	return nba
nba = mongo_con_nba()

def h_scores(team):
	"""Finds all scores by game from each home team 
	and puts it into a list for analysis
	"""
	cur = nba.aggregate([{"$match": {"team": team}}, 
						 {"$match": {"h_a": "vs"}},
						 {"$group": {"_id": {"scores": "$h_a"}, 
						 team: {"$push": "$s"} }}
						 ])

	new_cur = cur['result'][0][team]
	new_cur = filter(None, new_cur)
	return new_cur

def a_scores(team):
	"""Finds all aways scores by team and by games, 
	puts each game score into a list for analysis
	"""

	cur = nba.aggregate([{"$match": {"team": team}}, 
					     {"$match": {"h_a": "@"}},
					     {"$group": {"_id": {"scores": "$h_a"}, 
					     team: {"$push": "$s"} }}
					     ])

	new_cur = cur['result'][0][team]
	new_cur = filter(None, new_cur)
	return new_cur

# list of each teams score by game 
# split up by home and away

atl_away = a_scores('atl')
atl_home = h_scores('atl')

tor_away = a_scores('tor')
tor_home = h_scores('tor')

chi_away = a_scores('chi')
chi_home = h_scores('chi')

cle_away = a_scores('cle')
cle_home = h_scores('cle')

wsh_away = a_scores('wsh')
wsh_home = h_scores('wsh')

mil_away = a_scores('mil')
mil_home = h_scores('mil')

mia_away = a_scores('mia')
mia_home = h_scores('mia')

bkn_away = a_scores('bkn')
bkn_home = h_scores('bkn')

cha_away = a_scores('cha')
cha_home = h_scores('cha')

det_away = a_scores('det')
det_home = h_scores('det')

ind_away = a_scores('ind')
ind_home = h_scores('ind')

bos_away = a_scores('bos')
bos_home = h_scores('bos')

orl_away = a_scores('orl')
orl_home = h_scores('orl')

phi_away = a_scores('phi')
phi_home = h_scores('phi')

ny_away = a_scores('ny')
ny_home = h_scores('ny')

gs_away = a_scores('gs')
gs_home = h_scores('gs')

mem_away = a_scores('mem')
mem_home = h_scores('mem')

hou_away = a_scores('hou')
hou_home = h_scores('hou')

por_away = a_scores('por')
por_home = h_scores('por')

dal_away = a_scores('dal')
dal_home = h_scores('dal')

lac_away = a_scores('lac')
lac_home = h_scores('lac')

sa_away = a_scores('sa')
sa_home = h_scores('sa')

okc_away = a_scores('okc')
okc_home = h_scores('okc')

no_away = a_scores('no')
no_home = h_scores('no')

phx_away = a_scores('phx')
phx_home = h_scores('phx')

utah_away = a_scores('utah')
utah_home = h_scores('utah')

den_away = a_scores('den')
den_home = h_scores('den')

sac_away = a_scores('sac')
sac_home = h_scores('sac')

lal_away = a_scores('lal')
lal_home = h_scores('lal')

min_away = a_scores('min')
min_home = h_scores('min')

def calculate_score(data, z):
    # remove outliers
    # extract data between lower and upper quartile
    data.sort()
    lowerq = int((len(data))/4)
    #change from 3 to 4 adds an extra game to the upper
    upperq = lowerq * 3 + 2
    newdata = [data[i] for i in range(lowerq,upperq)]
    # fit Gaussian using MLE
    mu = round(numpy.mean(newdata),2)
    sigma = round(numpy.std(newdata),2)
    #compute x that corresponds to standard score z
    x = math.ceil(mu + (z * sigma))
    y = math.floor(mu - (z * sigma))
    return x,y,mu,sigma,newdata

def ss(data):
	"""sum of squares"""
	mu=numpy.mean(data)
	return sum([(x-mu)**2 for x in data])

def combine_score(away, home):
	"""if one team played more games on the home or road and it was different
	then the other team then this function will add the rolling mean to the team
	that needed it to make the amount of games played the same
	"""
	if len(home) > len(away):
		return map(sum, itertools.izip_longest(away, home, fillvalue=int(round(numpy.mean(away)))))
	elif len(home) < len(away):
		return map(sum, itertools.izip_longest(away, home, fillvalue=int(round(numpy.mean(home)))))
	elif len(home) == len(away):
		return map(sum, itertools.izip_longest(away, home))

def total_combinations(away, home):	
	"""This will add all combinations of home + away scores
	makes for a solid mean but lowers the std
	"""
	total = []
	for com in itertools.product(away, home):
		x = sum(com)
		total.insert(0,x)
	return len(total), round(numpy.mean(total),2), round(numpy.std(total),2), round(numpy.median(total),2)

def matchup(n1, away, n2,home):
	away.sort()
	home.sort()
	# sp2 = (ss(away)+ss(home))/(len(away)+len(home))
	# stdp = numpy.sqrt(sp2)
	print "#######   " + n1.upper() + " away"
	print away
	print calculate_score(away, 1.65)
	print len(away)
	print "avg: ",round(numpy.mean(away),2)
	print "std: ", round(numpy.std(away),2)
	print "Under: ", math.ceil(numpy.mean(away) + numpy.std(away) * .85)
	print "Over: ",  math.floor(numpy.mean(away) - numpy.std(away) * .85)
	print "|--------------------------------------|"
	print "########   " + n2.upper() + " home"
	print home
	print calculate_score(home, 1.65)
	print len(home)
	print "avg: ", round(numpy.mean(home),2)
	print "std: ", round(numpy.std(home),2)
	print "Under: ", math.ceil(numpy.mean(home) + numpy.std(home) * .85)
	print "Over: ",  math.floor(numpy.mean(home) - numpy.std(home) * .85)
	print "|--------------------------------------|"
	print total_combinations(away, home)[0]
	print combine_score(away, home)
	print calculate_score(combine_score(away,home), 1.65)
	print numpy.mean(combine_score(away, home))
	print "Game_Total: ", total_combinations(away, home)[1], total_combinations(away, home)[3]
	print "STD: ", total_combinations(away, home)[2]
	print "Game_Under: ", math.ceil(total_combinations(away,home)[1] + (total_combinations(away,home)[2] * .85))
	print "Game_Over: ", math.floor(total_combinations(away,home)[1] - (total_combinations(away,home)[2] * .85))
	print "Actual Game Score: "
	print "Game Totals: "
	print ""
	


# make the daily matchups and run
print matchup('okc', okc_away, 'chi', chi_home)
print matchup('dal', dal_away, 'por', por_home)




