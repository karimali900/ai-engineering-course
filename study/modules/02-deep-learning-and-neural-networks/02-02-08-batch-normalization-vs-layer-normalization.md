---
title: Batch Normalization vs Layer Normalization
module: 2
module_title: Deep Learning and Neural Networks
lesson: '2.8'
source: https://outcomeschool.com/blog/batch-normalization-vs-layer-normalization
published: May 15, 2026
tags:
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 1520
reading_time: 8
status: full
---
# Batch Normalization vs Layer Normalization

> **Module 2 · Lesson 2.8**  
> Source: [Outcome School](https://outcomeschool.com/blog/batch-normalization-vs-layer-normalization) · Published: May 15, 2026 · Reading time: ~8 min · Tags: `llm`, `ai`, `machine-learning`

---

![Batch Normalization vs Layer Normalization](../../assets/images/02-02-08-batch-normalization-vs-layer-normalization/batch-normalization-vs-layer-normalization.png)

Batch Normalization normalizes each feature across all the examples in a batch, whereas Layer Normalization normalizes all the features within each single example.

In this blog, we are going to learn about Batch Normalization vs Layer Normalization. We will also see how Batch Normalization and Layer Normalization differ from each other and when to use which one.

We will cover the following:

- What is Normalization?
- Why do we need Normalization?
- What is Batch Normalization?
- What is Layer Normalization?
- Batch Normalization vs Layer Normalization
- When to use which one?

Let's get started.

## What is Normalization?

In simple words, **Normalization is the process of adjusting the values so that they are on a similar scale.**

Let's say we have two features: age (0 to 100) and salary (0 to 10,00,000). The values of salary are much larger than the values of age. This creates problems while training a [neural network](https://outcomeschool.com/blog/neural-network) because the network gives more importance to the feature with larger values.

So, here comes Normalization to the rescue. It brings all the values to a similar scale, typically with mean 0 and variance 1.

## Why do we need Normalization?

When we train a deep neural network, the values flowing through the layers can become very large or very small. This causes the following issues:

- Training becomes slow.
- The model becomes unstable.
- Gradients can explode or vanish.

So, we must normalize the values flowing through the network. This is where Batch Normalization and Layer Normalization come into the picture.

Now, let's learn about Batch Normalization first.

## What is Batch Normalization?

**Batch Normalization is a technique that normalizes the values across the batch dimension for each feature.**

In simple words, for each feature, it calculates the mean and variance across all the examples in the batch, and then normalizes the values using this mean and variance.

The best way to learn this is by taking an example.

Let's say we have a batch of 4 examples, and each example has 3 features as below:

```
Example 1: [10, 12, 14]
Example 2: [20, 22, 24]
Example 3: [30, 32, 34]
Example 4: [40, 42, 44]
```

Here, we have 4 rows (batch size = 4) and 3 columns (features = 3).

In Batch Normalization, we normalize column by column. Means, for the first feature, we take all 4 values from the first column [10, 20, 30, 40], calculate the mean and variance, and then normalize them.

- Mean of feature 1 = (10 + 20 + 30 + 40) / 4 = 25
- We do the same for feature 2 and feature 3.

So, Batch Normalization works across the batch. The mean and variance of each feature depend on the other examples present in the batch.

The formula is as below:

```
x_normalized = (x - mean) / sqrt(variance + epsilon)
```

Here, `epsilon` is a very small number added to avoid division by zero.

After normalization, we apply two learnable parameters `gamma` (scale) and `beta` (shift) as below:

```
output = gamma * x_normalized + beta
```

Here, `gamma` and `beta` allow the network to learn the best scale and shift for the normalized values.

**Note:** During training, we use the mean and variance of the current batch. During inference, we often process one example at a time, so we cannot calculate the batch mean and variance. So, we use the average of the mean and variance that we tracked across all the batches during training. This means, Batch Normalization behaves differently during training and inference.

**Advantages:**

- Faster training.
- Allows higher learning rates.
- Reduces the need for careful weight initialization.
- Acts as a regularizer.

**Disadvantages:**

- Does not work well with small batch sizes because the mean and variance of a very small batch are not reliable.
- Different behavior during training and inference, which can lead to inconsistent predictions.
- Not suitable for sequence models like [Recurrent Neural Networks (RNNs)](https://outcomeschool.com/blog/recurrent-neural-network) and [Transformers](https://outcomeschool.com/blog/decoding-transformer-architecture) because the sequence lengths vary from one example to another, and computing statistics across the batch becomes very difficult.

This was all about Batch Normalization. Now, it's time to learn about Layer Normalization.

## What is Layer Normalization?

**Layer Normalization is a technique that normalizes the values across the feature dimension for each example.**

In simple words, for each example, it calculates the mean and variance across all the features of that example, and then normalizes the values using this mean and variance.

Let's take the same example as before:

```
Example 1: [10, 12, 14]
Example 2: [20, 22, 24]
Example 3: [30, 32, 34]
Example 4: [40, 42, 44]
```

In Layer Normalization, we normalize row by row. Means, for Example 1, we take all 3 values from the first row [10, 12, 14], calculate the mean and variance, and then normalize them.

- Mean of Example 1 = (10 + 12 + 14) / 3 = 12
- We do the same for Example 2, Example 3, and Example 4 independently.

So, Layer Normalization works across the features for each example, independently of the batch. The mean and variance of each example do not depend on the other examples present in the batch.

The formula is the same as Batch Normalization:

```
x_normalized = (x - mean) / sqrt(variance + epsilon)
output = gamma * x_normalized + beta
```

Here, the only difference is the dimension over which we calculate the mean and variance.

**Note:** Layer Normalization behaves the same way during training and inference, because it does not depend on the batch at all.

**Advantages:**

- Works with any batch size, even a batch size of 1.
- Same behavior during training and inference.
- Works very well for sequence models like RNNs and Transformers.
- Used in popular models like BERT, GPT, and other Large Language Models.

**Disadvantages:**

- Not always the best choice for Convolutional Neural Networks (CNNs), where Batch Normalization usually performs better.

Now that we have learned about both Batch Normalization and Layer Normalization, it's time to compare them side by side.

## Batch Normalization vs Layer Normalization

For the sake of understanding, let's think of a classroom. Suppose we have 4 students and each student has scored marks in 3 subjects.

- **Batch Normalization** is like comparing the marks of a single subject across all 4 students. For example, we look at the Math marks of all 4 students together and normalize them.
- **Layer Normalization** is like comparing the marks of all 3 subjects for a single student. For example, we look at the Math, Science, and English marks of Student 1 together and normalize them.

This is the core difference between the two.

Let me tabulate the differences between Batch Normalization and Layer Normalization for your better understanding so that you can decide which one to use based on your use case.

| Aspect | Batch Normalization | Layer Normalization |
| --- | --- | --- |
| Direction of normalization | Across the batch (column-wise) | Across the features (row-wise) |
| Depends on batch size | Yes | No |
| Behavior in training and inference | Different | Same |
| Works with batch size of 1 | No | Yes |
| Best for | CNNs and image data | RNNs, Transformers, and LLMs |

In simple words:

- Batch Normalization normalizes one feature across all examples in the batch.
- Layer Normalization normalizes all features of one example.

## When to use which one?

The choice depends on our use case.

- If we are working with **image data** and **Convolutional Neural Networks (CNNs)** with large batch sizes, we must use Batch Normalization.
- If we are working with **sequence data**, **Recurrent Neural Networks (RNNs)**, **Transformers**, or **Large Language Models (LLMs)**, we must use Layer Normalization.
- If we have **very small batch sizes**, Layer Normalization is the better choice because it does not depend on the batch.

The reason Large Language Models like GPT and BERT use Layer Normalization is exactly this. The sequence lengths are different for different examples, and the batch sizes can be small. Layer Normalization handles both of these situations perfectly.

Now we must have understood Batch Normalization vs Layer Normalization.

## Frequently Asked Questions

### Why does Batch Normalization behave differently during inference?

During inference, we often process one example at a time, so we cannot calculate the batch mean and variance. Instead, we use the average of the mean and variance tracked across all the batches during training. This is why Batch Normalization behaves differently during training and inference, which can lead to inconsistent predictions.

### What are gamma and beta in normalization?

Gamma and beta are two learnable parameters applied after normalization. Gamma scales the normalized values and beta shifts them. They allow the network to learn the best scale and shift for the normalized values, and both Batch Normalization and Layer Normalization use them.

### Why do we add epsilon in the normalization formula?

We add epsilon to avoid division by zero. Epsilon is a very small number added to the variance before taking the square root. This keeps the formula safe even when the variance is zero.

### Does Batch Normalization work with small batch sizes?

No. Batch Normalization does not work well with small batch sizes, because the mean and variance of a very small batch are not reliable. It does not work with a batch size of 1 at all. Layer Normalization is the better choice here, since it does not depend on the batch.
