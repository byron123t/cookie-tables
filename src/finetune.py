import argparse
import os
import random
import torch
import numpy as np
from torch.optim import AdamW, Adam
from torch.utils.data import DataLoader
from tqdm import tqdm
from tqdm.auto import tqdm

import evaluate
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForMultipleChoice, get_scheduler


def set_seed(seed):
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


SEED = 595
set_seed(SEED)
device = torch.device('cuda:1') if torch.cuda.is_available() else torch.device('cpu')
print(device)


def load_data(tokenizer, params):
    def tokenize_function(examples):
        sol1_tok = []
        for goals, sol1, sol2 in zip(examples['goal'], examples['sol1'], examples['sol2']):
            sol1_tok.append(tokenizer([goals, goals], [sol1, sol2], padding='max_length', truncation=True, max_length=512, return_tensors='pt').to(device))
        return {'sol1': sol1_tok, 'label': examples['label']}

    dataset = load_dataset(params.dataset)
    tokenized_datasets = dataset.map(tokenize_function, batched=True, batch_size=params.batch_size)
    tokenized_datasets.set_format('torch')
    train_dataloader = DataLoader(tokenized_datasets['train'], batch_size=params.batch_size)
    eval_dataloader = DataLoader(tokenized_datasets['validation'], batch_size=params.batch_size)
    test_dataloader = DataLoader(tokenized_datasets['test'], batch_size=params.batch_size)

    return train_dataloader, eval_dataloader, test_dataloader


def finetune(model, train_dataloader, eval_dataloader, params):
    if params.optimizer == 'Adam':
        optimizer = Adam(model.parameters(), lr=params.lr)
    else:
        optimizer = AdamW(model.parameters(), lr=params.lr)
    metric = evaluate.load('accuracy')
    lr_scheduler = get_scheduler(name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=params.num_epochs * len(train_dataloader))
    model.train()
    with tqdm(range(params.num_epochs)) as tepoch:
        for _ in tepoch:
            # print()
            losses = []
            with tqdm(train_dataloader) as tbatch:
                for batch in tbatch:
                    data = {'input_ids': batch['sol1']['input_ids'].to(device),
                            'token_type_ids': batch['sol1']['token_type_ids'].to(device),
                            'attention_mask': batch['sol1']['attention_mask'].to(device),
                            'labels': batch['label'].to(device)}
                    outputs = model(**data)
                    loss = outputs.loss
                    losses.append(loss.detach().cpu())
                    tbatch.set_postfix(loss=np.mean(losses))
                    # print('Batch {} out of {}, Loss: {}\r'.format(i, len(train_dataloader), np.mean(losses)), end='')
                    loss.backward()
                    optimizer.step()
                    lr_scheduler.step()
                    optimizer.zero_grad()
            # print()

            model.eval()
            for batch in tqdm(eval_dataloader):
                with torch.no_grad():
                    data = {'input_ids': batch['sol1']['input_ids'].to(device),
                            'token_type_ids': batch['sol1']['token_type_ids'].to(device),
                            'attention_mask': batch['sol1']['attention_mask'].to(device),
                            'labels': batch['label'].to(device)}
                    outputs = model(**data)
                logits = outputs.logits
                predictions = torch.argmax(logits, dim=-1)
                metric.add_batch(predictions=predictions, references=batch['label'].to(device))
            score = metric.compute()
            tepoch.set_postfix(accuracy=score['accuracy'])
            # print('Test Accuracy:', score['accuracy'])
            # print()

    print()
    return model


def test(model, test_dataloader, prediction_save='predictions.torch'):
    print()
    metric = evaluate.load('accuracy')
    model.eval()
    all_predictions = []

    for batch in tqdm(test_dataloader):
        with torch.no_grad():
            data = {'input_ids': batch['sol1']['input_ids'].to(device),
                    'token_type_ids': batch['sol1']['token_type_ids'].to(device),
                    'attention_mask': batch['sol1']['attention_mask'].to(device),
                    'labels': batch['label'].to(device)}
            outputs = model(**data)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)
        metric.add_batch(predictions=predictions, references=batch['label'].to(device))
        all_predictions.extend(predictions)

    score = metric.compute()
    print('Test Accuracy:', score['accuracy'])
    torch.save(all_predictions, prediction_save)

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #


def main(params):

    tokenizer = AutoTokenizer.from_pretrained(params.model, num_labels=2)
    train_dataloader, eval_dataloader, test_dataloader = load_data(tokenizer, params)

    model = AutoModelForMultipleChoice.from_pretrained(params.model)
    model.to(device)
    model = finetune(model, train_dataloader, eval_dataloader, params)

    # test(model, test_dataloader)
    test(model, eval_dataloader, params.save)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finetune Language Model')

    parser.add_argument('--dataset', type=str, default='piqa')
    parser.add_argument('--model', type=str, default='bert-base-cased')
    parser.add_argument('--batch_size', type=int, default=4)
    parser.add_argument('--num_epochs', type=int, default=6)
    parser.add_argument('--lr', type=float, default=5e-5)
    parser.add_argument('--optimizer', type=str, default='Adam')
    parser.add_argument('--save', type=str, default='predictions.torch')

    params, unknown = parser.parse_known_args()
    main(params)
