---
title: What are Variational Autoencoders (VAEs) and How Do They Work?
module: 15
module_title: Multimodal AI and Generative Models
lesson: '15.6'
source: https://outcomeschool.com/blog/variational-autoencoders
published: June 2, 2026
tags:
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 3419
reading_time: 17
status: full
---
# What are Variational Autoencoders (VAEs) and How Do They Work?

> **Module 15 · Lesson 15.6**  
> Source: [Outcome School](https://outcomeschool.com/blog/variational-autoencoders) · Published: June 2, 2026 · Reading time: ~17 min · Tags: `ai`, `machine-learning`

---

![Variational Autoencoders](../../assets/images/15-15-06-what-are-variational-autoencoders-vaes-and-how-do-they-work/variational-autoencoders.png)

A Variational Autoencoder (VAE) is a special type of Autoencoder that learns a smooth and organized latent space, so that we can pick any random point from it and generate brand new, meaningful data like images.

In this blog, we will learn about Variational Autoencoders. We will understand what they are, why we need them, how they work step by step, and how they are able to generate brand new data like images that never existed before.

We will cover the following:

- What is an Autoencoder?
- The problem with a normal Autoencoder
- What is a Variational Autoencoder?
- The encoder, the latent space, and the decoder
- The reparameterization trick
- The loss function of a Variational Autoencoder
- A simple example walk-through
- A simple code example
- Advantages of Variational Autoencoders
- Where Variational Autoencoders are used

Let's get started.

### What is an Autoencoder?

Before jumping into Variational Autoencoders, we must first understand a normal Autoencoder.

In simple words, **Autoencoder = Encoder + Decoder**.

An Autoencoder is a [neural network](https://outcomeschool.com/blog/neural-network) that learns to compress data into a small form and then rebuild the original data back from that small form.

It has two parts:

- **Encoder:** It takes the input, like an image, and squeezes it down into a small set of numbers. This small set of numbers is called the **latent vector** or the **code**.
- **Decoder:** It takes that small set of numbers and tries to rebuild the original input from it.

Let's say we have a photo of a handwritten digit `7`. The encoder reads this photo and compresses it into a small list of numbers, for example just 2 numbers. The decoder then takes these 2 numbers and tries to draw the digit `7` back.

The space where these small numbers live is called the **latent space**. The word "latent" simply means "hidden". So, the latent space is the hidden compressed space where the encoder stores the most important features of the data.

So, why do we even compress the data? Because by forcing the network to squeeze everything into a few numbers, we force it to learn only the most important features of the data and throw away the noise.

We train the Autoencoder by comparing the rebuilt output with the original input. If they are different, we tell the network to fix itself. Over time, the network gets very good at rebuilding the input. This is called **reconstruction**.

### The problem with a normal Autoencoder

Now, here is the catch.

A normal Autoencoder is great at rebuilding the inputs it has already seen. But it is bad at creating new data that it has never seen.

Let's understand why.

When a normal Autoencoder learns, it places each input at some point in the latent space. The image of a `7` goes to one point. The image of a `3` goes to another point. But these points can be scattered all over the place with big empty gaps between them.

Now, suppose we want to generate a brand new digit that the model has never seen. To do this, we would pick a random point in the latent space and ask the decoder to draw something from it.

But here is the problem. If we pick a random point, it could easily land in one of those empty gaps. The decoder has never seen anything in that gap during training. So, it produces garbage, which means a blurry mess that does not look like any digit.

So, the latent space of a normal Autoencoder is **not continuous and not organized**. There are holes and gaps everywhere. We cannot safely pick a random point and expect a meaningful output.

We needed a solution for that, and the Variational Autoencoder was introduced to solve this problem. So, here comes the Variational Autoencoder to the rescue.

### What is a Variational Autoencoder?

**A Variational Autoencoder, also called a VAE, is a special type of Autoencoder that learns a smooth and organized latent space, so that we can pick any random point from it and generate brand new, meaningful data.**

In simple words, **Variational Autoencoder = Autoencoder + a smooth, organized latent space**.

So, what is the key difference?

A normal Autoencoder maps each input to a single point in the latent space.

But a Variational Autoencoder maps each input to a small region in the latent space, not a single point. It describes this region using a probability distribution.

Do not worry if the word "distribution" sounds heavy. Let's understand it in simple words.

A **distribution** is just a way of saying "the value is most likely around here, and a little less likely as we move away". For example, the heights of people follow a distribution. Most people are around the average height, and very few people are extremely short or extremely tall.

The most common distribution is the **normal distribution**, also called the **Gaussian distribution** or the **bell curve**. A normal distribution is fully described by just two numbers:

- **Mean, written as `mu`:** the center of the distribution.
- **Standard deviation, written as `sigma`:** how spread out the distribution is around the center.

So, instead of saying "this `7` lives exactly at point 1.5", the Variational Autoencoder says "this `7` lives somewhere around 1.5, give or take a little". This little spread is the key trick.

Because every input now covers a small region instead of a single point, these regions start to overlap and fill the gaps. So, the latent space becomes smooth and continuous with no holes. And when there are no holes, we can pick any random point and the decoder will produce something meaningful.

### The encoder, the latent space, and the decoder

Now, let's understand the three parts of a Variational Autoencoder.

The best way to learn this is by taking an example.

Suppose we feed an image of a handwritten digit into the Variational Autoencoder.

**The encoder.** The encoder reads the image. But instead of outputting one latent vector, it outputs two things: a mean `mu` and a standard deviation `sigma`. Together, these two numbers describe a normal distribution in the latent space. So, the encoder is telling us, "this digit lives in this region of the latent space".

**The latent space.** From the distribution given by `mu` and `sigma`, we pick a random sample. This random sample is our latent vector `z`. Because we pick `z` randomly from the region, the same input can produce slightly different `z` values each time. So, the decoder learns to rebuild the input not just from one exact point, but from the whole small region around it. This is what fills the gaps and makes the space smooth.

**The decoder.** The decoder takes the sampled latent vector `z` and rebuilds the image from it. The goal is for the rebuilt image to look like the original input.

We can visualize the full flow of a Variational Autoencoder as below:

```
        Input Image
             |
             v
         Encoder
             |
        +----+----+
        |         |
        v         v
       mu       sigma
        |         |
        +----+----+
             |
             v
   Sample z from the distribution
             |
             v
         Decoder
             |
             v
      Rebuilt Image
```

Here, we can see that the encoder turns the input into `mu` and `sigma`. Then we sample a latent vector `z` from the distribution described by `mu` and `sigma`. Finally, the decoder rebuilds the image from `z`.

### The reparameterization trick

Now, there is one problem we must solve.

We just said we pick a random sample `z` from the distribution. But picking a random sample is a random operation. And during training, a neural network learns using a method called [**backpropagation**](https://outcomeschool.com/blog/math-behind-backpropagation), which needs to flow gradients smoothly through every step.

In simple words, backpropagation is how the network figures out how to adjust itself to reduce its mistakes. It must be able to trace the path from the output back to every input. But a random sampling step blocks this path, because we cannot take a gradient through pure randomness.

So, here comes the **reparameterization trick** to the rescue.

The idea is simple. Instead of directly picking a random `z` from the distribution, we rewrite the sampling as below:

```
z = mu + sigma * epsilon
```

Here:

- `mu` is the mean from the encoder.
- `sigma` is the standard deviation from the encoder.
- `epsilon` is a random number drawn from a standard normal distribution with mean 0 and standard deviation 1. This is the same bell curve we learned about above, centered at 0.

Here, we have moved all the randomness into `epsilon`. And `epsilon` does not depend on the network at all. It is just an outside random number.

So now, `mu` and `sigma` are clean, smooth values that the network can learn. The randomness sits only in `epsilon`, which is outside the path of learning. This means backpropagation can now flow smoothly through `mu` and `sigma`, while the randomness is handled separately by `epsilon`.

We can visualize the trick like below:

```
   Before (random step lies on the path):
   forward    mu, sigma  ====>  [ random sampling ]  ====>  z
   backward   mu, sigma  <==X==   blocked            <====  z
   After (random step moved off the path):
                                  epsilon
                                     |
                                     v
   forward    mu, sigma  ====>  mu + sigma * epsilon  ====>  z
   backward   mu, sigma  <==============================  z
```

Here, the top row is the forward path and the bottom row is the backward gradient. In the "Before" case, the gradient hits the random sampling step and gets blocked, so `mu` and `sigma` never learn. In the "After" case, the path from `mu` and `sigma` to `z` is plain multiply and add, so the gradient flows all the way back. The only random part, `epsilon`, sits off to the side. This is how the reparameterization trick keeps the network trainable.

This simple trick is what makes the whole Variational Autoencoder trainable. It is the heart of the VAE.

### The loss function of a Variational Autoencoder

Now, let's understand how a Variational Autoencoder learns. The network learns by reducing a loss. The loss is made of two parts added together.

**Part 1: Reconstruction loss.** This part checks how close the rebuilt image is to the original image. If the rebuilt image is very different from the original, this loss is high. If the rebuilt image looks just like the original, this loss is low. So, this part pushes the decoder to rebuild the input correctly.

**Part 2: KL divergence loss.** This is the new and special part of a Variational Autoencoder.

In simple words, **KL divergence** measures how different one distribution is from another distribution. Here, it measures how different the distribution produced by the encoder is from a standard normal distribution with mean 0 and standard deviation 1.

So, this part gently pulls every encoded region towards the center of the latent space and keeps them all neatly packed together around one common point. This is exactly what removes the gaps and makes the latent space smooth and organized. Without this part, the encoder would push the regions far apart and the gaps would come back.

So, the full loss is:

**Total Loss = Reconstruction Loss + KL Divergence Loss**

Now, notice the balance between these two parts.

- The reconstruction loss wants each input to be perfectly rebuilt, which pushes the regions apart so they do not get confused with each other.
- The KL divergence loss wants all the regions to be packed neatly around the center.

These two parts pull against each other. The network finds a healthy balance between them. This balance is what gives us a latent space that is both accurate and smooth.

### A simple example walk-through

Let's take a small example to make this concrete.

Suppose we feed an image of the digit `7` into the Variational Autoencoder. For the sake of understanding, let's say our latent space has just 1 dimension, which means `mu`, `sigma`, and `z` are all single numbers.

**Step 1:** The encoder reads the image of `7` and outputs:

- `mu` = 1.5
- `sigma` = 0.2

So, the encoder is saying, "the digit `7` lives around 1.5 in the latent space, with a small spread of 0.2".

**Step 2:** We draw a random `epsilon` from a standard normal distribution. Let's say we get:

- `epsilon` = 0.5

**Step 3:** We compute the latent vector `z` using the reparameterization trick:

- `z` = `mu` + `sigma` \* `epsilon`
- `z` = 1.5 + 0.2 \* 0.5
- `z` = 1.5 + 0.1
- `z` = 1.6

**Step 4:** We feed `z` = 1.6 into the decoder. The decoder rebuilds an image of the digit `7`.

**Step 5:** We compare the rebuilt `7` with the original `7` to get the reconstruction loss. We also compute the KL divergence loss to keep the distribution close to the standard normal. We add both losses and update the network.

Now, here is the beautiful part. The next time we feed the same `7`, the random `epsilon` will be different, so `z` becomes a slightly different value like 1.55 or 1.62 or 1.48. This means the whole small region around 1.5 learns to produce a `7`. There are no sharp holes. This is what makes the space smooth.

So, after training, if we want to generate a brand new digit, we simply pick any random point from the center region of the latent space and feed it straight to the decoder. We can pick from the center because the KL divergence loss packed all the regions around the center. Since the space is smooth and has no gaps, the decoder produces a clean, meaningful digit that never existed before.

It works perfectly.

### A simple code example

Let's see a simple code example of a Variational Autoencoder in [PyTorch](https://outcomeschool.com/blog/how-does-pytorch-work) as below:

```python
import torch
import torch.nn as nn
class VAE(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Linear(784, 400)
        self.fc_mu = nn.Linear(400, 2)      # produces mu
        self.fc_sigma = nn.Linear(400, 2)   # produces log of sigma
        self.decoder = nn.Sequential(
            nn.Linear(2, 400), nn.ReLU(),
            nn.Linear(400, 784), nn.Sigmoid()
        )
```

Here, we have defined the building blocks. The `encoder` reads the input image, which is `784` numbers for a 28 by 28 pixel image. From the encoder, `fc_mu` produces the mean `mu` and `fc_sigma` produces the spread, which we keep in the log form for stability. Our latent space has `2` dimensions. The `decoder` takes the `2` latent numbers and rebuilds the `784` pixels back.

Now, let's add the forward pass with the reparameterization trick as below:

```python
    def forward(self, x):
        h = torch.relu(self.encoder(x))
        mu = self.fc_mu(h)
        log_sigma = self.fc_sigma(h)
        epsilon = torch.randn_like(mu)              # random number
        z = mu + torch.exp(log_sigma) * epsilon     # reparameterization
        return self.decoder(z), mu, log_sigma
```

Here, we can see the full flow. First, the encoder reads the input `x`. Then we get `mu` and `log_sigma`. After that, we draw a random `epsilon` using `torch.randn_like`. Then we apply the reparameterization trick to get `z`. Finally, the decoder rebuilds the image from `z`, and we also return `mu` and `log_sigma` so we can compute the loss.

**Note:** We let the network output `log_sigma` instead of `sigma` directly. This is a common trick to keep the training stable and to make sure the spread is always a positive number. The meaning stays the same as our simple formula `z = mu + sigma * epsilon`. We just recover `sigma` from `log_sigma` using `torch.exp`.

Now, let's see the loss function as below:

```python
def vae_loss(rebuilt, original, mu, log_sigma):
    recon = nn.functional.mse_loss(rebuilt, original, reduction='sum')
    kl = -0.5 * torch.sum(1 + 2 * log_sigma - mu.pow(2) - torch.exp(2 * log_sigma))
    return recon + kl
```

Here, we have the two parts of the loss. The `recon` is the reconstruction loss that checks how close the rebuilt image is to the original. The `kl` is the KL divergence loss that keeps the distribution close to a standard normal. We add both and return the total loss. This is exactly the **Total Loss = Reconstruction Loss + KL Divergence Loss** that we learned above.

### Advantages of Variational Autoencoders

Now, let's see the advantages of Variational Autoencoders.

- **Generation of new data:** A Variational Autoencoder can create brand new data, like new images, that never existed before. We simply pick a random point in the latent space and the decoder draws something meaningful.
- **Smooth latent space:** The latent space is smooth and continuous with no holes. So, if we slowly move from one point to another point, the generated output also changes slowly and smoothly. For example, a digit can slowly morph from a `4` into a `9`, passing through shapes that look in between.
- **Organized structure:** Similar inputs end up close to each other in the latent space. This makes the space easy to understand and explore.
- **Stable training:** Compared to some other [generative models](https://outcomeschool.com/blog/what-is-generative-ai), a Variational Autoencoder is easier and more stable to train, because its loss is clear and well behaved.

That's the beauty of a Variational Autoencoder.

### Where Variational Autoencoders are used

Now, let's see where Variational Autoencoders are used.

- **Image generation:** They are used to generate new images such as faces, digits, and objects.
- **Anomaly detection:** A Variational Autoencoder learns what normal data looks like. So, if it sees something it cannot rebuild well, that data is likely an anomaly. This is used to detect fraud and faults.
- **Data compression:** Since the encoder squeezes data into a small latent vector, it can be used to compress data.
- **Drug discovery:** They are used to generate new molecule structures that could become new medicines.
- **Denoising:** A Variational Autoencoder can take a noisy input and produce a clean version of it.

Variational Autoencoders are one of the foundation ideas behind modern generative models. The core idea of learning a smooth latent space and sampling from it is used in many advanced systems today, including modern [diffusion models](https://outcomeschool.com/blog/diffusion-models) such as Stable Diffusion, which use a Variational Autoencoder to build the latent space they work in. Other generative model families take a different route - for example, [Generative Adversarial Networks (GANs)](https://outcomeschool.com/blog/generative-adversarial-networks) learn by pitting two networks against each other, and [autoregressive models](https://outcomeschool.com/blog/autoregressive-models) build new data one piece at a time instead of sampling from a latent space all at once.

The same encoder idea also powers AI agents that compress raw observations into a compact latent state, and we have a detailed blog on [How do World Models work?](https://outcomeschool.com/blog/how-do-world-models-work) that explains this end to end.

This was all about Variational Autoencoders.

Now we must have understood what a Variational Autoencoder is, why we need it, how it works step by step, and how it generates brand new data.

## Frequently Asked Questions

### Can a normal Autoencoder generate new data?

Not reliably. A normal Autoencoder is great at rebuilding inputs it has already seen, but it is bad at creating new data. Its latent space has big empty gaps between points. If we pick a random point that lands in a gap, the decoder produces a blurry mess that does not look like any real data.

### What happens if we remove the KL divergence loss from a VAE?

The gaps in the latent space come back. The KL divergence loss gently pulls every encoded region towards the center and keeps them packed together. Without it, the reconstruction loss would push the regions far apart, and we could no longer pick a random point and expect a meaningful output.

### Why does a VAE encoder output log sigma instead of sigma?

It outputs log sigma to keep training stable and to make sure the spread is always a positive number. The meaning stays the same as the formula z equals mu plus sigma times epsilon. We simply recover sigma from log sigma using the exponential function before applying the reparameterization trick.

### How is a VAE different from a GAN?

A VAE learns a smooth latent space and generates new data by sampling a point from it and passing it to the decoder. A GAN learns by pitting two networks against each other instead. Compared to some other generative models, a VAE is easier and more stable to train, because its loss is clear and well behaved.

### How is a VAE related to Stable Diffusion?

Stable Diffusion uses a Variational Autoencoder to build the latent space it works in. The core idea of a VAE, learning a smooth latent space and sampling from it, is used in many advanced systems today. Variational Autoencoders are one of the foundation ideas behind modern generative models.
