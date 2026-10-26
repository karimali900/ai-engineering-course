---
title: What are Generative Adversarial Networks (GANs) and How Do They Work?
module: 15
module_title: Multimodal AI and Generative Models
lesson: '15.5'
source: https://outcomeschool.com/blog/generative-adversarial-networks
published: June 4, 2026
tags:
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 3260
reading_time: 16
status: full
---
# What are Generative Adversarial Networks (GANs) and How Do They Work?

> **Module 15 · Lesson 15.5**  
> Source: [Outcome School](https://outcomeschool.com/blog/generative-adversarial-networks) · Published: June 4, 2026 · Reading time: ~16 min · Tags: `ai`, `machine-learning`

---

![Generative Adversarial Networks (GANs)](../../assets/images/15-15-05-what-are-generative-adversarial-networks-gans-and-how-do-they-work/generative-adversarial-networks.png)

A Generative Adversarial Network (GAN) is a Machine Learning system where two neural networks compete against each other, and through this competition, one of them learns to create new data that looks real.

In this blog, we will learn about Generative Adversarial Networks (GANs), one of the most fascinating ideas in Machine Learning that can create brand new images, faces, and art that never existed before.

We will cover the following:

- What is a Generative Adversarial Network (GAN)?
- The two players: Generator vs Discriminator
- The counterfeiter vs police analogy
- The adversarial training loop
- The loss function and the minimax game in simple words
- A tiny PyTorch-style code sketch
- The mode collapse problem
- Training stability
- Types of GANs (DCGAN, Conditional GAN, StyleGAN, CycleGAN)
- Real-world applications of GANs

Let's get started.

### What is a Generative Adversarial Network (GAN)?

A **Generative Adversarial Network (GAN)** is a Machine Learning system where two [neural networks](https://outcomeschool.com/blog/neural-network) compete against each other, and through this competition, one of them learns to create new data that looks real.

In simple words, a GAN is a system that learns to create fake things so convincing that they look completely real.

Let's break the name down:

> GAN = Generative + Adversarial + Network

- [**Generative**](https://outcomeschool.com/blog/what-is-generative-ai) means it generates, which means it creates new things, like new images.
- **Adversarial** means there is a fight, a competition between two sides.
- **Network** means we are using neural networks, which are the brains of Machine Learning.

So, a GAN is two neural networks fighting each other to learn how to create new data.

Let's say we want a computer to draw new human faces that no one has ever seen. These faces should look like real photographs, but they belong to no real person. A GAN can do exactly this.

The most interesting part is that a GAN learns to do this all by itself, just by looking at many real examples, and that too without anyone telling it exactly what to draw.

### The two players: Generator vs Discriminator

A GAN has two neural networks inside it. These are the two players of the game.

**Generator:** The first network is the **Generator**. Its job is to create fake data. It takes some random numbers as input and turns them into something, for example, a picture of a face.

**Discriminator:** The second network is the **Discriminator**. Its job is to look at a picture and decide one thing only, which means it answers a simple question: is this picture real or fake?

So, we have one network that creates fakes, and another network that catches fakes.

Here, the random numbers given to the Generator are very important. We call this random input the **noise** or the [**latent vector**](https://outcomeschool.com/blog/variational-autoencoders). A latent vector is just a small list of random numbers that acts like a seed. The Generator turns this random noise into a meaningful image. By changing the noise, we get a different image every time.

The Generator never sees the real images directly. It only learns from the feedback given by the Discriminator. This is the beauty of a GAN.

### The counterfeiter vs police analogy

The best way to learn this is by taking an example.

Let's say there is a **counterfeiter**, a person who makes fake currency notes. And there is the **police**, whose job is to catch fake notes.

Here is how the story goes:

- In the beginning, the counterfeiter is very bad at making fake notes. The notes look obviously fake.
- The police easily catch every fake note. This is easy in the start.
- But, the counterfeiter learns from getting caught. He improves and makes slightly better notes.
- Now, the police must also become smarter to catch these better fakes.
- This back and forth continues. Both keep getting better and better.
- Finally, the counterfeiter becomes so good that the fake notes look exactly like real notes, and even the police cannot tell the difference.

In our GAN:

- The counterfeiter is the **Generator**.
- The police is the **Discriminator**.
- The fake notes are the **fake images**.

So, both networks push each other to improve. The Generator becomes better at creating, and the Discriminator becomes better at judging. When the Generator wins, which means the Discriminator can no longer tell real from fake, our GAN is ready.

This is how two competing networks together produce something amazing.

### The adversarial training loop

Now, let's understand how the training actually happens, step by step.

Training a GAN means letting the two networks compete in repeated rounds. In each round, we train the Discriminator a little, and then we train the Generator a little.

**Step 1:** We take some real images from our dataset, for example, real photos of faces.

**Step 2:** The Generator takes random noise and creates some fake images.

**Step 3:** We show both the real images and the fake images to the Discriminator. We tell it which ones are real and which ones are fake. The Discriminator learns to tell them apart. So, the Discriminator gets better at catching fakes.

**Step 4:** Now, it is the Generator's turn. The Generator creates new fake images and shows them to the Discriminator. This time, the Generator wants to fool the Discriminator. If the Discriminator catches the fake, the Generator learns from this mistake and improves.

**Step 5:** We repeat these steps again and again, thousands of times.

Let's see a simple diagram of this loop as below:

```
  Random Noise
       |
       v
  [ Generator ] ----> Fake Images
                          |
  Real Images ----------> |
                          v
                  [ Discriminator ] ----> Real or Fake?
                          |
                          v
              Feedback to both networks
```

Here, we can see that the feedback goes back to both networks. The Discriminator uses the feedback to catch fakes better. The Generator uses the feedback to create better fakes.

Over time, the Generator becomes so good that its fake images look just like real images. This is how the adversarial training loop works.

### The loss function and the minimax game in simple words

Now, let's understand the maths part, but in very simple words. Do not worry, we will learn it slowly.

In Machine Learning, a **loss** is a number that tells us how wrong a network is. A high loss means the network is doing a bad job. A low loss means it is doing a good job. The network learns by trying to reduce its own loss.

In a GAN, the two networks have opposite goals. This is called a **minimax game**.

In simple words:

- The Discriminator wants to **maximize** its success, which means it wants to correctly catch every fake and approve every real.
- The Generator wants to **minimize** the Discriminator's success, which means it wants the Discriminator to fail at catching fakes.

So, one player is trying to win, and the other is trying to make the first player lose. This is why we call it a minimax game. One side maximizes, the other side minimizes.

Let's understand with simple numbers. The Discriminator gives a score between 0 and 1 for each image:

- A score close to 1 means "I think this is real."
- A score close to 0 means "I think this is fake."

Now:

- When the Discriminator sees a real image, it wants to give a score close to 1.
- When the Discriminator sees a fake image, it wants to give a score close to 0.
- But the Generator wants the Discriminator to give a score close to 1 for fake images, because that means the fake fooled the Discriminator.

So, both are pulling in opposite directions. They reach a balance point when the Discriminator can no longer tell real from fake, which means it gives a score of around 0.5 for everything, which is just like guessing. At this point, the Generator has won, and the fake images look truly real.

We can picture this tug-of-war on the score line as below:

```
  Discriminator pushes fake images this way
  <----------------------
  0.0 ----------- 0.5 ----------- 1.0
  "fake"        "unsure"        "real"
                (balance
                 point)
                       ---------------------->
                       Generator pushes fake images this way
```

Here, we can see that the score line runs from 0.0, which means fake, to 1.0, which means real, with 0.5 in the middle as the unsure balance point. The Discriminator tries to push the score of fake images toward 0.0, while the Generator tries to push the score of those same fake images toward 1.0. They pull in opposite directions, and when they meet at the 0.5 balance point, the Discriminator is only guessing and the fakes look real.

This is how the minimax game drives both networks to improve until the fakes become perfect.

### A tiny PyTorch-style code sketch

Now, let's see a small code sketch so that the idea becomes concrete. We will use PyTorch-style Python. [PyTorch](https://outcomeschool.com/blog/how-does-pytorch-work) is a popular Python library used to build neural networks. This is just for the sake of understanding, so we keep it short.

First, let's see the Generator as below:

```python
import torch.nn as nn
# The Generator turns random noise into an image
class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(100, 256),   # input is 100 random numbers
            nn.ReLU(),
            nn.Linear(256, 784),   # output is a 28x28 image (784 pixels)
            nn.Tanh()
        )
    def forward(self, noise):
        return self.net(noise)
```

Here, we can see the Generator:

- It takes `100` random numbers as input. This is the noise.
- It passes them through some layers.
- It outputs `784` numbers, which form a small `28x28` image.

Now, let's see the Discriminator as below:

```python
# The Discriminator decides if an image is real or fake
class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(784, 256),   # input is the image (784 pixels)
            nn.ReLU(),
            nn.Linear(256, 1),     # output is a single score
            nn.Sigmoid()           # squeezes the score between 0 and 1
        )
    def forward(self, image):
        return self.net(image)
```

Here, we can see the Discriminator:

- It takes an image of `784` pixels as input.
- It passes them through some layers.
- It outputs a single number between 0 and 1, which is the real-or-fake score.

Now, let's see the heart of the training loop as below:

```python
# First, train the Discriminator on real and fake images
real_score = discriminator(real_images)
fake_images = generator(noise)
fake_score = discriminator(fake_images.detach())
d_loss = loss_fn(real_score, ones) + loss_fn(fake_score, zeros)
d_loss.backward()
d_optimizer.step()
# Then, train the Generator to fool the Discriminator
fake_score = discriminator(generator(noise))
g_loss = loss_fn(fake_score, ones)   # Generator wants fakes labeled as real
g_loss.backward()
g_optimizer.step()
```

Here, we can notice the key idea:

- For the Discriminator, real images are labeled `ones` (real) and fake images are labeled `zeros` (fake). It learns to tell them apart.
- For the Generator, the fake images are labeled `ones`, because the Generator wants the Discriminator to believe the fakes are real.
- `detach()` is used so that we do not update the Generator while training the Discriminator.

This is how the two networks are trained one after the other in every round.

### The mode collapse problem

Now, let's discuss a common problem in GANs called **mode collapse**.

**Mode collapse** happens when the Generator stops being creative and keeps producing the same output again and again.

Let's say we are training a GAN to create images of all digits from 0 to 9. But the Generator discovers that creating only the digit "8" fools the Discriminator very well. So, it gets lazy and keeps creating only "8" again and again, ignoring all other digits.

This is bad, because our GAN was supposed to create a variety of images, but now it produces only one type. The Generator collapsed into a single mode, which means a single kind of output. This is why we call it mode collapse.

Let's compare the good case and the collapsed case like below:

```
  GOOD case (variety):
  [ Generator ] ----> 0 1 2 3 4 5 6 7 8 9
  COLLAPSED case (mode collapse):
  [ Generator ] ----> 8 8 8 8 8 8 8 8 8 8
```

Here, we can see that in the good case the Generator produces a variety of digits from 0 to 9, just as we wanted. But in the collapsed case the Generator keeps producing only the digit "8" again and again. The output has lost all its variety, and this is exactly what mode collapse looks like.

So, mode collapse means the GAN loses variety and keeps repeating itself.

There are techniques to reduce this problem, for example, changing the loss function, adding more variety in training, and using improved GAN designs. But we must always watch out for mode collapse while training a GAN.

### Training stability

Now, let's understand why GANs are known to be hard to train.

In a normal Machine Learning model, we train one network, and we just try to reduce one loss. It is simple. But in a GAN, we are training two networks that fight each other. This makes the training delicate.

Here are the common issues we face:

- **One side becomes too strong.** If the Discriminator becomes too good too fast, the Generator gets no useful feedback and stops learning. If the Generator becomes too good too fast, the Discriminator gets confused.
- **The training does not settle.** Since both keep changing, the balance can keep shifting, and the networks may never reach a calm point.
- **Mode collapse**, which we just learned about.

So, training a GAN is like balancing two children on a see-saw. If one side is too heavy, the see-saw stops working. We must keep both sides balanced.

To improve training stability, we can do the following:

- Keep the learning of both networks at a similar pace.
- Use better network designs like DCGAN.
- Use improved loss functions that give smoother feedback.

This is how we keep our GAN training stable.

Diffusion Models later improved on this very instability, which is why they have largely overtaken GANs for image generation today. We have a detailed blog on [Diffusion Models](https://outcomeschool.com/blog/diffusion-models) that covers this end to end.

### Types of GANs (DCGAN, Conditional GAN, StyleGAN, CycleGAN)

After the first GAN was introduced, many improved versions came into the picture. Now, let's briefly understand the most popular ones.

**DCGAN (Deep Convolutional GAN):** This GAN uses convolutional layers, which are special layers that are very good at understanding images. DCGAN made GANs much better and more stable at generating clear images. It is one of the most common starting points for image generation.

**Conditional GAN (cGAN):** In a normal GAN, we cannot control what the Generator creates. We just get a random image. In a **Conditional GAN**, we can give an extra instruction, called a condition. For example, we can tell it to create the digit "7" specifically, and it will create a "7". So, a Conditional GAN gives us control over the output.

**StyleGAN:** This is a very advanced GAN created by NVIDIA. It is famous for creating extremely realistic human faces. StyleGAN also lets us control the style of the image, for example, the hair, the age, or the expression of a face. The website that shows "this person does not exist" is powered by StyleGAN.

**CycleGAN:** This GAN is used to convert one type of image into another type without needing matching pairs of images. For example, it can turn a photo of a horse into a zebra, or turn a summer scene into a winter scene, or turn a normal photo into a painting in the style of a famous artist. CycleGAN learns the translation between two worlds of images.

Let me tabulate the differences between these GAN types so that you can decide which one to use based on your use case:

| GAN Type | Main Idea | Common Use |
| --- | --- | --- |
| DCGAN | Uses convolutional layers for images | Clear, stable image generation |
| Conditional GAN | Adds a condition to control output | Generating a specific category |
| StyleGAN | Controls style and detail of images | Highly realistic faces |
| CycleGAN | Translates one image type to another | Style transfer, photo conversion |

This is how different GANs solve different kinds of problems.

### Real-world applications of GANs

Now, let's see where GANs are actually used in the real world. This is the most exciting part.

- **Image generation:** GANs can create brand new images of faces, animals, objects, and more. These images look real but belong to no real thing.
- **Deepfakes:** GANs can swap one person's face onto another person's video. This is powerful technology, and we must use it responsibly, because it can also be misused to spread false information.
- **Super-resolution:** GANs can take a blurry, low-quality image and turn it into a sharp, high-quality image. This is very useful for old photos and low-quality videos.
- **Art and design:** GANs can create original digital art, paintings, and designs. Artists use GANs as a creative tool.
- **Photo editing:** GANs can change a person's hairstyle, age, or expression in a photo. They can also remove or add objects in an image.
- **Data generation:** Sometimes we do not have enough real data to train a model. GANs can create extra realistic data to help train other Machine Learning models.
- **Medical imaging:** GANs can help create medical images for research and can improve the quality of scans.

So, now we know where we can use GANs.

Because this generated content can look completely real, we also need a way to tell machine-made content apart from human-made content. We have a detailed blog on [How Does LLM Watermarking Work?](https://outcomeschool.com/blog/how-does-llm-watermarking-work) that explains how a hidden signal is placed inside generated content and read back later.

GANs changed the way computers create. With just two networks competing against each other, we can generate images, art, and data that look completely real. This is the power of a Generative Adversarial Network, and that too learned almost entirely by the machine on its own.

## Frequently Asked Questions

### Does the Generator in a GAN ever see real images?

No. The Generator never sees the real images directly. It takes random noise as input and only learns from the feedback given by the Discriminator. When the Discriminator catches a fake, the Generator learns from this mistake and improves its next fakes.

### What does it mean when the Discriminator gives a score of 0.5?

A score of around 0.5 means the Discriminator can no longer tell real from fake and is just guessing. This is the balance point of the minimax game. At this point, the Generator has won, and the fake images look truly real.

### Can we control what a GAN generates?

Yes, with a Conditional GAN. In a normal GAN, we cannot control what the Generator creates, and we just get a random image. A Conditional GAN takes an extra instruction called a condition, so we can ask it to create a specific category, for example, the digit "7".

### Are GANs still the best choice for image generation?

Not today, since Diffusion Models have largely overtaken GANs for image generation. Diffusion Models improved on the training instability of GANs. GANs are hard to train because two networks fight each other, which can lead to one side becoming too strong, training that does not settle, and mode collapse.

### Why do we call `detach()` when training the Discriminator?

We call `detach()` so that we do not update the Generator while training the Discriminator. In each round, the two networks are trained one after the other. First the Discriminator learns to tell real from fake, and then the Generator is trained to fool the Discriminator.
