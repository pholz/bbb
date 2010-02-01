from math import sqrt

def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            #flip item and person
            result[item][person]=prefs[person][item]
    return result
    
def sim_distance(prefs, person1, person2):
    # there is a typo in the book for this function

    si={} #shared items
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    if len(si) == 0:
        return 0


    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in si])


    return 1/(1+sqrt(sum_of_squares))

def sim_pearson(prefs, person1, person2):

    si={} #shared items
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    n = float(len(si))

    if n==0: return 0 # 0 means no linear relationship b/t two variables

    #add up ratings each critic made for common films
    sum1 = sum([prefs[person1][item] for item in si])
    sum2 = sum([prefs[person2][item] for item in si])

    #sum the squares of each critics ratings
    sumSq1 = sum([pow(prefs[person1][item], 2) for item in si])
    sumSq2 = sum([pow(prefs[person2][item], 2) for item in si])

    #sum the products of each critics ratings
    pSum = sum([prefs[person1][item] * prefs[person2][item] for item in si])

    #calculate pearson correlation
    numerator = pSum-((sum1*sum2)/n)
    denominator = sqrt((sumSq1 - pow(sum1, 2)/n) * (sumSq2 - pow(sum2, 2)/n))
    if denominator == 0: return 0

    else:
        pearson = numerator/denominator
        return pearson
    
def topMatches(prefs, person, n=5, similarityMetric=sim_distance):
    #compare:
    #topMatches(critics, 'Lisa Rose', similarityMetric=sim_pearson)
    #topMatches(critics, 'Lisa Rose', similarityMetric=sim_distance)
    #How are they different? Which do you think is more intuitive?

    #apply similarity metric to the subject and iterate against every other member of the set
    scores = [(similarityMetric(prefs, person, other), other)
              for other in prefs if other != person]

    #sort the list and reverse so largest scores appear at the beginning of the list
    scores.sort()
    scores.reverse()
    return scores[0:n] #return the top number of scores requested


def calculateSimilarItems(prefs, n=10):
    result={}
    itemPrefs=prefs#transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        c+=1
        if c%100==0: 
            print "%d / %d" % (c, len(itemPrefs))
        scores=topMatches(itemPrefs, item, n=n, similarityMetric=sim_distance)
        result[item] = scores
    return result
    
def getRecommendedItems(prefs, itemMatch, user):
    userRatings=prefs[user]
    scores={}
    totalSim={}

    #loop over items rated by this user
    for (item, rating) in userRatings.items():
        #loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:

            #ignore if user already rated item
            if item2 in userRatings: continue

            #weighted sum of ratings * similarity
            scores.setdefault(item2, 0)
            scores[item2]+=similarity*rating

            #sum similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2]+=similarity

    #divide each total score by total weighting to get an average
    #this will only work correctly in a large database with lots of overlap between
    #what users have rated
    rankings = [(score/totalSim[item], item) for item, score in scores.items()]

    #taking the square root of the total similarities seems to give expected results for smaller sparser data
    #you should evaluate both approaches (or design your own!)
    #rankings = [(score/sqrt(totalSim[item]), item) for item, score in scores.items()]

    #return rankings from high to low
    rankings.sort()
    rankings.reverse()
    return rankings
    
