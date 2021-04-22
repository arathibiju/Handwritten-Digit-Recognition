from __future__ import print_function
from torch import nn, optim, cuda
from torch.utils import data
from torchvision import datasets, transforms, models
import torch.nn.functional as F
import time
import matplotlib as plt
import numpy as np
import torch
from matplotlib import pyplot


import matplotlib.pyplot as plt

# Training settings
batch_size = 100
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
                                           shuffle=True)

test_loader = data.DataLoader(dataset=test_dataset,
                                          batch_size=batch_size,
                                          shuffle=False)



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


model = Net()
model.to(device)
criterion = nn.CrossEntropyLoss()
#optimizer = optim.SGD(model.parameters(), lr=0.2, momentum=0.5)
#optimizer = optim.SGD(model.parameters(), lr=0.2)           # SGD with no momentum
optimizer = optim.Adam(model.parameters(), lr=0.001)       # use either Adam or SGD, doesnt matter.


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



max_accuracy = 0
def test():
    model.eval()
    test_loss = 0
    correct = 0
    global max_accuracy
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        # sum up batch loss
        test_loss += criterion(output, target).item()
        # get the index of the max
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    print(int(correct))
    print(max_accuracy) 
    test_loss /= len(test_loader.dataset)
    print(f'===========================\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(test_loader.dataset)} '
          f'({100. * correct / len(test_loader.dataset):.0f}%)')
    max_accuracy = int(correct) if int(correct) > max_accuracy else max_accuracy
    print(f'Max accuracy so far: {max_accuracy} \n')
   
def classify(img, ps):
    ''' 
    Function for viewing an image and it's predicted classes.
    '''
    ps = ps.data.numpy().squeeze()
    ps = ps/100
    img = img.cpu()
    fig, ax2 = plt.subplots(ncols=1)
    #fig, (ax1, ax2) = plt.subplots(figsize=(6,9), ncols=2)
    #ax1.imshow(img.resize_(1, 28, 28).numpy().squeeze())
    #ax1.axis('off')
    ax2.barh(np.arange(10), ps)
    ax2.set_aspect(10)
    ax2.set_yticks(np.arange(10))
    ax2.set_yticklabels(np.arange(10))
    ax2.set_title('Class Probability')
    ax2.set_xlim(0, 100)
    plt.tight_layout()
    plt.savefig('Tessss.png')



if __name__ == '__main__':


    since = time.time()
    for epoch in range(1, 2):
        epoch_start = time.time()
        train(epoch)
        m, s = divmod(time.time() - epoch_start, 60)
        print(f'Training time: {m:.0f}m {s:.0f}s')
        test()
        m, s = divmod(time.time() - epoch_start, 60)
        print(f'Testing time: {m:.0f}m {s:.0f}s')


        #images = test_dataset[0][0]
        #images.to(device)

        images, labels = next(iter(test_loader))
        # replace trainloader to check training accuracy.

        
        img = images[1].cuda()
        # img = images[0].view(1, 784).cuda()
        
        #images = torch.tensor(images[0])

        # img = images[0].view(1, 784)
        
        img = torch.unsqueeze(img, 0)
        # img = torch.unsqueeze(img, 0)

        #img = img.to(device)
        # print(img)

        # Turn off gradients to speed up this part
        with torch.no_grad():
            logpb = model(img)

        # Output of the network are log-probabilities, need to take exponential for probabilities
        pb = torch.exp(logpb)
        x = pb.cpu()
        
        probab = list(x.numpy()[0])
        print("Predicted Digit =", probab.index(max(probab)))
        classify(img.view(1, 28, 28), x)

    m, s = divmod(time.time() - since, 60)
    print(f'Total Time: {m:.0f}m {s:.0f}s\nModel was trained on {device}!')

