# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 08:32:38 2021

@author: DaveAstator
"""
import math
import numpy as np

#converts literals to dict calls.
def litToDict(st,dictName='vd'):
    if type(st) != str:
        st=str(st)

    st2= '_'+st+'_'
    res =''
    for i in range(len(st)):
        c= st2[i+1]
        if c.isalpha():
            if not (st2[i].isalpha() or st2[i+2].isalpha()):
               res = res + dictName+'["'+c+'"]' 
               continue
        res = res + c
    return res
        
#main function that uses iterator definitions
# for now it uses list of lists [var name, from, to, step]
def Iterate(iterList, output, trailIndex={}, cypher = 'mMs'):
    selfIter=iterList[0]
    selfName=selfIter[0]
    
    if selfName not in output:
        output[selfName]=[]
    print(output)

  """  iterParams = {}
    minId = cypher.find('m')
    maxId = cypher.find('M')
    stepId = cypher.find('s')
    cntId = cypher.find('c')
"""
    low = litToDict(selfIter[1],'trailIndex')
    high = litToDict(selfIter[2],'trailIndex')
    step = litToDict(selfIter[3],'trailIndex')
    print(low,high,step)
        
    low=eval(low)
    high=eval(high)
    step=eval(step)
    print(low,high,step)
    
    rng = high-low
    count = math.ceil(rng/step)+1
    print("cnt rng",rng,count)
    
    if len(iterList) == 1:
        for itr in np.linspace(low,high,count):
            trailIndex[selfName]=itr
            print(trailIndex)       
            
            #write index since we are at final iterator
            print(trailIndex)
            for k in trailIndex.keys():
                output[k].append(trailIndex[k])
    
    # there are more nested iterators, so go in.
    else:
        for itr in np.linspace(low,high,count):
            trailIndex[selfName]=itr
            Iterate(iterList[1:],output,trailIndex)
        
def TEST_Iterate():
    construct=[
    ['u',1,5,0.3],
    ['v','u','u*2',0.3]]
    
    outp = {}
    outp['x']=[]
    Iterate(construct,outp)    
        
def CalculateFunctions(funcList,indexDict):
    for k in indexDict.keys():
        indexDict[k]=np.asarray(indexDict[k])
    for f in funcList:
        varname=f[0]
        func=f[1]
        indexDict[varname] = eval(litToDict(func,'indexDict'))
    return indexDict
        
def TEST_CalcFunc():
        CalculateFunctions([['z','1+x']],{"x":[1.2,4]})

# PUBLIC API
        
def GenerateFuncValues(construct):
    iters=[]
    funcs=[]
    for e in construct:
        if len(e) >2:
            iters.append(e)
        else:
            funcs.append(e)
    indexes={}
    Iterate(iters,indexes)
    return CalculateFunctions(funcs,indexes)

def GenerateUniformFuncValues(construct):
    iters=[]
    funcs=[]
    for e in construct:
        if len(e) >2:
            iters.append(e)
        else:
            funcs.append(e)
            
    shape = [i[-1] for i in iters]
    print(shape)
    result = np.zeros(shape)
    indexes={}
    Iterate(iters,indexes)


f=np.zeros([1,2,3])

def TEST_Uniform():
    construct=[
        ['u',1,5,5],
        ['v','u','u*2',7],
        ['x','u+v'],
        ['y','x/4'],
        ['c','x*y']
        ]
    GenerateUniformFuncValues(construct)
    
def TEST_Construct():
    #Apparently this works!
    #range cypher is min, max, stepsize
    construct=[
        ['u',1,5,0.3],
        ['v','u','u*2','u/2'],
        ['x','u+v'],
        ['y','x/4'],
        ['c','x*y']
        ]
    
    rr= GenerateFuncValues(construct)
    rr2= GenerateUniformFuncValues(construct,3)
    construct=[
        ['x',0,10,1],
        ['y','pow(x,2)'],
        ]
    GenerateFuncValues(construct)

def FullTEST():
    TEST_Iterate()
    TEST_CalcFunc()
    TEST_Construct()


r=10-5
step = 1
cnt = r/step+1

np.linspace(10,5,6)