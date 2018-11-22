# coding = utf-8
import math
import random
# 定义一个神经元
class Neuron:
    def __init__(self, bias):
        self.bias = bias
        self.weights = []

    # 初始化输入，并计算输出
    def calculateOutput(self, inputs):
        self.inputs = inputs
        self.output = self.squash(self.calculateTotalNetInput())
        return self.output

    # sigmoid函数
    def squash(self, totalNetInput):
        return 1/(1 + math.exp(-totalNetInput))

    # 将输入乘以权重，再加上偏差，得到神经网络的输出
    def calculateTotalNetInput(self):
        total = 0
        for i in range(len(self.inputs)):
            total += self.inputs[i] * self.weights[i]
        return total + self.bias

    # 计算g_j = 差*导数
    def calculatePDTotalNetInput(self, targetOutput):
        return self.calculatePDTotalNetOutput(targetOutput)*self.calculatePDOutputNetInput()

    # 计算目标输出与计算输出的差别
    def calculatePDTotalNetOutput(self, targetOutput):
        return -(targetOutput - self.output)

    # 计算导数 因为f'(x) = f(x)(1-f(x))
    def calculatePDOutputNetInput(self):
        return self.output*(1-self.output)

    # 
    def calculatePDInputNetWeight(self, index):
        return self.inputs[index]

    # compute relative error
    def calculateError(self,targetOutput):
        return 0.5*(self.output-targetOutput) ** 2

    # 计算相对误差 0.5e^2/max{参考输出和实际输出的模}^2
    def calculateRelativeError(self,targetOutput):
        return (0.5*(self.output-targetOutput) ** 2)/(max(abs(targetOutput), abs(self.output))**2)

# 定义一层神经元
class NeuronLayer:
    def __init__(self, neuronNumber, bias):
        self.bias = bias
        self.neurons = []
        for i in range(neuronNumber):
            self.neurons.append(Neuron(self.bias[i]))

    # 计算这一层神经元的输出，存储在列表中
    def feedForward(self, inputs):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.calculateOutput(inputs))
        return outputs
    # 获取这一层的神经元的输出
    def getOutputs(self):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.output)
        return outputs


# 神经网络的类
class NeuralNetwork:
        def __init__(self, numInputs, numHidden, numOutputs, learningRate, hiddenLayerWeights = None, outputLayerWeights = None):
            self.numInputs = numInputs
            self.learningRate = learningRate
            # 初始化initIH 和initIO
            self.initIH = 1 / math.sqrt(numInputs)
            self.initIO = 1 / math.sqrt(numHidden)
            # 随机赋值隐藏层和输出层的偏差
            self.hiddenLayerBias = [random.randint(0, 100)/100*self.initIH * 2 - self.initIH] * numHidden
            self.outputLayerBias = [random.randint(0, 100)/100*self.initIO * 2 - self.initIO] * numOutputs
            self.hiddenLayer = NeuronLayer(numHidden, self.hiddenLayerBias) # 创建隐藏层
            self.outputLayer = NeuronLayer(numOutputs, self.outputLayerBias) # 创建输出层

            # 初始化输入层到影藏层的权重以及初始化隐藏层到输出层的权重
            self.initWeightsFromInputToHiddenLayerNeurons(hiddenLayerWeights)
            self.initWeightsFromHiddenToOutputLayerNeurons(outputLayerWeights)

        def initWeightsFromInputToHiddenLayerNeurons(self, hiddenLayerWeights):
            weightIndex = 0;
            for h in range(len(self.hiddenLayer.neurons)):
                for i in range(self.numInputs):
                    if not hiddenLayerWeights:
                        self.hiddenLayer.neurons[h].weights.append(random.randint(0, 100)/100*self.initIH* 2 - self.initIH)
                    else:
                        self.hiddenLayer.neurons[h].weights.append(hiddenLayerWeights[weightIndex])
                        weightIndex +=1

        def initWeightsFromHiddenToOutputLayerNeurons(self, outputLayerWeights):
            weightIndex = 0;
            for o in range(len(self.outputLayer.neurons)):
                for i in range(len(self.hiddenLayer.neurons)):
                    if not outputLayerWeights:
                        self.outputLayer.neurons[o].weights.append(random.randint(0, 100)/100*self.initIO* 2 - self.initIO)
                    else:
                        self.outputLayer.neurons[o].weights.append(outputLayerWeights[weightIndex])
                        weightIndex +=1

        # 根据输入计算输出，存储在列表中
        def feedForward(self, inputs):
            hiddenLayerOutputs = self.hiddenLayer.feedForward(inputs)
            return self.outputLayer.feedForward(hiddenLayerOutputs)

        def train(self, trainingInputs, trainOutputs):
            self.feedForward(trainingInputs)

            #1.output neuron deltas
            pdOutputNeuronTotalNetInput = [0]*len(self.outputLayer.neurons)
            for o in range(len(pdOutputNeuronTotalNetInput)):
                pdOutputNeuronTotalNetInput[o] = self.outputLayer.neurons[o].calculatePDTotalNetInput(trainOutputs[o])

            #2.Hidden neuron deltas
            pdHiddenNeuronTotalNetInput = [0]*len(self.hiddenLayer.neurons)
            for h in range(len(pdHiddenNeuronTotalNetInput)):
                dTotalNetHiddenOutput = 0
                for o in range(len(self.outputLayer.neurons)):
                    dTotalNetHiddenOutput += pdOutputNeuronTotalNetInput[o]*self.outputLayer.neurons[o].weights[h]

                pdHiddenNeuronTotalNetInput[h] = dTotalNetHiddenOutput * self.hiddenLayer.neurons[h].calculatePDOutputNetInput()

            #3.Update output neuron weights & bias
            for o in range(len(self.outputLayer.neurons)):
                for wHiddenToOutput  in range(len(self.outputLayer.neurons[o].weights)):
                    pdErrorWeight = pdOutputNeuronTotalNetInput[o]* self.outputLayer.neurons[o].calculatePDInputNetWeight(wHiddenToOutput)
                    pdErrorOutputBias = pdOutputNeuronTotalNetInput[o]
                    self.outputLayer.neurons[o].weights[wHiddenToOutput] -= self.learningRate * pdErrorWeight
                self.outputLayer.neurons[o].bias -= self.learningRate * pdErrorOutputBias
            #4.Update hidden neuron weights & bias
            for h in range(len(self.hiddenLayer.neurons)):
                for wInputToHidden in range(len(self.hiddenLayer.neurons[h].weights)):
                    pdErrorWeight2 = pdHiddenNeuronTotalNetInput[h] * self.hiddenLayer.neurons[h].calculatePDInputNetWeight(wInputToHidden)
                    pdErrorHiddenBias = pdHiddenNeuronTotalNetInput[h]
                    self.hiddenLayer.neurons[h].weights[wInputToHidden] -= self.learningRate * pdErrorWeight2
                self.hiddenLayer.neurons[h].bias -= self.learningRate * pdErrorHiddenBias

        def calculateError(self, trainingSet):
            myerror = 0
            trainingInputs,trainningOutputs = trainingSet
            self.feedForward(trainingInputs)
            for o in range(len(trainningOutputs)):
                myerror += self.outputLayer.neurons[o].calculateError(trainningOutputs[o])
            return myerror

        def calculateRelativeError(self, trainingSet):
            myerror = 0
            trainingInputs,trainningOutputs = trainingSet
            self.feedForward(trainingInputs)
            for o in range(len(trainningOutputs)):
                myerror += self.outputLayer.neurons[o].calculateRelativeError(trainningOutputs[o])
            return myerror