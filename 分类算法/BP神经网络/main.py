import bp_neural_network
import read_file
import random

learningRate = 0.01
numInput = 3
numHidden = 4
numOutput = 1
loss = 0.10
threshold = 0.5
def completeGradientDescent(trainingset=None,testset=None):
    nn = bp_neural_network.NeuralNetwork(numInput, numHidden, numOutput, learningRate, None, None)
    for i in range(10000):
        isCompelete = False
        for data in trainingset:
            if data[3] + 1 < 0.01:
                data[3] = 0.0
            nn.train(data[:3], data[3:])
            error_real = round(nn.calculateRelativeError([data[:3], data[3:]]), 9)
            if (error_real <= loss):
                isCompelete = True
                break
        if (isCompelete):
            print('iterater times:' + str(i))
            break
            # else:
            #     print('It may not convergence')
    count = 0
    total = 0
    for data in testset:
        forecastReal = 0
        forecast = nn.feedForward(data[:3])
        if forecast[0] < threshold:
            forecastReal = -1
        else:
            forecastReal = 1
        if abs(data[3] - forecastReal) < 0.001:
            count += 1
            total += 1
        else:
            total += 1
    print('Complete Descent Accuracy Rate:', round(count / total, 9))

def randomGradientDescent(trainingset=None,testset=None):
    nn = bp_neural_network.NeuralNetwork(numInput, numHidden, numOutput, learningRate, None, None)
    for i in range(10000):
        isCompelete = False
        index = 0
        while index < len(trainingset):
            if trainingset[index][3] + 1 < 0.01:
                trainingset[index][3] = 0.0
            nn.train(trainingset[index][:3], trainingset[index][3:])
            error_real = round(nn.calculateRelativeError([trainingset[index][:3], trainingset[index][3:]]), 9)
            index+=random.randint(0, 20)
            if (error_real <= loss):
                isCompelete = True
                break
        if (isCompelete):
            print('iterater times:' + str(i))
            break
            # else:
            #     print('It may not convergence')
    count = 0
    total = 0
    for data in testset:
        forecast = nn.feedForward(data[:3])
        if forecast[0] < threshold:
            forecastReal = -1
        else:
            forecastReal = 1
        if abs(data[3] - forecastReal) < 0.001:
            count += 1
            total += 1
        else:
            total += 1
    print('Random Descent Accuracy Rate:', round(count / total, 9))

def main():
    dataset = []
    for row in read_file.data_reader('titanic.dat'):
        dataset.append([float(row[0]), float(row[1]), float(row[2]), float(row[3])])
    split_ratio = 0.7
    trainingset, testset = read_file.split(dataset, split_ratio)
    completeGradientDescent(trainingset, testset)
    # randomGradientDescent(trainingset, testset)

if __name__ == '__main__':
    main()