---
title: Linear Regression vs Logistic Regression
module: 1
module_title: Machine Learning Foundations
lesson: '1.3'
source: https://outcomeschool.com/blog/linear-regression-vs-logistic-regression
published: December 10, 2025
tags:
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 1188
reading_time: 6
status: full
---
# Linear Regression vs Logistic Regression

> **Module 1 · Lesson 1.3**  
> Source: [Outcome School](https://outcomeschool.com/blog/linear-regression-vs-logistic-regression) · Published: December 10, 2025 · Reading time: ~6 min · Tags: `ai`, `machine-learning`

---

![Linear Regression vs Logistic Regression](../../assets/images/01-01-03-linear-regression-vs-logistic-regression/linear-regression-vs-logistic-regression.png)

Linear Regression predicts a continuous value, like the price of a house, whereas Logistic Regression predicts a category, like whether an email is spam or not.

In this blog, we will learn about Linear Regression vs Logistic Regression in Machine Learning.

Let's get started.

In [machine learning](https://outcomeschool.com/blog/machine-learning), the two fundamental algorithms you will frequently encounter are **Linear Regression** and **Logistic Regression**. Although they sound similar, they are designed for **fundamentally different tasks**. Understanding their differences is crucial for choosing the right one. Let's explore what they are, how they work, and when to use them.

But before diving into the algorithms, it's important to understand the difference between **regression and classification**.

**Regression**

It predicts a **continuous value**.

A **continuous value** is numeric and can take any value. These values are measurable such as temperature, height, weight, or house prices.

Example: Predicting house prices, temperature, or stock prices.

**Classification**

It predicts a **categorical value**.

A **categorical value**, on the other hand, represents discrete groups or classes. These values are descriptive and usually non-numeric, like "yes/no," "red/blue/green," or "spam/not-spam." Categorical values are used in **classification problems**, where the aim is to assign inputs to a specific category or class.

Example: Predicting whether an email is spam or not, or whether a patient has a disease or not.

Once such a classifier is built, its quality is measured using Precision and Recall. We have a detailed blog on [Precision vs Recall](https://outcomeschool.com/blog/precision-vs-recall) that explains how both work.

Now it's time to jump into our main topic: Linear Regression vs Logistic Regression. Let's start with Linear Regression.

## Linear Regression

**Linear Regression** is one of the most basic algorithms in [supervised learning](https://outcomeschool.com/blog/supervised-vs-unsupervised-learning). It is used to predict a **continuous value** based on one or more input features.

Most importantly, it predicts a continuous value using a **linear** relationship between inputs and output.

Linear Regression uses a simple **linear** equation for the input variables `(x)` and the output variable `(y)`:

```python
y = w1 × x1 + w2 × x2
```

- `x1`, `x2` are input features.
- `w1`, `w2` are weights.
- `y` is the predicted continuous value.

The algorithm finds the line (or hyperplane in multiple dimensions) that best fits the data by minimizing the **Mean Squared Error (MSE)** between predicted and actual values.

![Linear Regression Graph](../../assets/images/01-01-03-linear-regression-vs-logistic-regression/linear-regression-graph.png)

Linear Regression fits a straight line to predict a continuous numeric value, with no limits on the output range, it can go below 0 or above 1.

And finally, as a prediction, we get a **continuous value**.

Example: Predicting house prices based on size and location.

This was all about the Linear Regression. Now it's time to learn Logistic Regression.

## Logistic Regression

**Logistic Regression**, despite its name, is used for **classification problems** in supervised learning, not regression. It predicts the **probability** that a given input belongs to a particular class.

It starts with the same linear combination of inputs:

```python
z = w1 × x1 + w2 × x2 // notice we’re using z instead of y
```

Then applies the **sigmoid (logistic) function**:

```python
y = σ(z) = 1 / (1 + e^(-z))
```

This converts the raw value `z` into a probability between **0** and **1**.

That probability is then converted into a class:

- If probability ≥ 0.5 → Class 1
- If probability < 0.5 → Class 0

The model is trained using [**Cross-Entropy**](https://outcomeschool.com/blog/math-behind-cross-entropy-loss) loss function. This loss function is mainly used for classification problems.

![Logistic Regression Graph](../../assets/images/01-01-03-linear-regression-vs-logistic-regression/logistic-regression-graph.png)

Logistic Regression uses an S-shaped curve (Sigmoid) to predict the probability, which is always restricted to the range [0, 1].

And finally, as a prediction, we get probabilities, that works well for classification.

You might be wondering: if the algorithm is used for classification, why is it called Logistic *Regression*, especially the "Regression" part of the name?

The name comes from the **way the model is built**, not the task it performs.

Logistic Regression actually starts by doing something that looks exactly like **linear regression**. It takes the input features and forms a linear combination:

```python
z = w1 × x1 + w2 × x2
```

This part is literally a **regression-style** calculation, nothing about classification yet.

Then comes the twist: instead of using `z` directly, the model passes it through the **logistic (sigmoid) function** to convert it into a probability between 0 and 1:

```python
y = σ(z) = 1 / (1 + e^(-z))
```

That probability is then used to decide the final class.

So even though the final outcome is **classification**, the model's internal mechanics are:

- Linear **regression-like** equation
- Followed by a **logistic** transformation using sigmoid function.
- Producing probabilities for classification

Because the core computation is regression-based, the name **"Logistic Regression"** remained, even though we use it for classification.

That's why the name is **Logistic Regression**.

So, this was all about the Logictic Regression.

## Differences Between Linear Regression and Logistic Regression

Let's summarize the differences in a tabular format.

| Linear Regression | Logistic Regression |
| --- | --- |
| Regression: Continuous value | Classification: Probability (0–1) → Class |
| y = w1 × x1 + w2 × x2 | z = w1 × x1 + w2 × x2 → y = sigmoid(z) |
| Loss Function: Mean Squared Error | Loss Function: Cross-Entropy |
| Examples: House price, temperature | Examples: Spam detection, disease prediction |
| Use it when the target is continuous | Use it when the target is categorical |

I hope this explanation helped.

You can find the complete code that contains the implementation of linear regression and logistic regression from scratch. Check [Build your own X - Machine Learning](https://github.com/amitshekhariitbhu/build-your-own-x-machine-learning)

## Frequently Asked Questions

### Is Logistic Regression used for regression or classification?

Logistic Regression is used for classification, not regression. It predicts the probability that an input belongs to a particular class. The name comes from the way the model is built, since it starts with a regression-style linear equation before applying the sigmoid function.

### What is the difference between regression and classification?

Regression predicts a continuous value, and classification predicts a categorical value. A continuous value is numeric and measurable, like temperature, height, or house prices. A categorical value represents discrete groups, like spam or not spam, so the aim is to assign each input to a class.

### Can Linear Regression predict values below 0 or above 1?

Yes. Linear Regression fits a straight line, so its output has no limits on range and can go below 0 or above 1. Logistic Regression is different. It passes the value through the sigmoid function, so the output is always a probability between 0 and 1.

### Which loss function does each model use?

Linear Regression uses Mean Squared Error, and Logistic Regression uses Cross-Entropy. Linear Regression finds the line that best fits the data by minimizing the Mean Squared Error between predicted and actual values. Cross-Entropy is mainly used for classification problems, which is why Logistic Regression is trained with it.

### How does Logistic Regression turn a probability into a class?

Logistic Regression uses a threshold of 0.5. If the probability is greater than or equal to 0.5, the input goes to Class 1. If the probability is less than 0.5, the input goes to Class 0.
