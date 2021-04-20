from __future__ import print_function
from torch import nn, optim, cuda
from torch.utils import data
from torchvision import datasets, transforms
import torch.nn.functional as F
import matplotlib.pyplot as plt

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import torch
from matplotlib import pyplot
import time

# Training settings
batch_size = 60
device = 'cuda' if cuda.is_available() else 'cpu'
print(f'Training MNIST Model on {device}\n{"=" * 44}')

# MNIST Dataset
train_dataset = datasets.MNIST(root='mnist_data/',
                               train=True,
                               transform=transforms.ToTensor(),
                               download=True)

test_dataset = datasets.MNIST(root='mnist_data/',
                              train=False,
                              transform=transforms.ToTensor())

# Data Loader (Input Pipeline)
train_loader = data.DataLoader(dataset=train_dataset,
                                           batch_size=batch_size,
                                           shuffle=False)

test_loader = data.DataLoader(dataset=test_dataset,
                                          batch_size=batch_size,
                                          shuffle=False)


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.l1 = nn.Linear(784, 520)
        self.l2 = nn.Linear(520, 320)
        self.l3 = nn.Linear(320, 240)
        self.l4 = nn.Linear(240, 120)
        self.l5 = nn.Linear(120, 10)

    def forward(self, x):
        x = x.view(-1, 784)  # Flatten the data (n, 1, 28, 28)-> (n, 784)
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = F.relu(self.l3(x))
        x = F.relu(self.l4(x))
        return self.l5(x)


model = Net()
model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)


def train(epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 10 == 0:
            print('Train Epoch: {} | Batch Status: {}/{} ({:.0f}%) | Loss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))


def test():
    model.eval()
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        # sum up batch loss
        test_loss += criterion(output, target).item()
        # get the index of the max
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    test_loss /= len(test_loader.dataset)
    print(f'===========================\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(test_loader.dataset)} '
          f'({100. * correct / len(test_loader.dataset):.0f}%)')



    # since = time.time()
    # for epoch in range(1, 10):
    #     epoch_start = time.time()
    #     train(epoch)
    #     m, s = divmod(time.time() - epoch_start, 60)
    #     print(f'Training time: {m:.0f}m {s:.0f}s')
    #     test()
    #     m, s = divmod(time.time() - epoch_start, 60)
    #     print(f'Testing time: {m:.0f}m {s:.0f}s')

    # m, s = divmod(time.time() - since, 60)
    # print(f'Total Time: {m:.0f}m {s:.0f}s\nModel was trained on {device}!')

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        start = time.time()
        fig, axis = pyplot.subplots(2, 5, figsize=(6, 6))
        # print(len(test_loader))
        # images, labels = next(iter(test_loader))



        # for i, ax in enumerate(axis.flat):
        #     with torch.no_grad():
        #         image, label = images[i], labels[i]
        #         ax.imshow(image.view(28, 28), cmap='gray') # add image
        #         ax.set(title = f"{label}") # add label
    
        # plot first few images
        x = 0
        for i in range (0, 9999):
            labels = test_dataset[i][1]
            if (labels != 10 and x<10):
                pyplot.subplot(2, 5, x+1)
                pyplot.axis('off')
                img = test_dataset[i][0]
        
                pyplot.imshow(img.reshape(28,28), cmap=pyplot.get_cmap('gray'))
                x += 1

        pyplot.savefig("Figure.png")
        
        start = time.time()
        pixmap = QPixmap("Figure.png")
        end = time.time()
        print(f'it took {end - start} sec to load an image.')
        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        lbl_size = QLabel('Width: '+str(pixmap.width())+', Height: '+str(pixmap.height()))
        lbl_size.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)
        vbox.addWidget(lbl_size)
        self.setLayout(vbox)

        self.setWindowTitle('QPixmap')
        self.move(300, 300)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    