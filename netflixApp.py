from netflix import *
import os
import sys
import cPickle

mode_db = False

if len(sys.argv) < 2:
    print 'missing arguments. syntax is: "python netflixApp.py mode person-id" mode is "builddb" or "recommend"'

mode = sys.argv[1]
if mode == 'builddb':
    mode_db = True

mov = '1'
if len(sys.argv) == 3:
    mov = sys.argv[2]
print mov

ratings = {}

files = os.listdir('training_set')[0:500]
ratings = {}

f_movietitles = open('movie_titles.txt', 'r')

id_title = {}
for line in f_movietitles.readlines():
    line = line.strip('\n')
    id_year_title = line.split(',')
    id_title[id_year_title[0]] = id_year_title[2]

if True:
    for file in files:
        f = open('training_set/' + file, 'r')
        print 'reading ' + file + '...'
        firstline = f.readline()
        movie_id = firstline.strip(':\n')
    
        ratings[movie_id] = {}
    
        for line in f.readlines():
            line = line.strip('\n')
            customer_rating_date = line.split(',')
            ratings[movie_id][customer_rating_date[0]] = int(customer_rating_date[1])#, customer_rating_date[2])
        
   # print ratings
#print 'top matches for ' + id_title[mov]


# itembased
#items = calculateSimilarItems(ratings)
#nameMatches = map(lambda dist_mid: (dist_mid[0], id_title[dist_mid[1]]), items[mov])
#print nameMatches
#print items
#matches = getRecommendedItems(ratings,items,mov)



# standard
#matches = topMatches(ratings,mov,n=500,similarityMetric=sim_pearson)
#nameMatches = map(lambda dist_mid: (dist_mid[0], id_title[dist_mid[1]]), matches)
#print nameMatches


if mode_db:
    itemsim = calculateSimilarItems(ratings,n=500)
    f_itemdb = open('itemdb','w')
    print 'writing item-db to disk'
    cPickle.dump(itemsim,f_itemdb)
else:
    f_itemdb = open('itemdb','r')
    items = cPickle.load(f_itemdb)
    matches = getRecommendedItems(ratings,items,'469152') # picking some user id
    nameMatches = map(lambda dist_mid: (dist_mid[0], id_title[dist_mid[1]]), matches)
    print nameMatches
    