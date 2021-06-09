# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:01:39 2021

@author: DaveAstator
"""

import matplotlib.pyplot as plt;
import numpy as np;
            
def UniformDots2D(x,y):
    low = np.min(np.concatenate((x,y)))
    high = np.max(np.concatenate((x,y)))
    plt.xlim(low, high)
    plt.ylim(low, high)
    plt.scatter(x,y)
    
def UniformLine2D(x,y):
    low = np.min(np.concatenate((x,y)))
    high = np.max(np.concatenate((x,y)))
    plt.xlim(low, high)
    plt.ylim(low, high)
    plt.plot(x,y)
    
def ValOrNone(key,dic):
    if key in dic:
        return dic[key]
    else:
        return None
    
def UniformDots3D_p(plotData):
    c = ValOrNone('c' , plotData);
    s = ValOrNone('s' , plotData);
    x = ValOrNone('x' , plotData);
    y = ValOrNone('y' , plotData);
    z = ValOrNone('z' , plotData);
    a = ValOrNone('a' , plotData);
    UniformDots3D(x,y,z,c,s,a)

def UniformLine3D_p(plotData):
    c = ValOrNone('c' , plotData);
    s = ValOrNone('s' , plotData);
    x = ValOrNone('x' , plotData);
    y = ValOrNone('y' , plotData);
    z = ValOrNone('z' , plotData);
    a = ValOrNone('a' , plotData);
    UniformLine3D(x,y,z,c,s,a)
    
def UniformDots3D(x,y,z,c = None, s = None, a = 1):
    print('3d point plot',s)
    
    if s == None:
        s = plt.rcParams['lines.markersize'] ** 2
        
    if a == None:
        a = 1

        
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    low = np.min(np.concatenate((x,y,z)))
    high = np.max(np.concatenate((x,y,z)))
    
    ax.set_xlim(low, high)
    ax.set_ylim(low, high)
    ax.set_zlim(low, high)
    ax.set_box_aspect((1, 1, 1)) 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ax.scatter(x,y,z, c=c, s=s, alpha = a)
    plt.show()  
    
def UniformLine3D(x,y,z,c = None, s = None, a = 1):
    print('3d point plot',s)
        
    if a == None:
        a = 1

        
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    low = np.min(np.concatenate((x,y,z)))
    high = np.max(np.concatenate((x,y,z)))
    
    ax.set_xlim(low, high)
    ax.set_ylim(low, high)
    ax.set_zlim(low, high)
    ax.set_box_aspect((1, 1, 1)) 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ax.plot(x,y,z, c=c, alpha = a)
    plt.show()

def toPlotData(data, cypher):
    valDict = {}
    bins = cypher.split(',')
    row = 0

    subDimId = 0
    for b in bins:
        if len(bins) ==1:
            bvals = data
        else:
            bvals = data[row]
        row = row + 1
    
        for dim in b:
            if type(bvals) is list:        # curren bin looks at list
                if type(bvals[0]) is list: # curren bin consist of lists
                    valDict[dim] = [p[subDimId] for p in bvals]
                else:                      # curren bin consists of values
                    valDict[dim] = bvals
                    #valDict[dim] = [p for p in bvals]
                    #valDict[dim] = bvals[subDimId]
            else:                          # curren bin looks at a value
                valDict[dim] = bvals       # essentialy a value
                
            subDimId = subDimId + 1
        subDimId = 0
    return valDict


#new list cypher snytax: i:xyi:z
# for example [1,2,[3,4,5]] -:xy-:z

def addNestedToData(nest,cypher,valDict = {},trailNames='',trailVals=[]):
    for c in cypher.replace(':',''):
        if c not in valDict:
            valDict[c]=[]
    
    split = cypher.find(':')
    if (split < 1):
        print('endpoint semantic',cypher)
        nestSemantic = cypher
        
        if len(nestSemantic) == 1: #
            print('len sem ==1',nest)
            valDict[nestSemantic].append(nest)
                
        else: #nest is ndim list
            print('endpoint nest',nest)
            eggidx=0
            
            #write values from nest
            for n,v in zip(nestSemantic,nest):
                valDict[n].append(v)
        
        #write trailing values
        for n,v in zip(trailNames,trailVals):
            valDict[n].append(v)
            
        
    else:
        propSemantic = cypher[:split-1]
        idxSemantic = cypher[split-1]
        nestSemantic = cypher[split+1:]
        splitIndex = len(propSemantic)
        
        if splitIndex>0:  # add inner props to index and continue
            propValues = nest[:splitIndex]        
            nextNest = nest[splitIndex]
            
            newTrailNames = trailNames + propSemantic    
            newTrailVals = trailVals + propValues
            print('newTrailNames and vals',newTrailNames, '---', newTrailVals)
            print('recusing into', nextNest)
            addNestedToData(nextNest,
                            idxSemantic+':'+nestSemantic,
                            valDict,
                            newTrailNames,
                            newTrailVals)

        else: # iterate over index
            newTrailNames = trailNames + idxSemantic            
            idx = 0    
            for egg in nest:
                newTrailVals = trailVals + [idx]
                print('newTrailNames and vals',newTrailNames, '---', newTrailVals)
                nextNest = egg
    
                idx = idx + 1
                print('recursing egg',nextNest,nestSemantic)
                
                addNestedToData(nextNest, nestSemantic, valDict, newTrailNames, newTrailVals)
    return valDict

# ------------ PUBLIC API -------------

def dots(data, cypher):
    valDict = toPlotData(data,cypher)
    
    ndim = int('x' in cypher) + int('y' in cypher) + int('z' in cypher)

    if ndim <= 1:
        plt.plot(valDict['x'])
    if ndim == 2:
        UniformDots2D(valDict['x'],valDict['y'])
    if ndim == 3:
        UniformDots3D_p(valDict)

def line(data,cypher):
    valDict = toPlotData(data,cypher)
    ndim = int('x' in cypher) + int('y' in cypher) + int('z' in cypher)

    if ndim <= 1:
        plt.plot(valDict['x'])
    if ndim == 2:
        UniformLine2D(valDict['x'],valDict['y'])
    if ndim == 3:
        UniformLine3D_p(valDict)
    
    
# ---------- TESTING -----------

import math
pt = []
for z in range (0,100):
    pt.append([math.cos(z)*5,math.sin(z)*10,z])

pt=[]
for u in range (0,5):
    for v in range (0,10):
        for w in range (0,10):
            pt.append([u+math.sin(w),v+cos(u),w+v*0.1,u])
dots(pt,'xyzs')
            

d=np.array([[1, 2, 3], [4, 5, 6]], np.int32)

addNestedToData(d,'y:x:h',{})

data = [[[1,2,3],[2,3,20],[5,5,11]],[0.1,0.2,0.8],8]
#dots(data,'zxy,c,s')
#line(data,'xyz,-,s')
dots(pt,'xyzs')




addNestedToData([[11,21,31],[41,51,61]],'x:y:h',{})    

data=[
 [1,2,[-5,-6]],
 [11,12,[-15,-16]]
 ]

addNestedToData(data,'p:xyk:s',{})







            
    