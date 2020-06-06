from Methods import *
import pandas as pd



c=Country()
s=States()

c.start()
s.start()

wishMe()

c.join()
s.join()
df=pd.concat([c.countriesData,s.statesData])

while True:

     query = takeCommand()
     if Exit(query):
         print("Bye")
         speak("Bye")
         break
     places=find_place(query,s,c)

     for i in places:
         p,q,r,t=df.loc[i,:]

         print('Searching Cases for {}...'.format(i))
         speak('Searching Cases for {}...'.format(i))
         print("{} have Total {} corona cases in which {} are still active , {} have recovered and {} are dead.".format(i,p,q,r,t))
         speak("{} have Total {} corona  cases in which {} are still active , {} have recovered and {} are dead.".format(i,p,q,r,t))





