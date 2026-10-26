---
title: What is Dropout in Neural Networks and How Does It Work?
module: 2
module_title: Deep Learning and Neural Networks
lesson: '2.7'
source: https://outcomeschool.com/blog/dropout-in-neural-networks
published: June 5, 2026
tags:
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 2606
reading_time: 13
status: full
---
# What is Dropout in Neural Networks and How Does It Work?

> **Module 2 · Lesson 2.7**  
> Source: [Outcome School](https://outcomeschool.com/blog/dropout-in-neural-networks) · Published: June 5, 2026 · Reading time: ~13 min · Tags: `ai`, `machine-learning`

---

![Dropout in Neural Networks](../../assets/images/02-02-07-what-is-dropout-in-neural-networks-and-how-does-it-work/dropout-in-neural-networks.png)

Dropout is a technique where we randomly switch off some neurons in a neural network during training, so that the network does not depend too much on any single neuron and does not overfit.

In this blog, we will learn about Dropout in Neural Networks. We will understand what it is, the problem it solves, how it works step by step with a simple example, and where it is used.

We will cover the following:

- What is Dropout?
- The problem of Overfitting
- Why do we need Dropout?
- How does Dropout work?
- A step-by-step example
- Dropout during training vs testing
- Dropout in code
- Variants of Dropout
- Advantages of Dropout
- Where Dropout is used

Let's get started.

### What is Dropout?

**Dropout is a technique where we randomly switch off some neurons in a [neural network](https://outcomeschool.com/blog/neural-network) during training, so that the network does not depend too much on any single neuron.**

Before we go deeper, let's understand one word - **neuron**.

A neural network is made of small units called **neurons**. Each neuron takes some numbers as input, does a small calculation, and passes a number forward to the next neurons. Many neurons connected together form a neural network. The network learns patterns from data using these neurons.

Now, the word "Dropout" simply means to remove something temporarily.

So, in simple words, during training, we randomly pick some neurons and switch them off for that moment. A switched-off neuron sends nothing forward, as if it does not exist for that one step.

We do this randomly again and again during training. So, every training step uses a slightly different version of the network.

Do not worry, we will understand exactly why we do this and how it helps.

### The problem of Overfitting

The best way to learn this is by taking an example.

Suppose we are preparing a student for a math exam.

Let's say the student studies from only one practice book. The student reads the same book again and again. After some time, the student memorizes every single question and its answer from that book.

Now, in the practice book, the student scores 100 out of 100. The student looks perfect.

But, here is the catch. In the real exam, the questions are slightly different. And now the student fails, because the student only memorized the practice book and did not actually learn the concepts.

This problem is called **Overfitting**.

**Overfitting happens when a model performs very well on the training data but performs poorly on new, unseen data.**

In simple words, the model memorizes the training data instead of learning the general pattern.

A neural network with many neurons is very powerful. So, it can easily memorize the training data. This is exactly the student who memorizes the practice book.

So, now we have a clear problem. We need a way to stop the network from memorizing and force it to actually learn the general pattern.

### Why do we need Dropout?

Now, let's understand the real reason behind Overfitting inside a neural network.

When we train a network normally, some neurons become very strong and the network starts depending heavily on them. These few neurons do most of the work, and the other neurons become lazy.

This is a problem. The network is now relying on a small group of neurons. This is called **co-adaptation**, which means a few neurons adapt together and start working as a fixed team. If this fixed team memorizes the training data, the whole network overfits.

So, how can we stop the network from relying on a fixed team of neurons? The answer is Dropout.

So, here comes Dropout to the rescue.

When we randomly switch off neurons during training, no neuron can be sure that its neighbors will be present. So, every neuron is forced to learn something useful on its own, instead of depending on a few strong neurons.

This breaks the fixed team. Every neuron must now pull its own weight. As a result, the network learns the general pattern instead of memorizing the training data.

This is how Dropout reduces Overfitting.

### How does Dropout work?

Now, it's time to learn how Dropout actually works inside the network.

Dropout uses one important number called the **dropout rate**, written as `p`.

**The dropout rate `p` is the probability that a neuron will be switched off during a training step.**

For example, if `p = 0.5`, then every neuron has a 50% chance of being switched off in that step. If `p = 0.2`, then every neuron has a 20% chance of being switched off.

So, during each training step, the following happens.

**Step 1:** For every neuron in a Dropout layer, we flip a coin based on the dropout rate `p`. Based on this, we decide whether the neuron stays on or gets switched off.

**Step 2:** Every switched-off neuron outputs 0 for that step. It is as if the neuron is not there.

**Step 3:** The remaining neurons that stayed on pass their values forward as usual.

**Step 4:** The network learns from this thinner version of itself for that one step.

**Step 5:** In the next training step, we flip the coins again. So, a different random set of neurons gets switched off.

So, every training step trains a slightly different, thinner network. Over many steps, we are effectively training many different networks that all share the same weights.

Let's picture this with a small network as below:

```
   Without Dropout (all neurons active)
   Input        Hidden         Output
   (o) ──────►  (o) ─┐
                     ├──────►  (o)
   (o) ──────►  (o) ─┘
   With Dropout (one neuron switched off)
   Input          Hidden       Output
   (o) ─┐
        ├──────►  (o) ──────►  (o)
   (o) ─┘
                  (X)
```

Here, we can see how the signal flows from the input neurons to the hidden neurons, and then to the output neuron. To keep the picture clean, we draw one line per neuron, but in a fully connected network every input neuron actually connects to every hidden neuron, and every hidden neuron connects to the output. In the top network, "Without Dropout", every neuron is active. In the bottom network, "With Dropout", one hidden neuron is switched off, marked with `(X)`. A switched-off neuron sends nothing forward and receives nothing, so all of its connections are removed for that one training step. The network is now thinner, and the remaining neuron must do the work on its own.

This is a very powerful idea. It is like training a huge team of smaller networks and then combining their strength into one final network.

Let's understand why this combining helps. Suppose we ask one person a tough question, the answer can be wrong. But if we ask many people and take the most common answer, the final answer is usually better. Dropout gives us this same benefit, because the final network behaves like many networks joined together.

### A step-by-step example

Let's take a small example to make this concrete.

Suppose a layer has 4 neurons. After their calculation, their output values are as below:

```
Neuron 1: 2.0
Neuron 2: 4.0
Neuron 3: 6.0
Neuron 4: 8.0
```

Now, let's apply Dropout with a dropout rate `p = 0.5`. So, each neuron has a 50% chance of being switched off.

Suppose the random coin flips switch off Neuron 2 and Neuron 4. So, their outputs become 0.

```
Neuron 1: 2.0
Neuron 2: 0.0   (dropped)
Neuron 3: 6.0
Neuron 4: 0.0   (dropped)
```

Here, we can see that Neuron 2 and Neuron 4 are switched off. They send nothing forward. Only Neuron 1 and Neuron 3 are active for this step.

Now, there is one important detail. Since half the neurons are switched off, the total signal going forward has become smaller. We do not want the next layer to suddenly receive a weaker signal.

So, we scale up the values of the active neurons to balance this. We divide each active value by the keep probability, which is `1 - p`. Here, `1 - p = 1 - 0.5 = 0.5`.

So, we divide each active value by 0.5, which means we multiply it by 2.

```
Neuron 1: 2.0 / 0.5 = 4.0
Neuron 2: 0.0
Neuron 3: 6.0 / 0.5 = 12.0
Neuron 4: 0.0
```

Here, we can see that the active neurons are scaled up. This keeps the overall strength of the signal roughly the same as before.

This scaling trick is called **inverted dropout**, and this is the standard way Dropout is done today. The benefit is that we do all the adjustment during training, so we do not need to change anything during testing.

This is how Dropout works on a single layer for a single training step.

### Dropout during training vs testing

Now, this is a very important point, so let's understand it carefully.

Dropout is only used during **training**. During **testing**, which means when we actually use the model to make predictions, we turn Dropout off.

Now, the question is: why do we turn it off during testing?

The answer is simple. During testing, we want the full power of the network. We want every neuron to participate so that we get a stable and reliable prediction. We do not want randomness in our final answer.

So, during testing, all neurons stay on. No neuron is switched off.

And because we already used inverted dropout during training, which scaled the values up, we do not need to do any extra adjustment during testing. The numbers already balance out.

> Dropout is on during training and off during testing.

This is one of the most common mistakes beginners do. So, we must always remember to keep Dropout active only during training.

### Dropout in code

The best way to understand this is by seeing it in code. Let's see how we add Dropout in a neural network using [PyTorch](https://outcomeschool.com/blog/how-does-pytorch-work) as below:

```python
import torch
import torch.nn as nn
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(p=0.5),   # drop 50% of neurons
    nn.Linear(256, 10)
)
```

Here, we can see what is happening.

- `nn.Linear(784, 256)` is a normal layer with 256 neurons.
- `nn.ReLU()` is the activation that decides the output of the neurons.
- `nn.Dropout(p=0.5)` is the Dropout layer. It switches off 50% of the neurons during training.
- `nn.Linear(256, 10)` is the final layer that gives the output.

So, the Dropout layer simply sits between two layers and randomly switches off the neurons coming from the previous layer.

Now, there is one more important thing. We must tell PyTorch when we are training and when we are testing. We can do this as below:

```python
model.train()   # Dropout is active
# ... run training here ...
model.eval()    # Dropout is turned off
# ... run testing here ...
```

Here, we can see that `model.train()` keeps Dropout active, and `model.eval()` turns Dropout off. This is exactly the training versus testing behavior we discussed above.

### Variants of Dropout

Now, let's briefly learn about a few variants of Dropout. The basic idea stays the same, but each variant is designed for a different situation.

- **Standard Dropout:** This is the one we learned above. We randomly switch off individual neurons in a layer. This is used most of the time.
- **Spatial Dropout:** This is used in Convolutional Neural Networks, which are networks used for images. Instead of switching off individual neurons, it switches off an entire group of related neurons at a time. This works better for image data.
- **DropConnect:** Instead of switching off neurons, it randomly switches off the connections between neurons. So, the neurons stay, but some links between them are removed.
- **Recurrent Dropout:** This is used in Recurrent Neural Networks, which are networks used for sequences like text and speech. It applies Dropout in a careful way so that it does not damage the memory of the sequence.

Do not worry if these variants feel new. The most important one to understand is Standard Dropout, and we have already learned it well.

### Advantages of Dropout

Now, let's list the main advantages of Dropout.

- **Reduces overfitting:** This is the main reason we use Dropout. It stops the network from memorizing the training data.
- **No dependency on single neurons:** Every neuron learns to be useful on its own, so the network does not rely on a fixed team of neurons.
- **Acts like many models in one:** Since every step trains a different thinner network, the final network behaves like a combination of many networks. This makes the predictions more robust.
- **Very simple to use:** We just add one Dropout layer. There is no complex math we need to write ourselves.
- **Works with almost any network:** We can use Dropout in many types of neural networks with very little effort.

That's the beauty of Dropout. It solves a big problem with a very simple idea.

### Where Dropout is used

Now, let's see where Dropout is used.

- **Image classification:** Dropout is used in deep networks that classify images, to stop them from memorizing the training images.
- **Natural Language Processing:** Dropout is used in models that work with text, such as language models and translation models.
- **Speech recognition:** Dropout is used in models that convert speech into text.
- **Almost every deep network:** Whenever a network is large and has a risk of overfitting, Dropout is one of the first techniques we reach for.

One thing to remember is the choice of the dropout rate `p`. A common value is between 0.2 and 0.5. A very high value can switch off too many neurons and the network will not learn well. A very low value will not help much against overfitting. So, we pick the value based on our use case.

This was all about Dropout in Neural Networks.

Now we must have understood what Dropout is, the problem of overfitting it solves, how it works step by step, and where it is used.

## Frequently Asked Questions

### What dropout rate should we use?

A common value for the dropout rate `p` is between 0.2 and 0.5. A very high value can switch off too many neurons, and the network will not learn well. A very low value will not help much against overfitting. So we pick the value based on our use case.

### Does a dropped neuron stay switched off for the rest of training?

No. A neuron is switched off only for that one training step. In the next step, we flip the coins again, so a different random set of neurons gets switched off. This way, every step trains a slightly different, thinner network that shares the same weights.

### Do we need to scale the outputs during testing?

No. With inverted dropout, we scale up the active neurons during training by dividing by the keep probability `1 - p`. Because all the adjustment happens during training, we do not need to change anything during testing. This is the standard way Dropout is done today.

### What happens if we forget to call model.eval() in PyTorch?

Dropout stays active, so neurons keep getting switched off at random while we make predictions. During testing, we want every neuron to participate and we do not want randomness in our final answer. Calling `model.eval()` turns Dropout off, and forgetting it is one of the most common mistakes beginners make.

### Is DropConnect the same as Dropout?

No. Dropout randomly switches off whole neurons. DropConnect keeps the neurons and instead randomly switches off the connections between them, so some links are removed. Both share the same basic idea of adding randomness during training.
