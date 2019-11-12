import random
import collections

kuotaDosen=[5,5,6,6,3,5]
jmlpopulasi=10
target=[5,0,3,4,2,4,5,1,5,0,0,4,5,4,2,3,3,4,1,1,0,4,1,2,3,5,0,1,3,2]

def populasi(jml,pnjngtarget,kuota):
    populasi=[['' for x in range(pnjngtarget)] for y in range(jml)]
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

# crossover semua parent
def crossover(populasi, crossoverPoint):
    # crossoverPoint : array yg isinya point crossover
    # misal 2, 4, 5, 9
    #        v     v  v           v            v     v  v           v 
    # [-][-][-][-][-][-][-][-][-][-] -> [-][-][+][+][-][+][+][+][+][-]
    # [+][+][+][+][+][+][+][+][+][+] -> [+][+][-][-][+][-][-][-][-][+]
    offsprings = []
    random.shuffle(populasi)
    if(len(crossoverPoint) % 2 == 1):
        crossoverPoint.append(len(populasi[0]))
    for i1 in range(len(populasi)):
        for i2 in range(len(populasi)):
            if(i1 != i2):
                # copy array
                offspring1 = list(populasi[i1])
                offspring2 = list(populasi[i2])
                for j in range(0, len(crossoverPoint), 2):
                    for k in range(crossoverPoint[j], crossoverPoint[j+1]):
                        offspring1[k], offspring2[k] = offspring2[k], offspring2[k] # diubah per crossover point
                offsprings.append(offspring1)
                offsprings.append(offspring2)
    random.shuffle(offsprings)
    return offsprings[:jmlpopulasi]

def mutation(populasi):
    # iterasi per individu
    for individu in populasi:
        genPos = getGenPotision(individu) # posisi per gen tiap individu
        # iterasi tiap gen
        for i in range(len(kuotaDosen)):
            # jika gen lebih banyak dari kuota dosen maka akan diubah ke yang kurang
            if(len(genPos[i]) > kuotaDosen[i]):
                selisih = len(genPos[i]) - kuotaDosen[i]
                # diubah sebanyak lebihnya
                for _ in range(selisih):
                    random.shuffle(genPos[i])
                    inx = genPos[i].pop() # index random yang diubah
                    val = getRandomIndex(genPos) # dosen yang kuotanya kurang
                    individu[inx] = val # diubah
                    genPos[val].append(inx) # update posisi gen
    return populasi

def getGenPotision(individu):
    # mendapatkan array 2D yang berisi posisi dari nilai gen
    # misal 0 ada di index 2, 3, 5 maka hasilnya
    # genPos[0] = [2, 3, 5]
    genPos = [[] for i in range(len(kuotaDosen))]
    for i in range(len(individu)):
        genPos[individu[i]].append(i)
    return genPos

def getRandomIndex(genPos): # mendapatkan dosen yang kuotanya kurang
    arr = [] # array isinya index yang kuota kurang
    for i in range(len(kuotaDosen)):
        if(len(genPos[i]) < kuotaDosen[i]):
            arr.append(i)
    random.shuffle(arr) # dishuffle
    return arr.pop()

def updateGeneration(offsprings, parents):
    fitOffsprings = fitnesspopulasi(offsprings, target) # fitness offspring
    fitParents = fitnesspopulasi(parents, target) # fitness parent
    pBest = max(fitParents) # fitness terbaik parent
    oWorst = min(fitOffsprings) # fitness terburuk offspring
    if(oWorst < pBest):
        offsprings[fitOffsprings.index(oWorst)] = parents[fitParents.index(pBest)]
    return offsprings

population=populasi(jmlpopulasi, len(target),kuotaDosen)
fitness=fitnesspopulasi(population, target)
for i in range(len(population)):
    print("Kromosom",[i+1],":",population[i],"Fitness:", fitness[i])
parents=selectionparents(fitness,population,10)
offsprings = mutation(crossover(parents, [3, 17]))
parents = updateGeneration(offsprings, parents)

for i in parents:
    c = collections.Counter(i)
    print(i,dict(c))
