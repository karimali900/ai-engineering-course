---
title: What is Grouped Query Attention (GQA) and Why Do LLMs Use It?
module: 5
module_title: Modern LLM Architecture
lesson: '5.3'
source: https://outcomeschool.com/blog/grouped-query-attention
published: April 22, 2026
tags:
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 3560
reading_time: 18
status: full
---
# What is Grouped Query Attention (GQA) and Why Do LLMs Use It?

> **Module 5 · Lesson 5.3**  
> Source: [Outcome School](https://outcomeschool.com/blog/grouped-query-attention) · Published: April 22, 2026 · Reading time: ~18 min · Tags: `llm`, `ai`, `machine-learning`

---

![Grouped Query Attention](../../assets/images/05-05-03-what-is-grouped-query-attention-gqa-and-why-do-llms-use-it/grouped-query-attention.png)

Grouped-Query Attention (GQA) is a strategy where the attention heads are divided into groups, and all the heads within a group share the same Key and Value, while each head still has its own Query.

In this blog, we will learn about Grouped-Query Attention (GQA) and how it differs from Multi-Head Attention (MHA).

We will also learn about Multi-Query Attention (MQA) along the way and see when to use which one.

Grouped-Query Attention is one of the most important optimizations in modern Large Language Models. It allows models to generate text much faster while using less memory, and that too without losing much quality.

Before jumping into Grouped-Query Attention, we must know how [Multi-Head Attention](https://outcomeschool.com/blog/multi-head-attention-in-transformers) works. We have a detailed blog on [Transformer Architecture](https://outcomeschool.com/blog/decoding-transformer-architecture) where we have explained Multi-Head Attention as well. I will highly recommend reading it first.

Today, we will cover the following topics:

- The Big Picture
- Quick Recap: Multi-Head Attention (MHA)
- The Problem with Multi-Head Attention
- What is Multi-Query Attention (MQA)?
- What is Grouped-Query Attention (GQA)?
- How Grouped-Query Attention Works
- GQA is a Generalization of MHA and MQA
- GQA vs MHA vs MQA
- Real-World Use Cases
- A Note on Terminology
- Uptraining: Converting MHA to GQA
- Quick Summary

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

In Multi-Head Attention, every head keeps its own Key and Value. This is great for quality, but it makes the [KV Cache](https://outcomeschool.com/blog/kv-cache-in-llms) very large during inference. Grouped-Query Attention keeps the same set of Queries, but it makes groups of heads share one Key and one Value. This shrinks the KV Cache by a lot while keeping the quality very close to Multi-Head Attention. It is one of the main [KV Cache Compression](https://outcomeschool.com/blog/kv-cache-compression) techniques, the one that is built into the model design itself.

In simple words:

**Grouped-Query Attention = Near Multi-Head Attention quality + Much smaller KV Cache through head grouping.**

## Quick Recap: Multi-Head Attention (MHA)

In our blog on [Transformer Architecture](https://outcomeschool.com/blog/decoding-transformer-architecture), we have explained Multi-Head Attention in detail. Here is a quick recap.

In Multi-Head Attention, we run the attention mechanism multiple times in parallel. Each parallel run is called a **head**. Each head has its own separate set of weight matrices for **Query (Q)**, **Key (K)**, and **Value (V)**.

If we want to understand the math behind how Q, K, and V actually work in attention, we have a detailed blog on [Math Behind Attention: Q, K, V](https://outcomeschool.com/blog/math-behind-attention-qkv).

Let's say we have a model with 8 heads. This means:

- Head 1 has its own Q₁, K₁, V₁
- Head 2 has its own Q₂, K₂, V₂
- Head 3 has its own Q₃, K₃, V₃
- ... and so on for all 8 heads

Each head looks at the input from a different perspective. The outputs from all heads are concatenated and passed through a final projection to produce the result.

Think of it like a team of 8 detectives investigating a crime scene. Each detective has their own set of clues (K and V) and their own set of questions (Q). Each one investigates independently and finds different insights. When they share their findings, the team gets a complete picture.

This works great during training. But, here is the catch. There is a big problem during **inference** (i.e. when the model is actually generating text for the user). Let's understand this problem.

## The Problem with Multi-Head Attention

When a language model generates text, it produces one word at a time. For each new word, the model needs to look back at all the previous words using the attention mechanism.

**Note:** Technically, language models work with **tokens** (small pieces of text) instead of whole words. But just for the sake of understanding, we will use the word "word" throughout this blog.

Now, here is the important part. To compute attention, the model needs the **Key (K)** and **Value (V)** for every previous word. If the model recomputes K and V for all previous words every time it generates a new word, it would be very slow.

So, the model stores the Key and Value of all previous words in memory. This stored memory is called the [**KV Cache**](https://outcomeschool.com/blog/kv-cache-in-llms).

The best way to learn this is by taking an example.

Let's say we are generating a sentence and we have already produced 1,000 words. The model has 8 heads. Each head stores its own Key and Value for all 1,000 words.

So, the KV Cache stores:

- 8 sets of Keys (one per head) x 1,000 words = 8,000 Key vectors
- 8 sets of Values (one per head) x 1,000 words = 8,000 Value vectors
- Total: 16,000 vectors in memory

**Note:** This is per transformer layer. The full KV Cache multiplies this by the number of layers in the model. This is why long-context inference gets memory-hungry so fast.

Now, imagine a large model with 64 heads and a sequence length of 100,000 tokens. The KV Cache becomes extremely large. It takes up a huge amount of GPU memory.

Going back to our detective analogy, each detective (head) maintains their own personal notebook (KV Cache) where they write down clues about every word they have seen. With 64 detectives and 100,000 words, that is 64 separate notebooks, each with 100,000 pages. That is a lot of paper.

**This is the problem. The KV Cache in Multi-Head Attention grows very fast and takes up a lot of memory.** This makes inference slow and expensive, especially for long sequences and large models.

So, we need a smarter approach that reduces the size of this KV Cache without losing the quality of the model's output. First, let's understand Multi-Query Attention (MQA), which was the first attempt to solve this problem. Then we will learn about Grouped-Query Attention (GQA), which is a better solution.

## What is Multi-Query Attention (MQA)?

**Multi-Query Attention (MQA) is a strategy where all heads share the same Key and Value, but each head still has its own Query.**

Let's decompose the term:

**Multi-Query Attention = Multiple Queries + Single shared Key and Value**

In Multi-Head Attention, each head has its own Q, K, and V. In Multi-Query Attention, each head has its own Q, but all heads share **one single K** and **one single V**.

Let's say we have 8 heads:

**Multi-Head Attention (MHA):**

- Head 1: Q₁, K₁, V₁
- Head 2: Q₂, K₂, V₂
- Head 3: Q₃, K₃, V₃
- ... (8 separate K and V sets)

**Multi-Query Attention (MQA):**

- Head 1: Q₁, K\_shared, V\_shared
- Head 2: Q₂, K\_shared, V\_shared
- Head 3: Q₃, K\_shared, V\_shared
- ... (only 1 K and 1 V set for all heads)

Now, the KV Cache only needs to store 1 set of Keys and 1 set of Values instead of 8. The KV Cache becomes 8 times smaller.

Going back to our detective analogy, in MQA, all 8 detectives share a single notebook of clues. They still ask their own different questions (Q), but they are all looking at the same evidence. This saves a lot of paper (memory), but it limits their ability to find different insights.

**The problem with MQA:**

MQA reduces memory by a lot, but there is a trade-off. Since all heads share the same Key and Value, the model loses some of its ability to look at the input from different perspectives. The quality of the output can drop, and training can also become unstable.

We need something in between. Something that reduces memory like MQA but maintains quality like MHA.

So, here comes **Grouped-Query Attention** to the rescue.

## What is Grouped-Query Attention (GQA)?

**Grouped-Query Attention (GQA) is a strategy where heads are divided into groups, and all heads within a group share the same Key and Value, while each head still has its own Query.**

Let's decompose the term:

**Grouped-Query Attention = Grouped Queries + Shared Key and Value per group**

In simple words, instead of giving every head its own K and V (like MHA) or giving all heads a single shared K and V (like MQA), GQA divides the heads into groups and lets each group share one K and V.

The best way to learn this is by taking an example.

Let's say we have 8 heads and we divide them into 2 groups (4 heads per group):

**Group 1:** Head 1, Head 2, Head 3, Head 4 - share K\_group1, V\_group1

**Group 2:** Head 5, Head 6, Head 7, Head 8 - share K\_group2, V\_group2

So:

- Head 1: Q₁, K\_group1, V\_group1
- Head 2: Q₂, K\_group1, V\_group1
- Head 3: Q₃, K\_group1, V\_group1
- Head 4: Q₄, K\_group1, V\_group1
- Head 5: Q₅, K\_group2, V\_group2
- Head 6: Q₆, K\_group2, V\_group2
- Head 7: Q₇, K\_group2, V\_group2
- Head 8: Q₈, K\_group2, V\_group2

Now, instead of storing 8 sets of K and V (like MHA), we only store 2 sets. The KV Cache becomes 4 times smaller.

And instead of using just 1 shared K and V (like MQA), we use 2 sets. So, the model still has some ability to look at the input from different perspectives.

Going back to our detective analogy, in GQA, we divide the 8 detectives into 2 teams. Each team of 4 detectives shares one notebook of clues. This way, we need only 2 notebooks instead of 8 (much less paper), but we still have 2 different sets of clues (better than 1). Each team can discover different things.

GQA is the sweet spot between MHA and MQA. It gives us the memory savings close to MQA while keeping the quality close to MHA.

**Note:** In GQA, only the Key and Value are shared within a group. The Query is still separate for every head. This is important because the Query is what allows each head to look at the input from a different perspective. By keeping the Queries separate, GQA preserves the diversity of attention patterns. The KV Cache shrinks because we only store the Key and Value during inference, not the Query.

Now, let's understand how GQA actually works step by step.

## How Grouped-Query Attention Works

Let's walk through the process step by step.

**Step 1:** Divide the heads into groups. The number of groups is a setting that we choose before training. Let's say we have 8 heads and 2 groups.

**Step 2:** Each head computes its own Query (Q) using its own weight matrix. So, all 8 heads have their own separate Queries. This is the same as MHA.

**Step 3:** Each group computes one shared Key (K) and one shared Value (V) using the group's weight matrices. Group 1 computes K\_group1 and V\_group1. Group 2 computes K\_group2 and V\_group2.

**Step 4:** Each head runs the attention mechanism using its own Query but with the shared Key and Value of its group. Heads 1 to 4 use K\_group1 and V\_group1. Heads 5 to 8 use K\_group2 and V\_group2.

**Step 5:** The outputs from all heads are concatenated and passed through the final projection, just like in MHA.

The result is the same type of output as MHA. But the KV Cache is much smaller because we only store K and V for each group, not for each head.

This is how Grouped-Query Attention works.

Now, let's see something very interesting about GQA.

## GQA is a Generalization of MHA and MQA

Here is something beautiful about GQA. It is actually a generalization of both MHA and MQA. Let's understand how.

- **When the number of groups = number of heads:** Each group has exactly 1 head. Each head gets its own K and V. This is exactly **Multi-Head Attention (MHA)**.
- **When the number of groups = 1:** All heads are in one group. All heads share the same K and V. This is exactly **Multi-Query Attention (MQA)**.
- **When the number of groups is between 1 and number of heads:** This is **Grouped-Query Attention (GQA)**.

So, MHA and MQA are just special cases of GQA. By changing the number of groups, we can control the trade-off between quality and memory. That's the beauty of Grouped-Query Attention.

Now that we have learned about all three, let's compare them.

## GQA vs MHA vs MQA

Before we compare the numbers, let's first see the three architectures visually side by side.

```
MHA (8 query heads, 8 KV sets - one per head):
  [Q1]  [Q2]  [Q3]  [Q4]  [Q5]  [Q6]  [Q7]  [Q8]
   |     |     |     |     |     |     |     |
   v     v     v     v     v     v     v     v
  [K1]  [K2]  [K3]  [K4]  [K5]  [K6]  [K7]  [K8]
  [V1]  [V2]  [V3]  [V4]  [V5]  [V6]  [V7]  [V8]
MQA (8 query heads, 1 KV set - shared by all heads):
  [Q1]  [Q2]  [Q3]  [Q4]  [Q5]  [Q6]  [Q7]  [Q8]
    \     \    \    |     |    /    /     /
     +-----+----+---+-----+---+----+-----+
                       |
                       v
                  [K_shared]
                  [V_shared]
GQA (8 query heads, 2 groups - 1 KV set per group):
  [Q1] [Q2] [Q3] [Q4]       [Q5] [Q6] [Q7] [Q8]
    \   |    |   /             \   |    |   /
     +--+----+--+                +-+----+-+
            |                          |
            v                          v
       [K_group1]                 [K_group2]
       [V_group1]                 [V_group2]
```

Here, we can see the difference clearly:

- In **MHA**, each Query has its own private Key and Value. 8 Queries, 8 KV sets. Maximum quality, maximum memory.
- In **MQA**, all Queries point to a single shared Key and Value. 8 Queries, 1 KV set. Minimum memory, but reduced diversity.
- In **GQA**, Queries are divided into groups, and each group shares one Key and Value. 8 Queries, 2 KV sets. A balance of both worlds.

Now, let me tabulate the differences between GQA, MHA, and MQA for your better understanding so that you can decide which one to use based on your use case.

| Feature | MHA | MQA | GQA |
| --- | --- | --- | --- |
| Key-Value sets | One per head | One for all heads | One per group |
| KV Cache size | Largest | Smallest | In between |
| Output quality | Best | Can degrade | Close to MHA |
| Memory usage during inference | Highest | Lowest | In between |
| Inference speed | Slowest | Fastest | Fast |
| Example (8 heads, 2 groups) | 8 KV sets | 1 KV set | 2 KV sets |

**In simple words:** MHA gives the best quality but uses the most memory. MQA uses the least memory but can lose quality. GQA is the sweet spot - it uses much less memory than MHA while keeping quality very close to MHA.

Now, let's see some real-world use cases.

## Real-World Use Cases

GQA is now used in many popular large language models:

- **LLaMA 2 (34B and 70B):** Uses GQA with 8 KV groups. The 70B model has 64 query heads, so the KV Cache is 8 times smaller compared to standard MHA. (Meta described the 34B in the paper but never publicly released its weights.) The smaller LLaMA 2 models (7B and 13B) still use standard MHA.
- **LLaMA 3:** Uses GQA across all model sizes for faster inference.
- **Mistral 7B:** Uses GQA with 32 query heads and 8 KV groups. It also pairs GQA with [Sliding Window Attention](https://outcomeschool.com/blog/how-does-sliding-window-attention-work) so that long inputs stay cheap.

These models use GQA because it allows them to handle longer sequences and serve more users at the same time, and that too while keeping the quality of the output very high.

Serving many users on one GPU also means managing the KV Cache memory carefully at serving time, and we have a detailed blog on [vLLM](https://outcomeschool.com/blog/how-does-vllm-work) that explains how a serving system handles this.

GQA is especially useful for:

- **Long conversations:** When the model needs to remember thousands of previous words, GQA keeps the KV Cache manageable.
- **Serving many users:** Smaller KV Cache means more users can be served on the same GPU.
- **[Edge deployment](https://outcomeschool.com/blog/cloud-vs-on-device-model-deployment):** Reduced memory makes it easier to run models on devices with limited resources.

GQA has become [a standard technique in modern LLMs](https://outcomeschool.com/blog/evolution-of-llm-architecture). It enables us to have faster inference and lower memory usage without meaningfully sacrificing quality. It makes our life easy.

## A Note on Terminology

In the actual code of popular models (like the configurations in HuggingFace or LLaMA), the number of groups is called `num_key_value_heads`. The number of query heads is called `num_attention_heads`.

So, the number of heads per group is simply:

**Heads per group = `num_attention_heads` / `num_key_value_heads`**

Let's say we read about a model that has 32 query heads and 8 KV heads. This means there are 8 groups, and each group has 4 heads sharing the same Key and Value.

This terminology is good to know because when we read the configuration of a real model, we will see `num_key_value_heads` directly instead of the word "groups".

## Uptraining: Converting MHA to GQA

Now, the next big question is: do we always need to train a GQA model from scratch? The answer is no.

The original GQA paper showed that we can take an existing Multi-Head Attention model and convert it into a GQA model very cheaply. This is called **uptraining**.

The process is simple:

**Step 1:** Take an existing MHA model that has already been trained.

**Step 2:** For each group, take all the Key weight matrices of the heads in that group and average them. Do the same for the Value weight matrices. This gives us one shared Key and one shared Value per group.

**Step 3:** [Fine-tune](https://outcomeschool.com/blog/how-does-fine-tuning-work) the model for a short time. The original paper showed that uptraining with just around 5% of the original pre-training compute is enough to recover quality close to full MHA.

This is one of the main reasons GQA was adopted so quickly. Labs did not have to throw away their existing MHA models or spend huge compute to train new ones. They could just uptrain them into GQA.

Now, we have understood Grouped-Query Attention and how it differs from Multi-Head Attention. We also learned about Multi-Query Attention, how GQA is a generalization of both MHA and MQA, the terminology used in real code, and how existing MHA models can be uptrained into GQA.

## Quick Summary

Let's recap what we have learned:

- **Multi-Head Attention (MHA):** Every head has its own Query, Key, and Value. Best quality, but the KV Cache becomes very large during inference.
- **The KV Cache problem:** During text generation, the model stores the Key and Value of every previous word for every head. With many heads and long sequences, this takes a huge amount of GPU memory.
- **Multi-Query Attention (MQA):** All heads share one single Key and one single Value, while each head still has its own Query. The KV Cache becomes very small, but the output quality can drop.
- **Grouped-Query Attention (GQA):** Heads are divided into groups. Each group shares one Key and one Value, while each head still has its own Query. This is the sweet spot between MHA and MQA.
- **GQA is a generalization:** When the number of groups equals the number of heads, GQA becomes MHA. When the number of groups is 1, GQA becomes MQA. Anything in between is GQA.
- **Importance:** GQA gives us memory savings close to MQA while keeping quality close to MHA. It is now used in many popular models like LLaMA 2, LLaMA 3, and Mistral 7B.
- **Uptraining:** We do not need to train a GQA model from scratch. We can take an existing MHA model, average the K and V weights within each group, and fine-tune for a short time to convert it into a GQA model. This is one of the main reasons GQA was adopted so quickly.

## Frequently Asked Questions

### Why does GQA share the Key and Value but not the Query?

The Query is what allows each head to look at the input from a different perspective, so keeping it separate preserves the diversity of attention patterns. Also, the KV Cache only stores the Key and Value during inference, not the Query. So, sharing only the Key and Value is what shrinks the KV Cache.

### Does Grouped-Query Attention reduce model quality?

Only slightly. GQA keeps the output quality very close to Multi-Head Attention while using much less memory. Multi-Query Attention, which shares a single Key and Value across all heads, can lose more quality and can even make training unstable. GQA sits in between, which is why it is called the sweet spot.

### Is GQA mainly useful during training or during inference?

GQA is mainly useful during inference. Multi-Head Attention works great during training, but when the model generates text one word at a time, it stores the Key and Value of every previous word in the KV Cache. GQA shrinks this KV Cache, which helps with long conversations, serving many users on the same GPU, and edge deployment.

### How do we find the number of GQA groups in a model's configuration?

The number of groups is called `num_key_value_heads`, and the number of query heads is called `num_attention_heads`. Heads per group is `num_attention_heads` divided by `num_key_value_heads`. For example, a model with 32 query heads and 8 KV heads has 8 groups, and each group has 4 heads sharing the same Key and Value.

### Do all LLaMA 2 models use Grouped-Query Attention?

No. In LLaMA 2, the 34B and 70B models use GQA with 8 KV groups, while the smaller 7B and 13B models still use standard Multi-Head Attention. LLaMA 3 uses GQA across all model sizes, and Mistral 7B also uses GQA.
