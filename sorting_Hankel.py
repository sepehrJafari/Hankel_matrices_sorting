import random
import time
import timeit
import sys



def isSublist(lst1, lst2):
    ls=[x for x in lst1 if x in lst2 ]
    return len(ls)==len(lst1)


# randomList and randomChain creat a random Chain

def randomList(listLenghth, n,seed):
    random.seed(seed+1)
    label = random.choice([[1, n], [1, n - 1], [2, n], [2, n - 1]])
    return [label, sorted(random.sample(range(label[0], label[-1] + 3), listLenghth))]

def randomSequences(listLenghth, n,seed):
    random.seed(seed+2)
    chain = []
    while chain==[]:
        l1 = randomList(listLenghth, n, seed)
        l = l1[1]
        label = l1[0]
        if len(l) > 1:
            for i in range(0, len(l) - 1):
                if l[i + 1] > l[i] + 1:
                    chain.append(l[i])
                else:
                    continue
        else:
            chain = l
        if chain!=[]:
            return [label, chain]
        else:
            continue

# here we define the orders we need on chains

def lexOrder(list_1, list_2):
    for i in range(0, min(len(list_1), len(list_2))):
        if list_1[i] < list_2[i]:
            return True
        elif list_1[i] > list_2[i]:
            return False
        else:
            if len(list_1) >= len(list_2):
                return True
            else:
                return False


def dLexOrder(list_1, list_2):
    if len(list_1) > len(list_2):
        return True
    elif len(list_1) == len(list_2) and lexOrder(list_1, list_2):
        return True
    else:
        return False

# This function defines the order on lables: [[1, n], [1, n - 1], [2, n], [2, n - 1]]

def labelOrder(lable_1,lable_2):
    if lable_1[0]<lable_2[0]:
        return True
    elif lable_1[0]==lable_2[0] and lable_1[1]<lable_2[1]:
        return True
    else:
        return False

# The following gives a pair of sequences after ordering them


def arrangeSequences(sequence_1,sequence_2):
    if sequence_1[0]==sequence_2[0]:
        if dLexOrder(sequence_1[1],sequence_2[1]):
            return [sequence_1,sequence_2]
        else:
            return [sequence_2,sequence_1]
    else:
        if labelOrder(sequence_1[0],sequence_2[0]):
            return [sequence_1,sequence_2]
        else:
            return [sequence_2,sequence_1]



def sequenceOrder(sequence_1,sequence_2):
    if arrangeSequences(sequence_1,sequence_2)==[sequence_1,sequence_2]:
        return True
    else:
        return False

# in the following we chack the sorting conditions

# this is the interval defined in Num

def intervalNum(chain):
    l = [[x-1,x] for x in chain[1:]]
    return [item for sublist in l for item in sublist]

# the following are what I call as controller functions in my thesis

def delta (sequence_1,sequence_2):
    if len(sequence_1[1]) <= len(sequence_2[1]) and\
            sequence_2[0][-1] < sequence_1[1][-1]:
        return 1
    elif len(sequence_1[1]) > len(sequence_2[1]) and\
            sequence_1[0][-1] < sequence_2[1][-1]:
        return 1
    else:
        return 0

def omegaDiagonal (sequence_1,sequence_2):
    if len(sequence_1[1]) < len(sequence_2[1]):
        return len(sequence_1[1])-delta(sequence_1,sequence_2)
    else:
        return len(sequence_2[1])-1

def omegaColumn (sequence_1,sequence_2):
    if len(sequence_1[1]) <= len(sequence_2[1]):
        return len(sequence_1[1])-delta(sequence_1,sequence_2)
    else:
        return len(sequence_2[1])

def omegaAntiDiagonal (sequence_1,sequence_2):
    if len(sequence_1[1]) <= len(sequence_2[1]):
        return len(sequence_1[1])- 1
    else:
        return len(sequence_2[1]) - delta(sequence_1,sequence_2)


# the following fucntions check the definition of standard froms
'''in the following we see if a pair of seq jhas diagonal relations'''

def diagonalRelation(sequence_1,sequence_2):
    sortPair = arrangeSequences(sequence_1,sequence_2)
    chain_1 = sortPair[0][1]
    chain_2 = sortPair[1][1]
    length_2 = len(chain_2)
    for i in range(0,omegaDiagonal(sequence_1,sequence_2)):
        for j in range(i+1,length_2):
            if chain_1[i]>chain_2[j] and chain_1[i] not in intervalNum(chain_2[i:]):
                return True
    return False

def columnRelation(sequence_1,sequence_2):
    sortPair = arrangeSequences(sequence_1, sequence_2)
    chain_1 = sortPair[0][1]
    chain_2 = sortPair[1][1]
    if not diagonalRelation(sequence_1,sequence_2):
        for i in range(0, omegaColumn(sequence_1, sequence_2)):
            if chain_1[i] > chain_2[i] and chain_1[i] not in intervalNum(chain_2[i:]):
                return True
    return False

# in the following we check the definition of anti diagonal relations.
# note that, in this adoptation, when a pair of seq has False value for antidiagonalRelation
#  we say it is a standard form

def antidiagonalRelation (sequence_1,sequence_2):
    sortPair = arrangeSequences(sequence_1, sequence_2)
    chain_1 = sortPair[0][1]
    chain_2 = sortPair[1][1]
    length_1 = len(chain_1)
    if not columnRelation(sequence_1,sequence_2):
        for j in range(0, omegaAntiDiagonal(sequence_1,sequence_2)):
            for i in range(j , length_1):
                if chain_2[j] > chain_1[i] and chain_2[j] not in intervalNum(chain_1[j:]):
                    return True
    return False

# the function buuble sort and gives an arranged table

def bubbleSort(table):
    for passnum in range(len(table)-1,0,-1):
        for i in range(passnum):
            if sequenceOrder(table[i+1],table[i]):
                temp = table[i]
                table[i] = table[i+1]
                table[i+1] = temp
    return table

# the following checks if a table is standard form

def isStandardPair(sequence_1,sequence_2):
    if not diagonalRelation(sequence_1,sequence_2) and not columnRelation(sequence_1,sequence_2) and \
            not antidiagonalRelation(sequence_1,sequence_2):
        return True
    else:
        return False


def isStandardTable(table):
    table=bubbleSort(table)
    for i in range(0, len(table) - 1):
        for j in range(i + 1, len(table)):
            if not antidiagonalRelation(table[i], table[j]):
                return True
            else:
                return False


# here we reduce a given table to a quasi sorted table
'''
the following function takes a pair of diagonal sequences (defined in my paper) and
gives the reduciton of the pair with respect to diagonal relations.
'''

def diagonalReduce(sequence_1,sequence_2):
    sortPair = arrangeSequences(sequence_1,sequence_2)
    chain_1 = sortPair[0][1]
    chain_2 = sortPair[1][1]
    h_index= 0
    k_index=len(chain_2)-1
    v_index=0
    if diagonalRelation(sequence_1,sequence_2):
        for i in range(omegaDiagonal(sequence_1, sequence_2) - 1, -1, -1):
            for j in range(k_index - v_index, i , -1):
                if chain_1[i] > chain_2[j]:
                    if v_index == 0 and chain_1[i] not in intervalNum(chain_2[i:]):
                        h_index, k_index, v_index = i, j, v_index + 1
                        if i==0:
                            chain_1[h_index - v_index + 1:h_index + 1], chain_2[k_index - v_index + 1:k_index + 1] = \
                                chain_2[k_index - v_index + 1:k_index + 1], chain_1[h_index - v_index + 1:h_index + 1]
                            return diagonalReduce(sequence_1, sequence_2)
                        break
                    elif v_index !=0:
                        v_index = v_index + 1
                        if i==0:
                            chain_1[h_index - v_index + 1:h_index + 1], chain_2[k_index - v_index + 1:k_index + 1] = \
                                chain_2[k_index - v_index + 1:k_index + 1], chain_1[h_index - v_index + 1:h_index + 1]
                            return diagonalReduce(sequence_1, sequence_2)
                        break
                elif v_index!=0:
                    chain_1[h_index - v_index + 1:h_index + 1], chain_2[k_index - v_index + 1:k_index + 1] = \
                        chain_2[k_index - v_index + 1:k_index + 1], chain_1[h_index - v_index + 1:h_index + 1]
                    return diagonalReduce(sequence_1,sequence_2)
    return [sequence_1,sequence_2]

def diagonalReduceTable(table):
    table = bubbleSort(table)
    for i in range(0, len(table) - 1):
        for j in range(i + 1, len(table)):
            if diagonalRelation(table[i],table[j]):
                newTable=diagonalReduce(table[i], table[j])
                table[i] , table[j] = newTable[0] , newTable[1]
                diagonalReduceTable(table)
            else:
                continue
    return table

def criticalSeq(table,list):
    bubbleSort(table)
    for i in range(0,len(table)-1):
        for j in range(i+1,len(table)):
            if diagonalRelation(table[i],table[j]):
                list.append((i, j))
                newList=diagonalReduce(table[i],table[j])
                table[i], table[j] = newList[0] , newList[1]
                return criticalSeq(table,list)
    return [table,list]

'''work on the above function'''


def makeTable(numberRows,numberIntegrers,seed):
    table = []
    while len(table)<numberRows:
        sequence_1 = randomSequences(20 , numberIntegrers,seed+len(table))
        sequence_2 = randomSequences(10 , numberIntegrers,seed+len(table))
        if sequence_1 not in table and sequence_2 not in table:
            table.append(sequence_1)
            table.append(sequence_2)
    return bubbleSort(table)


##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

start = timeit.default_timer()




def test(table):
    table = bubbleSort(table)
    for j in range(1, len(table)):
        if diagonalRelation(table[0], table[j]):
            newTable = diagonalReduce(table[0], table[j])
            table[0], table[j] = newTable[0], newTable[1]
        else:
            continue
    return table


counter=1
seed=1


# while counter<100:
#     seed=seed+1
#     print('the seed is:',counter+seed)
#     print('the counter is:', counter)
#     table=makeTable(10,60,counter+seed)
#     if not diagonalRelation(table[0],table[1]):
#         goodList=[]
#         badList=[]
#         print('=========================================')
#         for x in table:
#             print(x)
#         counter = counter + 1
#         seq=criticalSeq(table,[])[1]
#         goodList.append(seq[0])
#         for i in range(1,len(seq)-1):
#             if not lexOrder(seq[0],seq[i]):
#                 goodList.append(seq[i])
#             else:
#                 badList.append(seq[i])
#         print('this is seq')
#         for x in seq:
#             print(x)
#         print('this is good list')
#         for x in goodList:
#             print(x)
#         print('this is bad list')
#         for x in badList:
#             print(x)

# while counter<100:
#     seed=seed+1
#     print('the seed is:',counter+seed)
#     print('the counter is:', counter)
#     table=makeTable(5,50,counter+seed)
#     if not diagonalRelation(table[0],table[1]):
#         print('=========================================')
#         print('the seed is:', counter + seed)
#         print('the counter is:', counter)
#         for x in table:
#             print(x)
#         counter = counter + 1
#         print('this is d-sorted:')
#         table=diagonalReduceTable(table)
#         for x in table:
#             print(x)

# the seed is: 205
#
# table=[
# [[1, 50], [6, 9, 12, 16, 20, 22, 27, 30, 35, 40]],
# [[1, 50], [6, 9, 12, 17, 20, 44]],
# [[2, 49], [4, 6, 10, 13, 18, 20, 28 ,42,45]],
# [[2, 50], [5, 11, 14, 16, 18, 21, 24, 29, 31, 35,40,48]],
# [[2, 50], [5, 14, 18, 31, 35, 38, 46, 48]]
# ]
#
# seq=criticalSeq(table,[])
#
# for x in seq[1]:
#     print(x)
#
# print('----------------------------------')
#
# table=[
# [[1, 50], [6, 9, 12, 16, 20, 22, 27, 30, 35, 40]],
# [[1, 50], [6, 9, 12, 17, 20, 44]],
# [[2, 49], [4, 6, 10, 13, 18, 20, 28 ,42,45]],
# [[2, 50], [5, 11, 14, 16, 18, 21, 24, 29, 31, 35,40,48]],
# [[2, 50], [5, 14, 18, 31, 35, 38, 46, 48]]
# ]
#
# for x in table:
#     print(x)
# print('----------------------------------')
# table1=diagonalReduceTable(table)
#
#
# for x in table1:
#     print(x)



stopEnd = timeit.default_timer()

print(stopEnd - start)

print("total time is:",(stopEnd - start)/60 , "minutes")
print("each reduction time is: ", 20/((stopEnd - start))/60 , "minutes")



#
#
# def columnReduce(chain_1, chain_2):
#     diag=diagonalReduce(chain_1,chain_2)
#     sortPair = arrangeSequences(diag[0],diag[1])
#     chain_1 = sortPair[0]
#     chain_2 = sortPair[1]
#     while not isColumnSorted(chain_1,chain_2):
#         if len(chain_1[2]) <= len(chain_2[2]):
#             if chain_2[1][1] < chain_1[2][-1]:
#                 newChain=[chain_1[0],chain_1[1],chain_1[2][:-1]]
#                 columnReduce(newChain,chain_2)
#                 newChain[2].append(chain_1[2][-1])
#                 return [newChain,chain_2]
#             else:
#                 for i in range(0, len(chain_1[2])):
#                     if chain_1[2][i] > chain_2[2][i] and \
#                             not isSublist(chain_1[2][i:],intervalNum(chain_2[2][i:])):
#                         chain_1[2][i], chain_2[2][i] = chain_2[2][i], chain_1[2][i]
#                     else:
#                         continue
#         else:
#             for i in range(0, len(chain_2[2])):
#                 if chain_1[2][i] > chain_2[2][i]:
#                     chain_1[2][i], chain_2[2][i] = chain_2[2][i], chain_1[2][i]
#                 else:
#                     continue
#
#     return [chain_1, chain_2]
#
# def antiDiagonalReduce(chain_1,chain_2):
#     column=columnReduce(chain_1,chain_2)
#     sortPair = arrangeSequences(column[0], column[1])
#     chain_1 = sortPair[0]
#     chain_2 = sortPair[1]
#     length_1 = len(chain_1[2])
#     length_2 = len(chain_2[2])
#     lable_1 = chain_1[1]
#     lable_2 = chain_2[1]
#     while not isAntiDiagonalSorted(chain_1,chain_2):
#         if  length_1>length_2:
#             if lable_1[1]<chain_2[2][-1]:
#                 newChain=[chain_2[0],chain_2[1],chain_2[2][:-1]]
#                 antiDiagonalReduce(chain_1,newChain)
#                 newChain[2].append(chain_2[2][-1])
#                 return [chain_1,newChain]
#             for j in range(0,length_2):
#                 for i in range( length_1-1,j,-1):
#                     if chain_2[2][j] in chain_1[2]:
#                         continue
#                     elif chain_2[2][j]>chain_1[2][i] and \
#                             not isSublist(chain_2[2][j:],intervalNum(chain_1[2][ length_1-1:])):
#                         chain_1[2][i], chain_2[2][j] = chain_2[2][j], chain_1[2][i]
#                     else:
#                         continue
#         else:
#             for j in range(0, length_1-1):
#                 for i in range( length_1-1,j,-1):
#                     if chain_2[2][j]>chain_1[2][i] and \
#                             not isSublist(chain_2[2][j:],intervalNum(chain_1[2][ length_1-1:])):
#                         chain_1[2][i], chain_2[2][j] = chain_2[2][j], chain_1[2][i]
#                     else:
#                         continue
#     return [chain_1,chain_2]
# #
# # def diagonalReduceTable(table):
# #     table=bubbleSort(table)
# #     for i in range(0,len(table)-1):
# #         for j in range(i+1,len(table)):
# #             newtable = diagonalReduce(table[i], table[j])
# #             table[i],table[j] = newtable[0],newtable[1]
# #     return table
#
#
#
# def columnReduceTable(table):
#     table = bubbleSort(table)
#     for i in range(0,len(table)-1):
#         for j in range(i+1,len(table)):
#             newtable=columnReduce(table[i],table[j])
#             table[i],table[j] = newtable[0],newtable[1]
#             columnReduceTable(table)
#     return table
#
#
#
# def antiDiagonalReduceTable(table):
#     table=bubbleSort(table)
#     for i in range(0,len(table)-1):
#         for j in range(i+1,len(table)):
#             newtable=antiDiagonalReduce(table[i],table[j])
#             table[i] , table[j] =newtable[0] , newtable[1]
#             table=diagonalReduceTable(table)
#             table=columnReduceTable(table)
#     return table
#
#
# def shape(table):
#     shapeReturn=[]
#     for x in table:
#         shapeReturn.append([x[1],len(x[2])])
#     return shapeReturn
#
# def size(table):
#     sizeReturn=[]
#     for x in table:
#         sizeReturn.append(len(x[2]))
#     return sizeReturn
#
#
#