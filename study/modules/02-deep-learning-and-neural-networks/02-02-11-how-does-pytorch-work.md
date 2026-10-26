---
title: How does PyTorch work?
module: 2
module_title: Deep Learning and Neural Networks
lesson: '2.11'
source: https://outcomeschool.com/blog/how-does-pytorch-work
published: July 9, 2026
tags:
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 3193
reading_time: 16
status: full
---
# How does PyTorch work?

> **Module 2 · Lesson 2.11**  
> Source: [Outcome School](https://outcomeschool.com/blog/how-does-pytorch-work) · Published: July 9, 2026 · Reading time: ~16 min · Tags: `ai`, `machine-learning`

---

![How does PyTorch work?](../../assets/images/02-02-11-how-does-pytorch-work/how-does-pytorch-work.png)

PyTorch is a free and open-source library that helps us build and train machine learning models. It stores data in tensors, records every math step in a computation graph, and uses autograd to calculate the gradients for training.

In this blog, we will learn about how PyTorch works. We will also see what a tensor is, how the computation graph and autograd work together to train a model, and why PyTorch uses the GPU to become one of the most popular tools in the real world.

We will cover the following:

- What is PyTorch?
- What is a Tensor?
- The problem PyTorch solves
- What is a Computation Graph?
- What is Autograd?
- A complete training example
- What is the GPU and why does PyTorch use it?
- Why is PyTorch so popular?

Let's get started.

## What is PyTorch?

**PyTorch is a free and open-source library that helps us build and train [machine learning](https://outcomeschool.com/blog/machine-learning) models.**

In simple words, PyTorch is a toolbox. It gives us ready-made tools so that we do not have to build everything from scratch.

Let's say we want to teach a computer to recognize a cat in a photo. We do not want to write thousands of lines of complex math by hand. PyTorch gives us those tools, so we can focus on our idea.

PyTorch was created by the team at Meta (the company behind Facebook). Today, it is one of the most used libraries in the world for building artificial intelligence.

PyTorch is written to be used with Python. Python is a programming language that is easy to read and write. That is one big reason why so many people love PyTorch.

Before we go deeper, we must understand the most important building block of PyTorch. It is called the Tensor.

## What is a Tensor?

**A Tensor is a container that holds numbers in an organized way.**

In simple words, a Tensor is just a box of numbers arranged in rows and columns.

Let's understand this slowly, because everything in PyTorch is built on Tensors.

Consider a single number, like `5`. That is the simplest form.

Now consider a list of numbers, like `[1, 2, 3]`. That is a row of numbers.

Now consider a grid of numbers, like a table with rows and columns. That is like a spreadsheet.

A Tensor is the general name for all of these. One number, a row of numbers, a grid of numbers, or even bigger arrangements. They are all Tensors.

Let's visualize this as below:

```text
   Single number        Row of numbers        Grid of numbers
   (one value)           (one line)            (rows and columns)
      +-----+          +---+---+---+          +---+---+---+
      |  5  |          | 1 | 2 | 3 |          | 1 | 2 | 3 |
      +-----+          +---+---+---+          +---+---+---+
                                              | 4 | 5 | 6 |
                                              +---+---+---+
                                              | 7 | 8 | 9 |
                                              +---+---+---+
   <------------------- all of these are Tensors ------------------->
```

Here, we can see that a single number, a row of numbers, and a grid of numbers are all Tensors. They are just different sizes of the same idea, which is a container of numbers arranged in an organized way.

So, why do we need Tensors? Because computers understand numbers, not photos or words. A photo is just a grid of numbers, where each number is the brightness of a tiny dot. A piece of text is also turned into numbers. So, to teach a computer anything, we first turn it into numbers, and Tensors hold those numbers.

Let's create a Tensor in PyTorch as below:

```python
import torch
# create a Tensor with three numbers
x = torch.tensor([1.0, 2.0, 3.0])
print(x)
```

It will print the following:

```
tensor([1., 2., 3.])
```

Here, we have imported `torch`, which is the PyTorch library. Then we used `torch.tensor` to create a Tensor that holds three numbers. PyTorch confirmed it by printing the Tensor back to us.

This is how we store data in PyTorch. Now, let's understand the actual problem that PyTorch is built to solve.

## The problem PyTorch solves

Before jumping into the solution, we must understand the problem first.

The goal of machine learning is simple to say. We want the computer to learn a pattern from data, and that too without us writing the rule by hand.

Let's say we want the computer to learn the rule that converts a temperature in Celsius into Fahrenheit. We humans know the formula. But assume that we do not know it, and we want the computer to discover it from examples.

We give the computer some examples. When the input is 0, the answer is 32. When the input is 100, the answer is 212. We want the computer to figure out the rule on its own.

The computer starts with a random guess for the rule. The guess is wrong in the beginning. So, the computer checks how wrong it is, then slightly fixes the guess. It repeats this many times until the guess becomes very good.

This "check how wrong, then fix a little" loop is the heart of machine learning. But there is a hard part. To fix the guess correctly, the computer must know which direction to adjust each number, and by how much. This requires a lot of careful math called calculus.

Doing this math by hand for millions of numbers is impossible for us.

So, here comes PyTorch to the rescue. PyTorch does this hard math for us, automatically. To do that, PyTorch uses two powerful ideas. The first is the Computation Graph, and the second is Autograd. Let's understand both.

## What is a Computation Graph?

**A Computation Graph is a record of every math step that PyTorch performs, kept in the right order.**

In simple words, while we do our calculations, PyTorch quietly writes down each step like a recipe.

Let's say we calculate the following. We take a number `a`, multiply it by `b`, and then add `c`. PyTorch does not just give us the final answer. It also remembers that we first multiplied, and then we added.

Why does it remember? Because later, when the computer wants to fix its guess, it needs to walk backward through these steps. To walk backward, it must first know the forward path. The Computation Graph is that path.

Let's see this with an example as below:

```python
import torch
a = torch.tensor(2.0)
b = torch.tensor(3.0)
c = torch.tensor(4.0)
# PyTorch records each step
result = a * b + c
print(result)
```

It will print the following:

```
tensor(10.0)
```

We can picture the graph as below:

```text
    a (2)  ----+
               |
               v
            [ multiply ]  ----> 6 ----+
               ^                      |
               |                      v
    b (3)  ----+                  [ add ]  ----> result (10)
                                      ^
                                      |
    c (4)  ---------------------------+
```

Here, we can see that PyTorch first takes `a` and `b` into the multiply step to get `6`, and then takes that `6` along with `c` into the add step to get the final `result` of `10`. PyTorch records this whole path so that it can walk back through it later.

Here, we can see that PyTorch gave us the answer `10`, because 2 multiplied by 3 is 6, and 6 plus 4 is 10. But behind the scenes, PyTorch also built a small graph. It noted that there was a multiply step, and then an add step.

The best part is that PyTorch builds this graph as we write normal code. We do not have to build the graph ourselves. PyTorch builds it line by line while our program runs.

This is how PyTorch keeps track of our calculations. Now, let's understand how it uses this graph to do the hard math for us.

## What is Autograd?

**Autograd is the part of PyTorch that automatically calculates how to adjust each number to reduce the error.**

The word Autograd can be decomposed like below:

> Autograd = Auto + Gradient

"Auto" means automatic. A "Gradient" is just a fancy word for direction and amount of change. So, Autograd means "automatic calculation of which direction to change and by how much".

Let's understand the idea of a gradient in simple words. Suppose we are standing on a hill in thick fog, and we want to reach the bottom. We cannot see far. So, we feel the ground under our feet to find which way it slopes downward, then take a small step in that direction. We repeat this until we reach the bottom.

A [gradient](https://outcomeschool.com/blog/math-behind-gradient-descent) is exactly that slope. It tells the computer which way is "downhill", where downhill means "less error". The computer takes a small step downhill, again and again, until the error is very small.

Autograd calculates this slope for every number in our model, automatically, using the Computation Graph we just learned about.

To turn on this tracking, we tell PyTorch that a Tensor needs gradients. We can write the code as below:

```python
import torch
# tell PyTorch to track this number for gradients
x = torch.tensor(3.0, requires_grad=True)
# do a simple calculation
y = x * x
# ask PyTorch to calculate the gradient
y.backward()
print(x.grad)
```

It will print the following:

```
tensor(6.0)
```

Here, we have done a few things. First, we created a Tensor `x` with the value `3.0` and set `requires_grad=True`, which tells PyTorch to track it. Then we calculated `y` as `x` multiplied by `x`. After that, we called `y.backward()`, which tells PyTorch to walk backward through the graph and calculate the slope.

Finally, `x.grad` gave us the answer `6.0`. For the calculation `x * x`, the slope at `x = 3` is exactly `6`. PyTorch found this for us automatically. We did not do any calculus by hand.

This is the real magic of PyTorch. We write the forward calculation in plain code, and PyTorch handles all the backward math.

This backward walk through the graph is exactly what backpropagation does. We have a detailed blog on the [Math Behind Backpropagation](https://outcomeschool.com/blog/math-behind-backpropagation) that explains it step by step.

Now that we have learned about Tensors, the Computation Graph, and Autograd, it is time to put them together into a real training example.

## A complete training example

Let's go back to our temperature problem. We want the computer to learn the rule that turns Celsius into Fahrenheit, only from examples.

The real rule is "multiply by 1.8 and add 32". But we will pretend we do not know it. We will let PyTorch discover the multiply number and the add number on its own.

Let's see the code for the full training loop as below:

```python
import torch
# our examples: Celsius inputs and the correct Fahrenheit answers
celsius = torch.tensor([0.0, 100.0])
fahrenheit = torch.tensor([32.0, 212.0])
# start with random guesses, and track them for gradients
weight = torch.tensor(0.0, requires_grad=True)
bias = torch.tensor(0.0, requires_grad=True)
learning_rate = 0.0001
# repeat the learning loop many times
for step in range(100000):
    # make a prediction with the current guess
    prediction = weight * celsius + bias
    # measure how wrong we are (the error)
    error = ((prediction - fahrenheit) ** 2).mean()
    # ask PyTorch to calculate the gradients
    error.backward()
    # take a small step downhill, then reset for the next round
    with torch.no_grad():
        weight -= learning_rate * weight.grad
        bias -= learning_rate * bias.grad
        weight.grad.zero_()
        bias.grad.zero_()
print(weight, bias)
```

We can picture the learning loop as below:

```text
        +-------------------------------------------------+
        |                                                 |
        v                                                 |
   make a prediction with the current weight and bias     |
        |                                                 |
        v                                                 |
   measure how wrong the prediction is (the error)        |
        |                                                 |
        v                                                 |
   error.backward() finds the slopes (gradients)          |
        |                                                 |
        v                                                 |
   nudge weight and bias a small step downhill            |
        |                                                 |
        +------------------- repeat ----------------------+
```

Here, we can see that the loop keeps going round and round. Each round we predict, measure the error, find the slopes, and take a small step downhill. With every round the error gets smaller, until `weight` is near `1.8` and `bias` is near `32`.

Here, we have done the complete learning cycle. Let me explain each part slowly.

- We created `celsius` and `fahrenheit` Tensors. These are our examples, the input and the correct answer.
- We created `weight` and `bias` as our guesses, starting at zero, and we set `requires_grad=True` so PyTorch tracks them.
- The `learning_rate` is the size of each small step. A small step keeps the learning safe and steady.
- Inside the loop, `prediction` is the computer's current guess for the answer.
- The `error` measures how far the guess is from the correct answer. A bigger number means a worse guess.
- `error.backward()` tells PyTorch to calculate the gradients, which are the slopes for `weight` and `bias`.
- Then we nudge `weight` and `bias` a little in the downhill direction, which reduces the error.
- Finally, we reset the gradients with `zero_()` so the next round starts fresh.

After the loop runs many times, the `weight` becomes close to `1.8` and the `bias` becomes close to `32`. The computer discovered the rule on its own. We never told it the formula.

**Note:** We run the loop for a large number of times here, around `100000`. The reason is that our Celsius inputs are not scaled, which means the numbers like `0` and `100` are very different in size. When the inputs are not scaled, the learning becomes slow, and the `bias` in particular takes many rounds to reach `32`. In real projects, we usually scale the inputs first so that the model learns much faster. For this simple example, we keep it as it is and just run more rounds.

Let's also see the idea as a small step-by-step walkthrough for the very first rounds:

- **Step 1:** weight = 0, bias = 0, so the prediction is very wrong, and the error is huge.
- **Step 2:** PyTorch finds the slopes, and we nudge weight and bias a little. The error gets smaller.
- **Step 3:** We repeat. The prediction gets closer to the correct answer each time.
- **Final step:** weight is near 1.8, bias is near 32, and the error is very small.

This is how a machine learning model learns inside PyTorch. The same loop, with more numbers and more steps, is how huge models are trained too.

This was all about the training loop. Now, let's understand one more thing that makes PyTorch fast.

## What is the GPU and why does PyTorch use it?

**A GPU is a special chip in the computer that can do a huge number of simple math operations at the same time.**

In simple words, the [GPU](https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning) is built for speed when we have a lot of small calculations.

Let's use an analogy. Suppose we have to deliver one thousand letters. A CPU is like one very fast person delivering them one after another. A GPU is like one thousand normal people, each delivering one letter at the same time. For this kind of work, the crowd finishes much faster.

Machine learning has millions of small math operations, mostly on Tensors. So, the GPU is perfect for it.

The beautiful thing about PyTorch is that moving our work to the GPU is very simple. We can write the code as below:

```python
# move the Tensor to the GPU if one is available
device = "cuda" if torch.cuda.is_available() else "cpu"
x = torch.tensor([1.0, 2.0, 3.0]).to(device)
print(x)
```

Here, we have checked if a GPU is available. The word `cuda` is the name PyTorch uses for many GPUs. If a GPU is present, we move the Tensor to it using `.to(device)`. If not, we stay on the `cpu`. The rest of our code stays the same.

We have a detailed blog on [how CUDA Kernels work](https://outcomeschool.com/blog/how-do-cuda-kernels-work) that explains what actually runs on the GPU behind the scenes.

This is how PyTorch makes our training fast without making our code complicated. It enables us to do complex things very simply. It provides us the power.

Now, we have understood the GPU. Let's finish with why PyTorch became so loved.

## Why is PyTorch so popular?

We have already seen the main reasons, so let me put them together.

- PyTorch builds the Computation Graph as our code runs, line by line. This makes it easy to read, easy to test, and easy to fix when something goes wrong.
- Autograd does all the hard calculus for us, so we focus on our idea, not on the math.
- It works smoothly with Python, which is simple to learn and read.
- It uses the GPU with a single small change in the code, so our training becomes fast.
- It is free, open-source, and supported by a very large community, so help is always available.

These reasons together make PyTorch a favourite for students, researchers, and big companies alike.

Let's quickly map the main pieces to simple roles for better understanding:

| PyTorch piece | Simple role |
| --- | --- |
| Tensor | The box that holds our numbers |
| Computation Graph | The recipe that records every math step |
| Autograd | The helper that finds the downhill direction |
| GPU | The crowd that does the math fast |

Here, we can see the full picture. The Tensor holds the data. The Computation Graph remembers the steps. Autograd uses those steps to find how to improve. The GPU makes it all run fast.

Now, we have understood how PyTorch works. We started with Tensors, learned how PyTorch records our steps in a Computation Graph, saw how Autograd does the hard math automatically, ran a full training loop where the computer learned a rule on its own, and finally saw how the GPU makes everything fast.

## Frequently Asked Questions

### Do we need to build the computation graph ourselves in PyTorch?

No. PyTorch builds the computation graph as our code runs, line by line. We just write normal code for the forward calculation, and PyTorch quietly records each math step in the right order. This also makes the code easy to read, easy to test, and easy to fix.

### Do we need a GPU to use PyTorch?

No. PyTorch works on the CPU too. A GPU only makes training faster, because it can do a huge number of simple math operations at the same time. We check if a GPU is available, move the Tensor to it with `.to(device)`, and otherwise stay on the CPU, while the rest of the code stays the same.

### What does requires\_grad=True do in PyTorch?

It tells PyTorch to track a Tensor for gradients. When we later call `backward()` on a result, PyTorch walks backward through the computation graph and calculates the gradient for every tracked Tensor. We then read that gradient from the Tensor's `grad` value.

### Why do we reset the gradients in every training round?

We reset the gradients with `zero_()` so that the next round starts fresh. In each round, we make a prediction, measure the error, calculate the gradients, and nudge the numbers a small step downhill. Resetting keeps each round working on its own new gradients.

### Why can a simple PyTorch training loop need so many rounds?

One reason is that the inputs are not scaled. When input numbers like 0 and 100 are very different in size, learning becomes slow, and some values take many rounds to reach the right answer. In real projects, we usually scale the inputs first so that the model learns much faster.
