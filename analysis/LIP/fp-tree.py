import pickle

class treeNode :
    def __init__(self,nameValue,numOccur,parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
    def inc (self,numOccur):
        self.count += numOccur
        
    def disp(self,ind = 1):
        print(' '*ind,self.name,'  ',self.count)
        for child in list(self.children.values()):
            child.disp(ind+1)

def createTree(dataSet,minSup=1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item,0)+ dataSet[trans]
    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:
            del(headerTable[k])  
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0 : return None,None
    for k in headerTable:
        headerTable[k] = [headerTable[k],None]
    retTree = treeNode('Null Set',1,None)
    for tranSet ,count in list(dataSet.items()):
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(list(localD.items()),key = lambda p:p[1],reverse = True)]
            # print orderedItems
            updateTree(orderedItems,retTree,headerTable,count)
    return retTree,headerTable

def updateTree(items,inTree,headerTable,count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0],count,inTree)
        if headerTable[items[0]][1] ==None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)
        
def updateHeader(nodeToTest,targetNode):
    while (nodeToTest.nodeLink !=  None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode
    
def loadSimpDat(loadPath):
    simpDat = []
    # simpDat = [['r', 'z', 'h', 'j', 'p'],
    #            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
    #            ['z'],
    #            ['r', 'x', 'n', 'o', 's'],
    #            ['y', 'r', 'x', 'z', 'q', 't', 'p'],
    #            ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    GoodDataFile = open(loadPath, 'U')
    readline = GoodDataFile.readlines()
    for line in readline :
        dat_line = []
        line = line.split()
        line = [w.lstrip("/x") for w in line]
        for w in line:
            if len(w)>1 and (w[-2:] in ["/d", "/zg", "/a", "/v"] or w[-3:] in ["/zg"]):
                dat_line.append(w)
                # print w
        # print dat_line
        simpDat.append(dat_line)
    return simpDat

def saveDat(freqItems, savePath):
    savefile = open(savePath, 'wb')
    pickle.dump(freqItems, savefile)
    savefile.close()
    return 0

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

def ascendTree(leafNode,prefixPath):
    if leafNode.parent !=None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat,treeNode):
    condPats={}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree,headerTable,minSup,preFix,freqItemList):
    # bigL = [v[0] for v in sorted(list(headerTable.items()),key=lambda p:p[1])]
    bigL = [v[0] for v in sorted(list(headerTable.items()), key=lambda p:p[1][0])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        # freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree,myHead = createTree(condPattBases, minSup) 
        newFreqList = frozenset([word for word in newFreqSet])
        # print newFreqList
        # print "condPattBases", condPattBases
        # freqItemList[newFreqList] = freqItemList.get(newFreqList, 0) + sum([cnt[1] for cnt in condPattBases.items()])
        for key in list(condPattBases.keys()):
            tmpItemList = newFreqList | key
            freqItemList[tmpItemList] = freqItemList.get(tmpItemList, 0) + condPattBases[key]
            # freqItemList[newFreqList.add(key)] = freqItemList.get(newFreqList.add(key), 0) + condPattBases[key]
        if myHead!= None:
            
            # print 'conditional tree for: ',newFreqSet
            # myCondTree.disp(1) 
            # for row in freqItemList.keys() :
            #     # print "\n"
            #     if '\xe4\xb8\x8d\xe9\x94\x99/a' in row and '\xe5\xbe\x88/zg' in row:
            #         for col in row :
            #             print col
            #         print row
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

if __name__ == "__main__":
    simpDat = loadSimpDat("datasets\\lzq_split_good.txt")
    # simpDat = loadSimpDat("datasets\\lzq_split_bad.txt")
    # print simpDat
    initSet = createInitSet(simpDat)
    # print initSet
    myFPtree , myHeaderTab = createTree(initSet, 3)
    # print myHeaderTab
    myFPtree.disp()
    # print findPrefixPath('t', myHeaderTab['t'][1])
    freqItems = {}
    mineTree(myFPtree, myHeaderTab, 3, set({}), freqItems)
    # freqItems = sorted(freqItems.items(),key = lambda p:len(p[0]),reverse = False)
    print(freqItems)
    
    for key in list(myHeaderTab.keys()):
        if (key[-2:] in ["/d", "/zg", "/a", "/v"] or key[-3:] in ["/zg"]):
            freqItems[frozenset([key])] = myHeaderTab[key][0]
    
    max_freq = 0
    for key in list(freqItems.items()):
        if key[1] >= max_freq:
            max_freq = key[1]
    
    for key in list(freqItems.keys()):
        freqItems[key] = freqItems[key]*1.0/max_freq

    for row in list(freqItems.keys()) :
        print("\n")
        # if '\xe4\xb8\x8d\xe9\x94\x99/a' in row or '\xe5\xbe\x88/zg' in row:
        for col in row :
            print(col)
        print(row, freqItems[row])


    saveDat(freqItems, "GoodResultItems_lzq.pkl")
    # print len(freqItems)
    