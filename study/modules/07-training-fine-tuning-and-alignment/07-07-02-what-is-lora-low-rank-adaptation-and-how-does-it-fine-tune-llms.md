---
title: What is LoRA (Low-Rank Adaptation) and How Does It Fine-Tune LLMs?
module: 7
module_title: Training, Fine-Tuning, and Alignment
lesson: '7.2'
source: https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms
published: April 24, 2026
tags:
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 2529
reading_time: 13
status: full
---
# What is LoRA (Low-Rank Adaptation) and How Does It Fine-Tune LLMs?

> **Module 7 · Lesson 7.2**  
> Source: [Outcome School](https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms) · Published: April 24, 2026 · Reading time: ~13 min · Tags: `llm`, `ai`, `machine-learning`

---

![LoRA: Low-Rank Adaptation of LLMs](../../assets/images/07-07-02-what-is-lora-low-rank-adaptation-and-how-does-it-fine-tune-llms/lora-low-rank-adaptation-of-llms.png)

LoRA (Low-Rank Adaptation) is a way to fine-tune a large model without updating all of its weights. It keeps the original weights frozen and learns a tiny pair of extra matrices on the side.

In this blog, we will learn about LoRA - Low-Rank Adaptation of Large Language Models.

Today, we will cover the following topics:

- The Big Picture
- Why Full Fine-Tuning Is Expensive
- The Core Idea Behind LoRA
- How LoRA Works Step by Step
- A Small Numeric Example
- Where LoRA Is Applied in a Transformer
- Merging LoRA Back Into the Model
- Real-World Use Cases
- Quick Summary

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

LoRA is a way to [fine-tune](https://outcomeschool.com/blog/how-does-fine-tuning-work) a large model **without updating all of its weights**. Instead of changing the original weight matrix, we keep it frozen and learn a tiny pair of extra matrices on the side. These tiny matrices capture the "adjustment" we want.

In simple words:

**LoRA = Frozen original weights + A small low-rank update learned on the side.**

This makes fine-tuning much cheaper, faster, and lighter on storage. And, we still get strong task-specific performance.

## Why Full Fine-Tuning Is Expensive

Before jumping into LoRA, we must first understand why full fine-tuning is hard.

We can learn everything about fine-tuning in this [video](https://www.youtube.com/watch?v=lnfWvX66FUk).

A modern Large Language Model can have billions of parameters. For example, a 7 billion parameter model has 7 billion numbers inside it. When we do full fine-tuning, we update **every single one** of these numbers.

This causes the following issues:

- **GPU memory explodes.** We need to keep the weights, the gradients, and the optimizer states in memory. For Adam, this can be 3 to 4 times the size of the model itself.
- **Training is slow.** Updating billions of parameters takes a lot of compute.
- **Storage is heavy.** Each fine-tuned copy of the model is the same size as the original. If we have 10 different tasks, we need 10 full copies of a multi-gigabyte model.
- **Sharing is hard.** A multi-gigabyte checkpoint per task is not easy to ship to users.

We need a smarter way. We need a way to adapt the model to a new task **without touching most of its weights**.

So, here comes **LoRA** to the rescue.

## The Core Idea Behind LoRA

The full form of LoRA is **Low-Rank Adaptation**.

Let's decompose the name:

**LoRA = Low-Rank + Adaptation.**

- **Adaptation** means we are adapting the model to a new task or a new style.
- **Low-Rank** means the change we apply to the weights is represented in a very compact form using two small matrices.

The idea is based on a powerful observation from the original LoRA paper from Microsoft:

> When we fine-tune a large model, the actual update that we apply to the weights is very low-rank. We do not need a full giant update matrix - a much smaller one is enough.

In simple words, the "adjustment" needed to teach the model a new task is much smaller than the model itself. So, we do not need a giant matrix to represent it.

Why does this work? The pre-trained model already knows a lot. It has learned grammar, facts, reasoning, and general patterns. Fine-tuning it for a new task is not a rewrite. It is just a small nudge along a few important directions. That is exactly what "low-rank" means.

Let's take a real-world analogy. Think of the pre-trained model as a giant textbook. Full fine-tuning is like rewriting every page of the textbook for a new topic. LoRA is like keeping the textbook unchanged and adding a small set of sticky notes on top that carry the new knowledge. The textbook stays the same, and the small notes do the actual adjustment.

Now, let's see how this works in math.

A weight matrix `W` inside the model has shape `d x d`. In full fine-tuning, we learn a new matrix `W_new` of the same shape:

```
W_new = W + ΔW
```

Here, `ΔW` is the change we want to apply. Both `W` and `ΔW` are huge.

LoRA replaces this huge `ΔW` with a product of **two small matrices**:

```
ΔW = BA
```

Where:

- `A` has shape `r x d`
- `B` has shape `d x r`
- `r` is the **rank**, a small number like 4, 8, 16, 32, or 64
- `d` is the original dimension, often 4096 or larger

Now, `BA` still has shape `d x d`, but we never store the full `d x d` update. We only store `A` and `B`, which are tiny compared to `W`.

**Note:** For simplicity, we are assuming `W` is a square `d x d` matrix. In real Large Language Models, attention projection matrices are square, but feed-forward layers are not. They are usually `d x 4d` or `4d x d`. LoRA works for any rectangular matrix - if `W` has shape `d x k`, then `B` becomes `d x r` and `A` becomes `r x k`. The idea stays exactly the same.

Here is a simple ASCII diagram comparing the sizes.

```
       ΔW (full update)                 B            x            A
        (d x d matrix)              (d x r)                   (r x d)
     +-------------------+             +--+              +-------------------+
     |                   |             |  |              +-------------------+
     |                   |             |  |
     |                   |             |  |
     |                   |     =       |  |      x
     |                   |             |  |
     |                   |             |  |
     |                   |             |  |
     |                   |             |  |
     +-------------------+             +--+
```

Here, the big square is the full update we would have to store. The thin column `B` and the short row `A` together carry all the information we actually train. The visual size difference is exactly why LoRA is so memory-efficient.

The forward pass for an input vector `x` becomes:

```
h = Wx + (BA)x
```

Here, `W` is **frozen**. Only `A` and `B` are trained.

## How LoRA Works Step by Step

Let's walk through LoRA step by step.

**Step 1:** Take the pre-trained model and freeze all of its original weights. Nothing inside the original model will be updated during training.

**Step 2:** For each weight matrix we want to adapt, add two small matrices `A` and `B` next to it.

- `A` is initialized with small random values (Gaussian).
- `B` is initialized with **all zeros**.

This zero initialization is important. At the start of training, `BA = 0`, so the model behaves exactly like the original pre-trained model. Training then gradually nudges `BA` away from zero.

**Step 3:** During training, only `A` and `B` receive gradient updates. The original `W` stays untouched.

**Step 4:** During the forward pass, compute the output as:

```
h = Wx + (alpha / r) * (BA)x
```

Here, `alpha` is a scaling factor. The ratio `alpha / r` controls how strongly the LoRA update influences the output. A common choice is `alpha = 2 * r`.

**Step 5:** After training, we have a tiny set of new weights `A` and `B` that capture the task-specific knowledge. The original model is still untouched.

That's the entire idea.

Going back to our textbook analogy, the original textbook is the frozen `W`. The sticky notes are `A` and `B`. The notes start blank because `B` is zero. As training goes on, the notes fill up with corrections that nudge the textbook's behavior toward the new task.

**Note:** The choice of rank `r` is the most important LoRA hyperparameter. A smaller `r` means fewer trainable parameters and faster training, but the adapter has less capacity to learn complex changes. A larger `r` gives more capacity but loses some of the efficiency benefits. In practice, ranks of 8 to 64 work well for most tasks.

## A Small Numeric Example

Let's put this into perspective with real numbers.

Suppose we have a weight matrix `W` of shape `4096 x 4096`. The number of parameters in `W` is:

```
4096 x 4096 = 16,777,216
```

That's around 16.8 million parameters in **just one matrix**. A full fine-tune would update all of them.

Now, let's apply LoRA with rank `r = 8`.

- `A` has shape `8 x 4096` = 32,768 parameters
- `B` has shape `4096 x 8` = 32,768 parameters
- Total LoRA parameters = 65,536

Let's compare:

- Full fine-tune: 16,777,216 parameters per matrix
- LoRA with r=8: 65,536 parameters per matrix

That is roughly **256x fewer parameters** for the same matrix. And, this is just for one matrix - the savings multiply across every layer of the model.

For a full 7B parameter model, full fine-tuning updates 7 billion parameters. LoRA with rank 8 typically updates only a few million. The trainable parameter count drops by **a factor of around 1000x or more**, depending on the rank and where LoRA is applied.

## Where LoRA Is Applied in a Transformer

LoRA can be applied to any linear layer in the model. But, in practice, LoRA is most commonly applied to the **attention projection matrices**.

We have a detailed blog on [Transformer Architecture](https://outcomeschool.com/blog/decoding-transformer-architecture) that explains how attention layers work inside a transformer.

Inside each attention block, we have four projection matrices:

- `W_Q` - the Query projection
- `W_K` - the Key projection
- `W_V` - the Value projection
- `W_O` - the Output projection

If we want to go deeper into how Q, K, and V are computed and used, we can read [Math Behind Attention: Q, K, V](https://outcomeschool.com/blog/math-behind-attention-qkv).

The original LoRA paper found that adapting just `W_Q` and `W_V` is often enough to get strong task performance with minimal extra parameters. In practice, we can also apply LoRA to all four projections, or even to the feed-forward layers, for better quality at the cost of more trainable parameters.

Here is a simple ASCII diagram showing the structure for a single weight matrix.

```
              Input x
                |
        +-------+-------+
        |               |
        v               v
   +---------+      +-------+
   |  W      |      |   A   |   (trainable, r x d)
   | (frozen)|      +-------+
   +---------+          |
        |               v
        |          +---------+
        |          |    B    |   (trainable, d x r)
        |          +---------+
        |               |
        v               v
        +-------+-------+
                |
                v
        h = Wx + (BA)x
```

Here, `W` stays frozen and only `A` and `B` are trained. The two paths are added together to form the final output.

## Merging LoRA Back Into the Model

Here is one of the most beautiful properties of LoRA.

Once training is done, we can **merge** `BA` directly into `W`:

```
W_merged = W + (alpha / r) * (BA)
```

Now, the model uses a single weight matrix `W_merged` exactly like the original. There are no extra matrices and no extra computation at inference time.

This means LoRA adds **zero inference latency** when merged. We get the benefits of fine-tuning without any runtime overhead.

In our textbook analogy, merging is like permanently writing the sticky notes into the textbook itself. The notes are gone, but the textbook now carries the new knowledge.

We can also keep `A` and `B` separate from `W` if we want to swap between different tasks at runtime. This is the basis of **adapter swapping**.

**Note:** Merging is a one-way operation. Once we merge `A` and `B` into `W`, we cannot easily swap that adapter out for a different one. So, if we want to serve many tasks from the same base model, we should keep the adapters unmerged and load them on demand.

This ability to merge is also what sets LoRA apart from the other Parameter-Efficient Fine-Tuning methods. We have a detailed blog on [How does Prefix Tuning work?](https://outcomeschool.com/blog/how-does-prefix-tuning-work) that explains a method where nothing gets merged, and a small learned prefix steers every attention layer of the frozen model instead.

## Real-World Use Cases

LoRA is everywhere in modern LLM workflows. Let's see where LoRA is used in practice.

- **Fine-tuning open-source LLMs on a single GPU.** Models like LLaMA, Mistral, and Qwen are commonly fine-tuned using LoRA on a single consumer or workstation GPU. Without LoRA, this would need a cluster of expensive GPUs.
- **Task-specific adapters.** Teams train small LoRA adapters for each task - one for summarization, one for code generation, one for customer support - and load only the adapter they need. The base model stays the same.
- **Style and domain adaptation.** LoRA is used to teach a base model a specific writing style, a domain like medical or legal, or a specific persona.
- **Image generation models.** LoRA is widely used in image models like [Stable Diffusion](https://outcomeschool.com/blog/diffusion-models) to add new characters, styles, or concepts without retraining the whole model. The community shares thousands of small LoRA files.
- **Foundation for QLoRA.** LoRA is the building block for QLoRA, which combines LoRA with [4-bit quantization](https://outcomeschool.com/blog/how-does-model-quantization-work) to fine-tune very large models on a single consumer GPU.

Because LoRA freezes the base model and trains only a small adapter, it is also a popular way to do [Continual Learning in LLMs](https://outcomeschool.com/blog/continual-learning-in-llms) - we can teach the model new tasks without overwriting the knowledge it already has.

**Note:** When we ship LoRA adapters to users, we only ship the small `A` and `B` matrices. These are often just a few megabytes. Compare that to a multi-gigabyte full fine-tuned model. This is why LoRA adapters are so easy to share, swap, and version.

## Quick Summary

Let's recap what we have decoded:

- **LoRA = Low-Rank Adaptation.** We freeze the original weights and learn a small low-rank update on the side.
- **The update is `ΔW = BA`** where `A` and `B` are tiny matrices controlled by a small rank `r`.
- **`A` is random, `B` is zero at the start.** This makes the model start exactly like the original pre-trained model.
- **Only `A` and `B` are trained.** The original `W` stays frozen, which saves massive amounts of memory and compute.
- **Trainable parameters drop by 100x to 1000x or more** depending on the rank and where LoRA is applied.
- **LoRA can be merged into the original weights** after training, so there is zero extra latency at inference time.
- **Adapter swapping** lets us serve many tasks from a single base model by loading different `A` and `B` matrices.
- **LoRA is used everywhere** - LLMs, image models, domain adaptation, and as the foundation for QLoRA.

This is how LoRA makes fine-tuning of Large Language Models cheap, fast, and accessible.

## Frequently Asked Questions

### Does LoRA slow down inference?

No. Once training is done, we can merge `BA` directly into the original weight matrix. The model then uses a single weight matrix exactly like the original, with no extra matrices and no extra computation. So, LoRA adds zero inference latency when merged.

### What rank should we choose for LoRA?

In practice, ranks of 8 to 64 work well for most tasks. A smaller rank means fewer trainable parameters and faster training, but less capacity to learn complex changes. A larger rank gives more capacity but loses some of the efficiency benefits. The rank is the most important LoRA hyperparameter.

### Why is the matrix B initialized with zeros?

Because at the start of training, `BA` becomes zero. This makes the model behave exactly like the original pre-trained model. Training then gradually nudges `BA` away from zero, while `A` starts with small random values.

### Can one base model serve many tasks with LoRA?

Yes. Teams train small LoRA adapters for each task and load only the adapter they need, while the base model stays the same. To do this, we should keep the adapters unmerged, because merging is a one-way operation and a merged adapter cannot easily be swapped out.

### What is the relation between LoRA and QLoRA?

LoRA is the building block for QLoRA. QLoRA combines LoRA with 4-bit quantization to fine-tune very large models on a single consumer GPU.
