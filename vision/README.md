# PyTorch Template Vision Task

*Authors: Andrew Guan*

> Referenced from <a href="https://github.com/cs230-stanford/cs230-code-examples">cs230 code template</a>.

## Quickstart

1. **Build the dataset**: I'm used to building description files. Such as `train description.csv`,`val description.csv` and `test description.csv`. And the data split is also completed in this stage.

2. **Create experiment:** `base_model` directory under the `experiments` directory can be the first model for your experiment. It contains a file `params.json` which sets the hyperparameters for the experiment. It looks like
   
    ```json
    {
        "learning_rate": 1e-3,
        "batch_size": 32,
        "num_epochs": 3,
        "dropout_rate":0.8, 
        "num_channels": 32,
        "save_summary_steps": 100,
        "num_workers": 4
    }
    ```
    
    For every new experiment, you will need to create a new directory under `experiments` with a similar `params.json` file.
    
3. **Train your experiment**. Simply run

    ```
    python train.py --data_dir xxx --model_dir experiments/xxx
    ```
	It will instantiate a model and train it on the training set following the hyperparameters specified in `params.json`. It will also evaluate some metrics on the validation set.

4. **hyperparameters search:** We created a new directory `learning_rate` in `experiments` for you. Now, run
    
    ```
    python search_hyperparams.py --data_dir xxx --parent_dir experiments/learning_rate
	```
It will train and evaluate a model with different values of learning rate defined in `search_hyperparams.py` and create a new directory for each experiment under `experiments/learning_rate/`. So the directory named with parameters(learning_rate, batch_size) under the experiments represents the fine tune experiment of the corresponding experiment. 
    
5. **Display the results** of the hyperparameters search in a nice format
    ```
    python synthesize_results.py --parent_dir experiments/learning_rate
    ```

6. __Evaluation on the test set__ Once you've run many experiments and selected your best model and hyperparameters based on the performance on the validation set, you can finally evaluate the performance of your model on the test set. (The best model weight should be putted in `experiments/base_model/`) Run
    ```
    python evaluate.py --data_dir data/xxx --model_dir experiments/base_model
    ```


## Guidelines for more advanced use

We recommend reading through `train.py` to get a high-level overview of the training loop steps:
- loading the hyperparameters for the experiment (the `params.json`)
- loading the training and validation data
- creating the model, loss_fn and metrics
- training the model for a given number of epochs by calling `train_and_evaluate(...)`

You can then have a look at `data_loader.py` to understand:
- how jpg images are loaded and transformed to torch Tensors
- how the `data_iterator` creates a batch of data and labels and pads sentences

Once you get the high-level idea, depending on your dataset, you might want to modify
- `model/net.py` to change the neural network, loss function and metrics
- `model/data_loader.py` to suit the data loader to your specific needs
- `train.py` for changing the optimizer
- `train.py` and `evaluate.py` for some changes in the model or input require changes here

Once you get something working for your dataset, feel free to edit any part of the code to suit your own needs.

## Argument Setting Specification

In this part, I set the convention that which parameters should be putted in the `params.json` and which should be putted in the `args`.

### `params.json`

The parameters which is related to specific experiment should be set in this file. Such as: learning rate, batch_size, num_epochs, num_channels, missing_rate and so on.

### `args`

The parameters which is related to the whole project should be set in this code. Such as: model_path, data_path and so on.

## Workflow Specification

1. **Data Define:** define data class, transforms and data loader. split data(I'm used to create `xxx description.csv`)
2. **Model Define:** define model, loss, metric
3. **Training:** set experiment parameters. How does the data flow the net.
4. **Evaluate:** use test set to evaluate the best model.