import random

kuotaDosen=[5,5,6,6,3,5]
jmlpopulasi=10
target=[5,0,3,4,2,4,5,1,5,0,0,4,5,4,2,3,3,4,1,1,0,4,1,2,3,5,0,1,3,2]

def populasi(jml,pnjngtarget,kuota):
    populasi=[['' for x in range(pnjngtarget)]for y in range(jml)]
    for i in range(jml):
        j=0
        while j < pnjngtarget:
            x=random.randint(0,len(kuota)-1)
            if populasi[i].count(x)<kuota[x]:
                populasi[i][j]=x
                j+=1
    return populasi

def fitnesschromosome(kromosom,target):
    fitnesschro=len(target)
    for i in range(len(target)):
        if kromosom[i]!=target[i]:
            fitnesschro-=1
    return fitnesschro

def fitnesspopulasi(populasi,target):
    fitnesspop=[0 for y in range(len(populasi))]
    for i in range(len(fitnesspop)):
        fitnesspop[i]=fitnesschromosome(populasi[i],target)
    return fitnesspop

def selectionparents(fit, populasi, matingpool):
    joinsorted=sorted(zip(fit,populasi), reverse=False)
    prob=[]
    kumulatif=[]
    parent=[]
    for i in range(len(populasi)):
        prob.append(joinsorted[i][0]/sum(fit))
        if i==0:
            kumulatif.append(prob[i])
        else:
            kumulatif.append(kumulatif[i-1]+prob[i])
        #print("kromosom",[i+1],":",joinsorted[i][1])
        #print("fitness:",joinsorted[i][0],"; prob:",prob[i],"; cumpol:",kumulatif[i])
    r=random.uniform(0,(1/matingpool))
    j=0
    saveindex=[]
    while j<matingpool:
        #print("iterasi ke ", j+1)
        #print("random: ", r)
        tmp=[]
        if j==0:
            for i in range(len(kumulatif)):
                if kumulatif[i]>r:
                    tmp.append(kumulatif[i])
        else:
            for i in range(len(kumulatif)):
                if kumulatif[i]>r:
                    tmp.append(kumulatif[i])
        r=r+(1/matingpool)
        if tmp:
            saveindex.append(kumulatif.index(min(tmp)))
        j+=1
    saveindex=list(set(saveindex))
    for i in range(len(saveindex)):
        parent.append(joinsorted[saveindex[i]][1])
    return parent

#def crossover(parent, n):
 #   if len(parent)>=1 and len(parent)<=2:

        
    

population=populasi(jmlpopulasi, len(target),kuotaDosen)
fitness=fitnesspopulasi(population, target)
for i in range(len(population)):
    print("Kromosom",[i+1],":",population[i],"Fitness:", fitness[i])
parents=selectionparents(fitness,population,10)
print(parents)
                            
               
