# inf573vegetalisation
Hello,

Before getting to the code we recommend that you read the paper first.
Once it is done here is how to run the notebook.

## Organisation
In this notebook, there are mostly three things :
- a python module that trains a Unet model
- a python module that implements the two algorithms mentionned in the paper.
- some data

## What you can do
the story.ipynb notebook is runnable for you, however, the train_cnn notebook won't be runnable without you downloading the big dataset that can be found here: https://ignf.github.io/FLAIR/ .
However all the parameters are the one we used for the training, and the results are still shown in the train_cnn.ipynb file.
We exported a few predictions, a few labels and a few images in the data_sample folder for you to try if you want.

In summary, go to story.ipynb to see how our code works.

## Installation
We used poetry for creating the virtual environment associated with the project. Here is how to install it :
```pip install poetry```
then 
```poetry install```
which should create a virtual environment to run the notebook.
