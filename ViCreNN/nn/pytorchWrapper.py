import torch
import torch.nn as nn
from torchsummary import summary
from ViCreNN.nn.wrapperTemplate import WrapperTemplate


class FrameStructure(WrapperTemplate, nn.Module):

    def __init__(self, numberInput, numberOutput, structure, structureName, logger):
        nn.Module.__init__(self)
        WrapperTemplate.__init__(self, numberInput, numberOutput, structure, structureName, logger)
        self.frame = "Pytorch"

    def prepareModel(self):
        # Input Block
        initBlockIndex = self.returnFirstCompleteDiagram(self.structure)
        inNeurons = self.ninput
        outNeurons = inNeurons
        # TODO
                    self.conv1 = nn.Conv2d(1, 20, 5)
                    self.conv2 = nn.Conv2d(20, 20, 5)

                def forward(self, x):
                    x = F.relu(self.conv1(x))
                    return F.relu(self.conv2(x))

        self.model = nn.Sequential()
        self.model.add_module("blockInput", torch.nn.Linear(, self.ninput))

        # nodes dictionary keeps track of every block as keras node
        nodes = {self.structure[initBlockIndex]["name"]: inputNode}
        # merge dictionary keeps track of the two branches associated to one special block
        merge = {}

        getP = self.getPair(initBlockIndex)

        # starts getting the next arch-block pair
        for arch, block in getP:
            activationFunc = self.chooseActivation(self.structure[arch]["activFunc"])

            if activationFunc is None:
                self.logger("Error choosing activation function in Pytorch: " + str(self.structure[arch]["activFunc"]) + " not available in Pytorch")
                return False

            if

            if self.structure[block]["LastBlock"] is False:
                outNeurons = int(self.structure[block]["neurons"])
            else:
                outNeurons = self.noutput

            self.model.add_module("arch" + self.structure[arch]["name"], activationFunc)
            self.model.add_module("block" + self.structure[block]["name"], torch.nn.Linear(inNeurons, outNeurons))

            inNeurons = outNeurons

    def forward(self, x):
        return self.model.forward(x)

    def saveModel(self):
        if self.model is None:
            self.prepareModel()

        torch.save(self.model, "test.txt")
        summary(self.model, (self.ninput,))

    def chooseNode(self, layerType):
        return None

    def chooseActivation(self, activ):
        if activ == "Hyperbolic Tangent (Tanh)":
            return nn.Tanh
        elif activ == "Softmax":
            return nn.Softmax
        elif activ == "Rectified Linear (ReLu)":
            return nn.ReLU
        elif activ == "Exponential Linear (Elu)":
            return nn.ELU
        elif activ == "Log Softmax":
            return nn.LogSoftmax
        elif activ == "Sigmoid":
            return nn.Sigmoid
        elif activ == "Softplus":
            return nn.Softplus
        elif activ == "Linear":
            return nn.Linear
        elif activ == "Hard Hyperbolic Tangent(HardTanh)":
            return nn.Hardtanh
        else:
            return None

    def chooseCost(self):
        if self.cost == "Mean Square Error (MSE)":
            self.loss_object = torch.nn.MSELoss
        elif self.cost == "Mean Absolute Error (MAE)":
            self.loss_object = torch.nn.L1Loss
        elif self.cost == "Categorical Cross Entropy":
            self.loss_object = torch.nn.CrossEntropyLoss
        elif self.cost == "Kullback-Leibler (KLDivergence)":
            self.loss_object = torch.nn.KLDivLoss
        elif self.cost == "Hinge":
            self.loss_object = torch.nn.HingeEmbeddingLoss
        elif self.cost == "Cosine Similarity":
            self.loss_object = torch.nn.CosineSimilarity
        elif self.cost == "Binary Cross Entropy (BCE)":
            self.loss_object = torch.nn.BCELoss
        elif self.cost == "Soft Margin Loss (SML)":
            self.loss_object = torch.nn.SoftMarginLoss
        elif self.cost == "Poisson Negative Log-Likelihood":
            self.loss_object = torch.nn.PoissonNLLLoss
        elif self.cost == "Negative Log-Likelihood":
            self.loss_object = torch.nn.NLLLoss
        else:
            self.loss_object = None

    def chooseOptimizer(self):
        if self.optimizer == "Adam":
            self.optimizer_object = torch.optim.Adam
        elif self.optimizer == "SDG":
            self.optimizer_object = torch.optim.SGD
        elif self.optimizer == "Adadelta":
            self.optimizer_object = torch.optim.Adadelta
        elif self.optimizer == "Adagrad":
            self.optimizer_object = torch.optim.Adagrad
        elif self.optimizer == "Adamax":
            self.optimizer_object = torch.optim.Adamax
        elif self.optimizer == "RMSprop":
            self.optimizer_object = torch.optim.RMSprop
        else:
            self.optimizer_object = None

    def run(self):
        self.chooseCost()
        self.chooseOptimizer()

        if self.loss_object is None:
            return "Error choosing cost function in PyTorch: " + self.cost + " not available in Pytorch"
        if self.optimizer_object is None:
            return "Error choosing optimizer in Pytorch: " + self.optimizer + " not available in Pytorch"

        optimizer = self.optimizer_object(self.model.parameters(), lr=0.01)
        self.model.train()

        y_pred = None
        loss = None

        for epoch in range(self.epoch):

            optimizer.zero_grad()  # Forward pass
            y_pred = self.model(self.inputTrain)  # Compute Loss
            loss = self.loss_object(y_pred.squeeze(), self.outputTrain)
            loss.backward()
            optimizer.step()

        correct = 0
        correct += (y_pred == self.outputTrain).sum().item()

        return "Train --> Loss: " + str(loss.item()) + ", Accuracy: " + str((correct/len(self.outputTrain)) * 100)

    def test(self):
        self.model.eval()
        y_pred = self.model(self.inputTest)
        after_train = self.loss_object(y_pred.squeeze(), self.outputTest)

        correct = 0
        correct += (y_pred == self.outputTest).sum().item()

        return "Test --> Loss: " + str(after_train.item()) + ", Accuracy: " + str((correct/len(self.outputTest)) * 100)

