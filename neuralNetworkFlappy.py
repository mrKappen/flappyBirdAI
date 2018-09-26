# -*- coding: utf-8 -*-
"""
Created on Thu Aug  18 18:11:24 2018

@author: tkapp
"""
import os
import numpy
import random
import scipy.special
import pickle
import matplotlib
class neuralNetwork:
    #initialize network
    def __init__(self, inputnodes,hiddennodes,outputnodes):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        self.activation_function = lambda x: scipy.special.expit(x)
        self.wih = numpy.random.normal(0.0,pow(self.hnodes,-0.5),(self.hnodes,self.inodes))
        self.who = numpy.random.normal(0.0,pow(self.onodes,-0.5),(self.onodes,self.hnodes))
        # self.wih = numpy.random.rand(self.hnodes,self.inodes)
        # self.who = numpy.random.rand(self.onodes,self.hnodes)
        pass
    def __str__(self):
        print('wih: ', self.wih)
        print('who: ',self.who)
        return ''
    def newGeneration(populationSize,inputNodes,hiddenNodes,outPutNodes,oldGeneration):
        if os.path.getsize("bestBird.txt") == 0:
            pickle.dump([0],open("bestBird.txt","wb"))
        newGen = [0]*populationSize
        if len(oldGeneration) == 0:
            for i,v in enumerate(newGen):
                newGen[i] = neuralNetwork(inputNodes,hiddenNodes,outPutNodes)
                pass
        else:
            scores = [x[1] for x in oldGeneration]
            oldPopulation = [x[0] for x in oldGeneration]
            bestBirdScore = pickle.load(open("bestBird.txt","rb"))[0]
            print(bestBirdScore)
            if len(pickle.load(open("bestBird.txt","rb"))) > 1:
                print("wih",pickle.load(open("bestBird.txt","rb"))[1])
                print("who",pickle.load(open("bestBird.txt","rb"))[2])
            if max(scores) > bestBirdScore:
                bestBird = oldPopulation[scores.index(max(scores))]
                open("bestBird.txt","w").close()
                pickle.dump([max(scores), bestBird.wih,bestBird.who],open("bestBird.txt","wb"))
                pass
            # mother = oldPopulation[scores.index(max(scores))]
            mother = neuralNetwork(inputNodes,hiddenNodes,outPutNodes)
            mother.wih = pickle.load(open("bestBird.txt","rb"))[1]
            mother.who = pickle.load(open("bestBird.txt","rb"))[2]
            father = oldPopulation[scores.index(max(scores))]
            for i,v in enumerate(newGen):
                newGen[i] = neuralNetwork.crossOver(mother,father)
                if i%2 == 0:
                    newGen[i] = neuralNetwork.mutate(newGen[i])
            pass
            newGen[0] = mother # preserve the best bird as is
        pass
        return newGen
    def copy(self):
        return self
        pass
    def mutate(network):
        mask = numpy.random.randint(0,2,size=network.wih.shape).astype(numpy.bool)
        # random matrix the same shape of your data
        r = numpy.random.rand(*network.wih.shape)*numpy.max(network.wih)
        # use your mask to replace values in your input array
        network.wih[mask] = r[mask]
        mask2 = numpy.random.randint(0,2,size=network.who.shape).astype(numpy.bool)
        # random matrix the same shape of your data
        r2 = numpy.random.rand(*network.who.shape)*numpy.max(network.who)
        # use your mask to replace values in your input array
        network.who[mask2] = r2[mask2]
        return network
        pass
    def crossOver(mother, father):
        "cross the weights"
        child = neuralNetwork(mother.inodes,mother.hnodes,mother.onodes)
        shape_wih = mother.wih.shape
        shape_who = mother.who.shape
        mother_wih = mother.wih.flatten()
        mother_who = mother.who.flatten()
        father_wih = father.wih.flatten()
        father_who = father.who.flatten()

        child_wih = numpy.zeros(len(mother_wih))
        child_who = numpy.zeros(len(mother_who))
        for index, value in enumerate(mother_wih):
            t1 = (value,father_wih[index])
            child_wih[index] = random.choice(t1)
            # child_wih[index] = (0.7*value + 0.3*father_wih[index])
            pass
        for index2, value2 in enumerate(mother_who):
            child_who[index2] = random.choice((value2,father_who[index2]))
            # child_who[index2] = (0.7*value2 + 0.3*father_who[index2])/2
            pass
        child_wih = child_wih.reshape(shape_wih)
        child_who = child_who.reshape(shape_who)
        child.wih = child_wih
        child.who = child_who
        return child
        pass
    def createRandomNeuralNets(population,inputNodes,hiddenNodes,outPutNodes):
        nets = [neuralNetwork(inputNodes,hiddenNodes,outPutNodes)]*population
        return nets
        pass
    #query the network
    def query(self,inputs_list):
        inputs = numpy.array(inputs_list,ndmin=2).T
        hidden_inputs = numpy.dot(self.wih,inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = numpy.dot(self.who,hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        return final_outputs
        pass
