---
title: How Does Backpropagation Work? The Math Explained Step by Step
module: 2
module_title: Deep Learning and Neural Networks
lesson: '2.5'
source: https://outcomeschool.com/blog/math-behind-backpropagation
published: April 6, 2026
tags:
- math
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 2794
reading_time: 14
status: full
---
# How Does Backpropagation Work? The Math Explained Step by Step

> **Module 2 · Lesson 2.5**  
> Source: [Outcome School](https://outcomeschool.com/blog/math-behind-backpropagation) · Published: April 6, 2026 · Reading time: ~14 min · Tags: `math`, `llm`, `ai`, `machine-learning`

---

![Math Behind Backpropagation](../../assets/images/02-02-05-how-does-backpropagation-work-the-math-explained-step-by-step/math-behind-backpropagation.png)

Backpropagation is a method used to calculate how much each weight in a neural network contributed to the error, so that we can adjust those weights to reduce the error. It does this by sending the error backward through the network, using the chain rule.

In this blog, we will learn about the math behind backpropagation in neural networks.

Backpropagation is the core algorithm that allows neural networks to learn from their mistakes. Without it, training neural networks efficiently would not be possible. Understanding the math behind it gives us a deeper understanding of how neural networks actually learn. Do not worry, we will learn about each concept step by step so that everything is clear.

We will cover the following topics:

- What is backpropagation?
- The chain rule of calculus
- Forward pass
- Loss calculation
- Backward pass (backpropagation)
- Step-by-step numeric example
- Weight update using gradient descent
- Backpropagation in Python

Let's get started.

## What is Backpropagation?

**Backpropagation is a method used to calculate how much each weight in a [neural network](https://outcomeschool.com/blog/neural-network) contributed to the error, so that we can adjust those weights to reduce the error.**

In simple words, **Backpropagation = Backward + Propagation**. It means propagating (sending) the error backward through the network. Here, **weights** are the numbers that the network adjusts during training to make better predictions.

Let's say a student takes a math test and gets a wrong answer. The teacher does not just say "wrong" - the teacher goes back through each step to find exactly where the student made the mistake. That is what backpropagation does. It goes backward through each layer of the network to find how much each weight contributed to the error.

## The Chain Rule of Calculus

Before we dive into backpropagation, we must understand the chain rule. Do not worry, we will keep it simple.

The chain rule is a formula from calculus that tells us how to find the rate of change of a value that depends on another value, which in turn depends on yet another value.

Let's say we have a chain of dependencies: the number of hours we study affects our knowledge, and our knowledge affects our exam score. If we want to know how study hours affect the exam score, we need to trace through the chain.

In mathematical terms, let's say we have three variables: x, y, and z.

- y depends on x: y = f(x)
- z depends on y: z = g(y)

Now, if we want to know how z changes when x changes, we use the chain rule as below:

```
dz/dx = (dz/dy) * (dy/dx)
```

Here, `dz/dx` means "how much does z change when x changes by a tiny amount?"

This is very important because in a neural network, the output depends on the activations of each layer, and each layer's activation depends on its own weights and the activations from the previous layer. The chain rule allows us to trace the error all the way back to each weight.

## Forward Pass

In the forward pass, the input data flows through the network from the input layer to the output layer. At each neuron, we perform two operations:

**Step 1: Weighted Sum**

We multiply each input by its weight and add a bias. For a neuron with two inputs, this looks like below:

```
z = (w1 * x1) + (w2 * x2) + b
```

Here, `w1` and `w2` are weights, `x1` and `x2` are inputs, and `b` is the bias. The bias is an extra value that helps the neuron adjust its output even when the inputs are zero. If a neuron has only one input, the formula simplifies to `z = w * x + b`.

**Step 2: Activation Function**

We pass the weighted sum through an activation function. Let's use the sigmoid function for our example as below:

```
a = sigmoid(z) = 1 / (1 + e^(-z))
```

Here, `e` is Euler's number (approximately `2.71828`). The sigmoid function always outputs a value between 0 and 1, which makes it useful for representing probabilities and keeping values in a manageable range.

The activation function introduces non-linearity, which allows the network to learn complex patterns (i.e. curves and non-linear relationships). Without it, no matter how many layers we stack, the network would only be able to learn simple straight-line relationships.

The output of one layer becomes the input to the next layer. This continues until we get the final output.

## Loss Calculation

After the forward pass, we compare the predicted output with the actual expected output. The difference between them is called the **loss** (or error).

A common loss function is the **Squared Error Loss**:

```
Loss = (1/2) * (y_actual - y_predicted)^2
```

Here, we use `(1/2)` as a constant to make the math cleaner when we calculate the derivative (i.e. the rate of change). This only changes the scale of the gradients, not their direction, and the learning rate compensates for this. When we have multiple training examples, we average this loss over all examples, and that is called the **Mean Squared Error (MSE)**. For our example, we have a single training example, so we will use this simpler form.

The goal of training is to minimize this loss. And to minimize it, we need to know how each weight affects the loss. This is exactly where backpropagation comes into the picture.

## Backward Pass (Backpropagation)

Now, we need to find out: "How much does each weight contribute to the loss?" In mathematical terms, we need to calculate the **gradient** of the loss with respect to each weight.

In simple words, the gradient is like a slope. Suppose we are standing on a hill and we want to reach the lowest point. The gradient tells us which direction to walk (uphill or downhill) and how steep the slope is.

The gradient tells us: The **direction** in which we need to change the weight (increase or decrease).

We use the chain rule to calculate these gradients, going backward from the output layer to the input layer.

### Setting Up a Simple Network

Let's take a very simple neural network with:

- 1 input neuron (x)
- 1 hidden neuron
- 1 output neuron
- Sigmoid activation function at the hidden and output neurons

The network looks like below:

```
Input (x) --[w1]--> Hidden (h) --[w2]--> Output (o)
```

**Forward pass equations:**

```
z_h = w1 * x + b1        (weighted sum at hidden neuron)
a_h = sigmoid(z_h)        (activation at hidden neuron)
z_o = w2 * a_h + b2       (weighted sum at output neuron)
a_o = sigmoid(z_o)         (activation at output neuron, this is our prediction)
```

**Loss:**

```
L = (1/2) * (y - a_o)^2
```

Here, `y` is the actual expected output and `a_o` is our predicted output.

### Calculating Gradients

Now, we want to find `dL/dw2` (how much the loss changes when w2 changes) and `dL/dw1` (how much the loss changes when w1 changes).

**Gradient for w2:**

Using the chain rule:

```
dL/dw2 = (dL/da_o) * (da_o/dz_o) * (dz_o/dw2)
```

Let's calculate each part:

```
dL/da_o = -(y - a_o)
```

This tells us how the loss changes with respect to the predicted output.

```
da_o/dz_o = a_o * (1 - a_o)
```

This is the derivative (i.e. the rate of change) of the sigmoid function. Let's see how we get this result.

We know that `a_o = sigmoid(z_o) = 1 / (1 + e^(-z_o))`. We can rewrite this as `(1 + e^(-z_o))^(-1)`.

Now, we apply the chain rule:

```
da_o/dz_o = -1 * (1 + e^(-z_o))^(-2) * (-e^(-z_o))
          = e^(-z_o) / (1 + e^(-z_o))^2
```

Here, we can notice that:

```
1 - a_o = 1 - 1 / (1 + e^(-z_o))
        = e^(-z_o) / (1 + e^(-z_o))
```

So, we can rewrite our derivative as below:

```
e^(-z_o) / (1 + e^(-z_o))^2 = [1 / (1 + e^(-z_o))] * [e^(-z_o) / (1 + e^(-z_o))]
                             = a_o * (1 - a_o)
```

The sigmoid function has this nice property where its derivative can be expressed using its own output. This is also very convenient because we already computed `a_o` during the forward pass, so we do not need to recalculate anything.

```
dz_o/dw2 = a_h
```

This is because `z_o = w2 * a_h + b2`, so the derivative with respect to `w2` is simply `a_h`.

Putting it all together:

```
dL/dw2 = -(y - a_o) * a_o * (1 - a_o) * a_h
```

**Gradient for w1:**

For w1, the chain is longer because w1 is further from the output. But the principle is exactly the same - we just multiply more terms together. We need to go through more steps:

```
dL/dw1 = (dL/da_o) * (da_o/dz_o) * (dz_o/da_h) * (da_h/dz_h) * (dz_h/dw1)
```

We already know the first two terms. Let's calculate the new ones:

```
dz_o/da_h = w2
```

This is because `z_o = w2 * a_h + b2`, so the derivative with respect to `a_h` is `w2`.

```
da_h/dz_h = a_h * (1 - a_h)
```

This is again the derivative of the sigmoid function.

```
dz_h/dw1 = x
```

This is because `z_h = w1 * x + b1`, so the derivative with respect to `w1` is `x`.

Putting it all together:

```
dL/dw1 = -(y - a_o) * a_o * (1 - a_o) * w2 * a_h * (1 - a_h) * x
```

Here, we can see that the gradient for w1 reuses the error signal `dL/da_o * da_o/dz_o` that we already computed for w2. This is the key insight of backpropagation - we reuse the error signals computed at later layers when computing gradients for earlier layers. This makes the computation very efficient because we do not have to calculate everything from scratch for each weight.

**Gradients for biases:**

We also need to calculate the gradients for the biases. The process is similar. For `b2`, since `z_o = w2 * a_h + b2`, the derivative of `z_o` with respect to `b2` is simply `1`. So:

```
dL/db2 = -(y - a_o) * a_o * (1 - a_o) * 1
```

Similarly, for `b1`, since `z_h = w1 * x + b1`, the derivative of `z_h` with respect to `b1` is `1`. So:

```
dL/db1 = -(y - a_o) * a_o * (1 - a_o) * w2 * a_h * (1 - a_h) * 1
```

Here, we can see that the bias gradients follow the same chain rule pattern as the weight gradients. The only difference is that the last term in the chain is `1` instead of the input value.

## Step-by-Step Numeric Example

The best way to learn this is by taking an example. Let's initialize our network with the following values:

```
x = 0.5       (input)
y = 1.0       (expected output)
w1 = 0.3      (weight 1)
b1 = 0.1      (bias 1)
w2 = 0.7      (weight 2)
b2 = 0.2      (bias 2)
```

**Forward Pass:**

Step 1: Calculate the hidden neuron output.

```
z_h = w1 * x + b1 = 0.3 * 0.5 + 0.1 = 0.25
a_h = sigmoid(0.25) = 1 / (1 + e^(-0.25)) = 0.5622
```

Step 2: Calculate the output neuron output.

```
z_o = w2 * a_h + b2 = 0.7 * 0.5622 + 0.2 = 0.5935
a_o = sigmoid(0.5935) = 1 / (1 + e^(-0.5935)) = 0.6442
```

Here, our predicted output is `0.6442`, but the expected output is `1.0`.

**Note:** We are rounding intermediate values to 4 decimal places for clarity. The Python implementation later uses full precision, so you may notice slight differences in the final digits.

Step 3: Calculate the loss.

```
L = (1/2) * (1.0 - 0.6442)^2 = (1/2) * (0.3558)^2 = 0.0633
```

**Backward Pass:**

Now, let's calculate the gradients.

Step 4: Gradient for w2.

```
dL/da_o = -(1.0 - 0.6442) = -0.3558
da_o/dz_o = 0.6442 * (1 - 0.6442) = 0.6442 * 0.3558 = 0.2292
dz_o/dw2 = a_h = 0.5622
dL/dw2 = -0.3558 * 0.2292 * 0.5622 = -0.0459
```

Step 5: Gradient for w1.

```
dz_o/da_h = w2 = 0.7
da_h/dz_h = 0.5622 * (1 - 0.5622) = 0.5622 * 0.4378 = 0.2461
dz_h/dw1 = x = 0.5
dL/dw1 = -0.3558 * 0.2292 * 0.7 * 0.2461 * 0.5 = -0.0070
```

Now, we have the gradients. The negative sign tells us that we need to increase both weights to reduce the loss. Now, it's time to learn about how we use these gradients to update the weights.

## Weight Update Using Gradient Descent

Once we have the gradients, we update the weights using the [gradient descent](https://outcomeschool.com/blog/math-behind-gradient-descent) formula:

```
w_new = w_old - learning_rate * (dL/dw)
```

Here, the **learning rate** is a small number (like 0.1 or 0.01) that controls how big each step is. If the learning rate is too large, we overshoot the optimal value. If it is too small, learning will be very slow.

Let's use a learning rate of 0.5:

```
w2_new = 0.7 - 0.5 * (-0.0459) = 0.7 + 0.0229 = 0.7229
w1_new = 0.3 - 0.5 * (-0.0070) = 0.3 + 0.0035 = 0.3035
```

Here, we can see that both weights increased slightly. If we run the forward pass again with these new weights, we will get a prediction closer to `1.0` and the loss will be smaller.

This process of forward pass, loss calculation, backward pass, and weight update is repeated many times during training. With each iteration, the network gets better at making predictions.

This same loop runs when we take an already trained model and adapt it to our own task. We have a detailed blog on [How does fine-tuning work?](https://outcomeschool.com/blog/how-does-fine-tuning-work) that explains it end to end.

Now, we have understood the complete math. Till now, we have learned all the theory and verified it with a numeric example. Now, let's put it all together in a working Python implementation.

## Backpropagation in Python

Now, let's implement the complete backpropagation example in Python as below:

```python
import math
# Initialize
x = 0.5
y = 1.0
w1, b1 = 0.3, 0.1
w2, b2 = 0.7, 0.2
learning_rate = 0.5
def sigmoid(z):
    return 1 / (1 + math.exp(-z))
# Training loop
for epoch in range(1000):
    # Forward pass
    z_h = w1 * x + b1
    a_h = sigmoid(z_h)
    z_o = w2 * a_h + b2
    a_o = sigmoid(z_o)
    # Loss
    loss = 0.5 * (y - a_o) ** 2
    # Backward pass
    dL_da_o = -(y - a_o)
    da_o_dz_o = a_o * (1 - a_o)
    dz_o_dw2 = a_h
    dz_o_da_h = w2
    da_h_dz_h = a_h * (1 - a_h)
    dz_h_dw1 = x
    dL_dw2 = dL_da_o * da_o_dz_o * dz_o_dw2
    dL_dw1 = dL_da_o * da_o_dz_o * dz_o_da_h * da_h_dz_h * dz_h_dw1
    dL_db2 = dL_da_o * da_o_dz_o
    dL_db1 = dL_da_o * da_o_dz_o * dz_o_da_h * da_h_dz_h
    # Weight update
    w2 = w2 - learning_rate * dL_dw2
    w1 = w1 - learning_rate * dL_dw1
    b2 = b2 - learning_rate * dL_db2
    b1 = b1 - learning_rate * dL_db1
    if epoch % 200 == 0:
        print(f"Epoch {epoch}, Loss: {loss:.6f}, Prediction: {a_o:.6f}")
print(f"Final prediction: {a_o:.6f}")
```

Here, we have implemented the complete forward pass, backward pass, and weight update in a training loop. We run it for 1000 epochs (an **epoch** is one complete pass through the training data). Since we have a single training example, each iteration is one epoch. The loss decreases with each epoch, and the prediction gets closer and closer to the expected output of `1.0`.

This will print the following:

```
Epoch 0, Loss: 0.063306, Prediction: 0.644173
Epoch 200, Loss: 0.001997, Prediction: 0.936796
Epoch 400, Loss: 0.000917, Prediction: 0.957166
Epoch 600, Loss: 0.000585, Prediction: 0.965799
Epoch 800, Loss: 0.000426, Prediction: 0.970806
Final prediction: 0.974146
```

Here, we can see how the loss decreases from `0.063306` to almost `0.000426` after 800 epochs, and the prediction moves from `0.644173` to `0.974146`, which is very close to our expected output of `1.0`.

This is how the math behind backpropagation works. The chain rule allows us to efficiently compute how much each weight contributes to the error. And gradient descent uses that information to update the weights in the right direction. Now, we have understood the complete math behind backpropagation and how neural networks learn from their mistakes.

## Frequently Asked Questions

### Is backpropagation the same as gradient descent?

No. Backpropagation uses the chain rule to compute how much each weight contributes to the error. Gradient descent then uses those gradients to update the weights in the right direction. The two work together in every training loop.

### Why is backpropagation efficient?

Backpropagation reuses the error signals computed at later layers when it computes gradients for earlier layers. For example, the gradient for `w1` reuses the error signal already computed for `w2`. So, we do not have to calculate everything from scratch for each weight.

### Why does a neural network need an activation function?

The activation function introduces non-linearity, which allows the network to learn complex patterns like curves. Without it, no matter how many layers we stack, the network would only be able to learn simple straight-line relationships.

### What happens if the learning rate is too large or too small?

If the learning rate is too large, we overshoot the optimal value. If it is too small, learning will be very slow. The learning rate is a small number that controls how big each step of the weight update is.

### Why is there a 1/2 in the squared error loss?

The `(1/2)` is a constant that makes the math cleaner when we calculate the derivative. It only changes the scale of the gradients, not their direction, and the learning rate compensates for this.
