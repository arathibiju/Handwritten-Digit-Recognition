# ##
# This is the MODEL of the application
# ##

from __future__ import print_function
from torch import nn, optim, cuda
from torch.utils import data
from torchvision import datasets, transforms, models
import torch.nn.functional as F
import time
import matplotlib as plt
import numpy as np

# # MNIST Dataset
# train_dataset = datasets.MNIST(root='mnist_data/',
#                             train=True,
#                             transform=transforms.ToTensor(),
#                             download=True)

# test_dataset = datasets.MNIST(root='mnist_data/',
#                             train=False,
#                             transform=transforms.ToTensor())


# # Data Loader (Input Pipeline)
# train_loader = data.DataLoader(dataset=train_dataset,
#                                            batch_size=batch_size,
#                                            shuffle=True)

# test_loader = data.DataLoader(dataset=test_dataset,
#                                           batch_size=batch_size,
#                                           shuffle=False)


class Model():
    def __init__(self):
        self.batch_size = 30
        self.data_available = False
        self.set_device()
        #self.load_dataset()
        self.model = Net()
        self.model.to(self.device)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        self.progress = 0
        self.epoch_range = 2
        self.max_accuracy = 0

        print('We are in Model init')
        # self.model = model
        
        # print(device)
        # self.criterion = criterion
        # self.optimizer = optimizer

    def main(self):
        print('We are in Model main')
        print(f'Training MNIST Model on {self.device}\n{"=" * 44}')
        
        since = time.time()
        for epoch in range(1, self.epoch_range):
            epoch_start = time.time()
            self.train(epoch)
            m, s = divmod(time.time() - epoch_start, 60)
            print(f'Training time: {m:.0f}m {s:.0f}s')
            self.test()
            m, s = divmod(time.time() - epoch_start, 60)
            print(f'Testing time: {m:.0f}m {s:.0f}s')

        m, s = divmod(time.time() - since, 60)
        print(f'Total Time: {m:.0f}m {s:.0f}s\nModel was trained on {self.device}!')

    def train(self, epoch):
        self.model.train()
        for batch_idx, (data, target) in enumerate(self.train_loader):
            data, target = data.to(self.device), target.to(self.device)
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)
            loss.backward()
            self.optimizer.step()
            if batch_idx % 10 == 0:
                self.progress += self.batch_size * 10
                print('Train Epoch: {} | Batch Status: {}/{} ({:.0f}%) | Loss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(self.train_loader.dataset),
                    100. * batch_idx / len(self.train_loader), loss.item()))
                

    def download_data(self):
        try:
            self.train_dataset = datasets.MNIST(root='mnist_data/',
                                        train=True,
                                        transform=transforms.ToTensor(),
                                        download=True)

            self.test_dataset = datasets.MNIST(root='mnist_data/',
                                        train=False,
                                        transform=transforms.ToTensor())
            print('Completed!')
            self.load_dataset()
            self.data_available = True

        except:
            print('The server is not very responsive, try again')
            time.sleep(2)
            self.download_data()

    def load_dataset(self):
        # Data Loader (Input Pipeline)
            self.train_loader = data.DataLoader(dataset = self.train_dataset,
                                                batch_size = self.batch_size,
                                                shuffle = True)

            self.test_loader = data.DataLoader(dataset = self.test_dataset,
                                                batch_size = self.batch_size,
                                                shuffle = False)

    def set_device(self):
        self.device = 'cuda' if cuda.is_available() else 'cpu'
        
        
    def test(self):
        self.model.eval()
        test_loss = 0
        correct = 0
        self.max_accuracy
        for data, target in self.test_loader:
            data, target = data.to(self.device), target.to(self.device)
            output = self.model(data)
            # sum up batch loss
            test_loss += self.criterion(output, target).item()
            # get the index of the max
            pred = output.data.max(1, keepdim=True)[1]
            correct += pred.eq(target.data.view_as(pred)).cpu().sum()

        print(int(correct))
        print(self.max_accuracy) 
        test_loss /= len(self.test_loader.dataset)
        print(f'===========================\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(self.test_loader.dataset)} '
            f'({100. * correct / len(self.test_loader.dataset):.0f}%)')
        self.max_accuracy = int(correct) if int(correct) > self.max_accuracy else self.max_accuracy
        print(f'Max accuracy so far: {self.max_accuracy} \n')


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Conv2d(32, 32, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Conv2d(32, 32, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(2, 2),
            nn.Dropout(0.3)
        )
        
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.Conv2d(64, 64, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2, 2),
            nn.Dropout(0.3)
        )
        
        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(2, 2),
            #nn.Dropout(0.2)    #Turn this off for aggressive predictions
        )
        
        self.fc = nn.Sequential(
            nn.Linear(128, 10)
        )
                
        
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        #x = F.log_softmax(x, dim=1)        #use either this or the nn.CrossEngtropyLoss(), doesnt really matter
        return x


# model = Net()
# model.to(device)
# criterion = nn.CrossEntropyLoss()
#optimizer = optim.SGD(model.parameters(), lr=0.2, momentum=0.5)
#optimizer = optim.SGD(model.parameters(), lr=0.2)           # SGD with no momentum
# optimizer = optim.Adam(model.parameters(), lr=0.001)       # use either Adam or SGD, doesnt matter.


# def train(epoch):
#     model.train()
#     for batch_idx, (data, target) in enumerate(train_loader):
#         data, target = data.to(device), target.to(device)
#         optimizer.zero_grad()
#         output = model(data)
#         loss = criterion(output, target)
#         loss.backward()
#         optimizer.step()
#         if batch_idx % 10 == 0:
#             print('Train Epoch: {} | Batch Status: {}/{} ({:.0f}%) | Loss: {:.6f}'.format(
#                 epoch, batch_idx * len(data), len(train_loader.dataset),
#                 100. * batch_idx / len(train_loader), loss.item()))



# max_accuracy = 0
# def test():
    # model.eval()
    # test_loss = 0
    # correct = 0
    # global max_accuracy
    # for data, target in test_loader:
    #     data, target = data.to(device), target.to(device)
    #     output = model(data)
    #     # sum up batch loss
    #     test_loss += criterion(output, target).item()
    #     # get the index of the max
    #     pred = output.data.max(1, keepdim=True)[1]
    #     correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    # print(int(correct))
    # print(max_accuracy) 
    # test_loss /= len(test_loader.dataset)
    # print(f'===========================\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(test_loader.dataset)} '
    #       f'({100. * correct / len(test_loader.dataset):.0f}%)')
    # max_accuracy = int(correct) if int(correct) > max_accuracy else max_accuracy
    # print(f'Max accuracy so far: {max_accuracy} \n')
   

if __name__ == '__main__':
    download_data()
    since = time.time()
    for epoch in range(1, 21):
        epoch_start = time.time()
        train(epoch)
        m, s = divmod(time.time() - epoch_start, 60)
        print(f'Training time: {m:.0f}m {s:.0f}s')
        test()
        m, s = divmod(time.time() - epoch_start, 60)
        print(f'Testing time: {m:.0f}m {s:.0f}s')

    m, s = divmod(time.time() - since, 60)
    print(f'Total Time: {m:.0f}m {s:.0f}s\nModel was trained on {device}!')   