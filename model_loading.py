import torch as pt
import pytorch_lightning as pl
from transformers import BertTokenizer, BertForSequenceClassification 
import numpy as np
import pandas as pd


class SuicideDataset(Dataset):
    def __init__(self, dataset):
        self.dataset = dataset
    def __len__(self):
        return len(self.dataset)
    def __getitem__(self, idx):
        return {'input_ids': self.dataset.iloc[idx][0], 'label': self.dataset.iloc[idx][1]}

class SuicideDetectionClassifier(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = BertForSequenceClassification.from_pretrained('bert-base-cased')
        self.loss = CrossEntropyLoss()

    def forward(self, x):
        mask = (x != 0).float()  
        logits = self.model(x, mask)['logits']
        return logits

    def training_step(self, batch, batch_idx):
        y, x = batch['label'], batch['input_ids']
        y_hat = self.forward(x)
        loss = self.loss(y_hat, y)
        return {'loss': loss, 'log': {'train_loss': loss}}

    # def validation_step(self, batch, batch_idx):
    #     y, x = batch['label'], batch['input_ids']
    #     y_hat = self.forward(x)
    #     loss = self.loss(y_hat, y)
    #     acc = (y_hat.argmax(-1) == y).float()
    #     return {'loss': loss, 'acc': acc}

    # def validation_epoch_end(self, outputs):
    #     loss = pt.cat([output['loss'] for output in outputs], 0).mean()
    #     acc = pt.cat([output['acc'] for output in outputs], 0).mean()
    #     out = {'val_loss': loss, 'val_acc': acc}
    #     return {**out, 'log': out}

    def configure_optimizers(self):
        optimizer = pt.optim.Adam(self.parameters(), lr=1e-5)
        return optimizer


def load_model(path):
    # return model
    return pt.load("./model.pt")


def pred(text: str, model):
    tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
    x = tokenizer.encode(text, 
                        max_length=256, 
                        return_tensors='pt', 
                        padding='max_length', 
                        truncation=True)
    # 0 = not suicidal
    # 1 = suicidal
    return np.argmax(pt.nn.Softmax()(model(x)).view(-1).detach().numpy())
