import matplotlib.pyplot as plt

import decimal as Decimal
import datetime
#from database import *
#import database

#testi searcci databasesta
#device = "livingroom" # testing
#choice = "veek"
#dbsearch = ()
#device, dbsearch = choicev(device, choice)

def show_plot(humlist, datetimeline):
    figure = plt.figure()
    lengt = len(humlist)
    axes = figure.add_subplot(1,1,1)
    
    axes.bar(
        range(len(humlist)), # tsekataan pituus
        [humlist[i] for i in range (len(humlist))],#, # korkeus palkeille  for search in mariadb_search
        tick_label=[datetimeline[i] for i in range (len(datetimeline))] # for search1 in mariadb_search.. tää haku osaa nyt erotella listan eri objektit eikä haittaa vaikka hakujen määrä kasvaa
        
    
    )
    plt.xticks(rotation=90)
    plt.show()
    #print(search)
    #print(search1)
    return 




def show_graphics(dbsearch, device, usrchoice, userdate):
    templist = []
    humlist = []
    datetimeline = []
    #usrchoice = 0
    #dbsearch.sort(key=id)
    #print(dbsearch) testing
    #print(len(dbsearch))

    #i = len(dbsearch)
    #print(i) ### tähän if lause jos selaillaan siilin juoksuja!!
    for i in range (len(dbsearch)):
        #ranke = list(filter(lambda x:11 in x, dbsearch))
        #print(ranke)
        datatemp = ""
        templist = dbsearch[i] # eli joka tuplesya index 0
        humlist.append(templist[usrchoice]) # tää toimii. ny tulee lämmöt grafiikkaan
        datetemp = templist[userdate]
        print(userdate)
        dateformat = '%m-%d %H:'
        datatemp1 = datetime.datetime.strftime(datetemp, dateformat)
        datetimeline.append(datatemp1) # here you have to format away year and min and sec. etc
        #humlist.append(i[1])
        #datetime.append(i[2])
        #print(templist, datetimeline) testing
    
    
    show_plot(humlist, datetimeline)

