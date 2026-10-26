---
title: How Does Matrix Multiplication Work in Neural Networks?
module: 2
module_title: Deep Learning and Neural Networks
lesson: '2.3'
source: https://outcomeschool.com/blog/matrix-multiplication-in-neural-networks
published: October 22, 2026
tags:
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 3196
reading_time: 16
status: full
---
# How Does Matrix Multiplication Work in Neural Networks?

> **Module 2 · Lesson 2.3**  
> Source: [Outcome School](https://outcomeschool.com/blog/matrix-multiplication-in-neural-networks) · Published: October 22, 2026 · Reading time: ~16 min · Tags: `ai`, `machine-learning`

---

![How Does Matrix Multiplication Work in Neural Networks?](../../assets/images/02-02-03-how-does-matrix-multiplication-work-in-neural-networks/matrix-multiplication-in-neural-networks.png)

Matrix multiplication in neural networks is the operation that takes the input numbers, multiplies them with the weights of all the neurons in a layer, and adds up the results, all in one step. Most of the work a neural network does is this one operation, repeated layer after layer.

In this blog, we will learn about how matrix multiplication works in neural networks. We will also see what vectors, matrices, and the dot product are, the row-times-column rule with a fully worked example, the shape rule that tells us which matrices can be multiplied, how one layer of neurons becomes one matrix multiplication plus a bias, how we process many inputs at once, and why GPUs are so good at this.

We will cover the following:

- What are Vectors and Matrices?
- What is a Dot Product?
- How does Matrix Multiplication Work?
- The Shape Rule
- One Layer of Neurons is One Matrix Multiplication
- Processing Many Inputs at Once
- Why is the GPU Perfect for Matrix Multiplication?

Let's get started.

## What are Vectors and Matrices?

A [neural network](https://outcomeschool.com/blog/neural-network) does not understand pictures, words, or sounds directly. It understands only numbers. So, before anything goes into a neural network, we turn it into a list of numbers.

A **vector** is a list of numbers written in a fixed order.

For example, we can describe a house with 3 numbers: the number of bedrooms, the number of bathrooms, and the number of floors.

```text
[3, 2, 1]
```

This is a vector with 3 numbers in it. The order matters. The first number is always bedrooms, the second is always bathrooms, and the third is always floors.

A **matrix** is a table of numbers arranged in rows and columns. We can think of it as many vectors stacked on top of each other. For example, 2 houses described with 3 numbers each give us a matrix like below:

```text
[ 3  2  1 ]    <- house 1
[ 4  3  2 ]    <- house 2
```

This matrix has 2 rows and 3 columns. We call it a **2 x 3** matrix. We always say the number of rows first and the number of columns second. This "rows x columns" is the **shape** of the matrix.

## What is a Dot Product?

Before jumping into matrix multiplication, we must know the dot product, because matrix multiplication is nothing but many dot products done together.

A **dot product** takes two vectors of the same length, multiplies the matching numbers, and adds all the results to get one single number.

Let's say we go to a shop and buy 2 pens, 3 notebooks, and 1 bag. A pen costs 10, a notebook costs 5, and a bag costs 20.

```text
quantities = [2, 3, 1]
prices     = [10, 5, 20]
```

To find the total bill, we multiply each quantity with its price and add them up:

**total = 2 \* 10 + 3 \* 5 + 1 \* 20 = 20 + 15 + 20 = 55**

This is exactly a dot product. Two lists of 3 numbers go in, and one number, 55, comes out.

Now, let's see why this is important for neural networks. A single neuron does exactly this. It takes the input numbers, multiplies each one with its own **weight**, and adds them up. A weight is a number that tells the neuron how important each input is. In the shop example, the prices play the role of the weights.

**So, one neuron = one dot product.**

## How does Matrix Multiplication Work?

Now that we have learned about the dot product, it's time to learn about matrix multiplication.

When we multiply matrix A with matrix B, every number in the answer is one dot product: **one row of A with one column of B**. This is called the **row-times-column rule**.

The best way to learn this is by taking an example.

Let's take matrix A of shape 2 x 3 and matrix B of shape 3 x 2:

```text
A = [ 1  2  3 ]        B = [  7   8 ]
    [ 4  5  6 ]            [  9  10 ]
                           [ 11  12 ]
```

The answer C will have 2 rows (the rows of A) and 2 columns (the columns of B). So, C is a 2 x 2 matrix, and we need to find 4 numbers.

**Step 1:** We find the number at row 1, column 1. We take row 1 of A, which is [1, 2, 3], and column 1 of B, which is [7, 9, 11].

**1 \* 7 + 2 \* 9 + 3 \* 11 = 7 + 18 + 33 = 58**

**Step 2:** We find the number at row 1, column 2. We take row 1 of A, [1, 2, 3], and column 2 of B, [8, 10, 12].

**1 \* 8 + 2 \* 10 + 3 \* 12 = 8 + 20 + 36 = 64**

**Step 3:** We find the number at row 2, column 1. We take row 2 of A, [4, 5, 6], and column 1 of B, [7, 9, 11].

**4 \* 7 + 5 \* 9 + 6 \* 11 = 28 + 45 + 66 = 139**

**Step 4:** We find the number at row 2, column 2. We take row 2 of A, [4, 5, 6], and column 2 of B, [8, 10, 12].

**4 \* 8 + 5 \* 10 + 6 \* 12 = 32 + 50 + 72 = 154**

Let's see Step 1 as a diagram, because every step follows the same path:

```text
┌──────────────────────────────────────┐
│ row 1 of A = [1, 2, 3]               │
│ column 1 of B = [7, 9, 11]           │
└──────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────┐
│ multiply the matching numbers        │
│ 1*7 = 7, 2*9 = 18, 3*11 = 33         │
└──────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────┐
│ add them up                          │
│ 7 + 18 + 33 = 58                     │
└──────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────┐
│ C at row 1, column 1 = 58            │
└──────────────────────────────────────┘
```

Here, we can see that one row and one column go in, and exactly one number comes out. Steps 2, 3, and 4 use a different row or column, but the path is the same.

So, the final answer is:

```text
C = [  58   64 ]
    [ 139  154 ]
```

Let's verify this with NumPy, a popular Python library for working with numbers. In NumPy, the `@` symbol means matrix multiplication. We can write the code as below:

```python
import numpy as np
A = np.array([[1, 2, 3],
              [4, 5, 6]])
B = np.array([[7, 8],
              [9, 10],
              [11, 12]])
C = A @ B
print(C)
print(C.shape)
```

This will print the following:

```text
[[ 58  64]
 [139 154]]
(2, 2)
```

Here, we can see that NumPy gives the same 4 numbers that we calculated by hand, and the shape of the answer is 2 x 2.

This is how matrix multiplication works. It is a set of dot products, one for every row of A paired with every column of B.

## The Shape Rule

In the example above, a row of A had 3 numbers and a column of B also had 3 numbers. That is why the dot product worked. If the lengths did not match, some numbers would have no partner to multiply with.

This gives us the shape rule:

**(m x n) @ (n x p) = (m x p)**

- The number of columns of A (n) must be the same as the number of rows of B (n). These are the two "inside" numbers.
- The answer takes its rows from A (m) and its columns from B (p). These are the two "outside" numbers.

In our example:

**(2 x 3) @ (3 x 2) = (2 x 2)**

The inside numbers are 3 and 3. They match, so the multiplication is allowed. The outside numbers, 2 and 2, give the shape of the answer.

Now, let's see what happens if the inside numbers do not match. Let's try to multiply a 2 x 3 matrix with another 2 x 3 matrix:

```python
import numpy as np
A = np.ones((2, 3))
B = np.ones((2, 3))
C = A @ B
```

NumPy stops with an error:

```text
ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 2 is different from 3)
```

Here, the last part of the error, "size 2 is different from 3", tells us that the inside numbers do not match. A row of A has 3 numbers, but a column of B has only 2 numbers, so the dot product cannot be done.

This shape mismatch error is one of the most common errors while building neural networks. Most of the time, we do mistakes in the shapes, and the shape rule is how we find and fix them.

## One Layer of Neurons is One Matrix Multiplication

Now, let's connect everything to neural networks.

A **layer** in a neural network is a group of neurons that all look at the same input. Each neuron does the following:

- It takes a dot product of the input with its own weights.
- It adds its own extra number called the [**bias**](https://outcomeschool.com/blog/bias-in-artificial-neural-network). The bias lets the neuron shift its output up or down, even when the inputs are zero.

After this, the neuron usually passes the result through an activation function, a small function that helps the network learn complex patterns. That part comes after the multiplication, so we will keep it aside in this blog.

Let's say our input has 3 numbers, and our layer has 2 neurons.

```text
input x = [1, 2, 3]
neuron 1 weights = [2, 1, 0],  bias = 1
neuron 2 weights = [0, 1, 3],  bias = -2
```

If we compute each neuron one by one, we first take the dot product and then add the bias:

**neuron 1 = (1 \* 2 + 2 \* 1 + 3 \* 0) + 1 = 4 + 1 = 5**

**neuron 2 = (1 \* 0 + 2 \* 1 + 3 \* 3) + (-2) = 11 - 2 = 9**

Now, here comes the matrix multiplication into the picture. Instead of computing each neuron separately, we put the weights of each neuron as one **column** of a weight matrix W:

```text
          neuron 1   neuron 2
W  =    [    2          0    ]
        [    1          1    ]
        [    0          3    ]
b  =    [    1         -2    ]
```

W has 3 rows (one for each input number) and 2 columns (one for each neuron). So, W is a 3 x 2 matrix.

Now, the whole layer becomes one line:

**output = x @ W + b**

Here, we can think of x as a matrix with 1 row and 3 columns, so x is 1 x 3. The inside numbers are 3 and 3, so the multiplication is allowed.

Let's see the code for this:

```python
import numpy as np
x = np.array([1, 2, 3])
W = np.array([[2, 0],
              [1, 1],
              [0, 3]])
b = np.array([1, -2])
print(x @ W + b)
```

This will print the following:

```text
[5 9]
```

Here, we can see that we get the same 5 and 9 that we calculated neuron by neuron. The row of x meets column 1 of W to give neuron 1, and meets column 2 of W to give neuron 2.

Let's see the shapes flowing through this layer as a diagram:

```text
┌──────────────────────────────────────┐
│ input x = [1, 2, 3]                  │
│ shape 1 x 3                          │
└──────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────┐
│ x @ W                                │
│ (1 x 3) @ (3 x 2) = (1 x 2)          │
│ result = [4, 11]                     │
└──────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────┐
│ add bias b = [1, -2]                 │
│ [4, 11] + [1, -2] = [5, 9]           │
└──────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────┐
│ output = [5, 9]                      │
│ shape 1 x 2, one number per neuron   │
└──────────────────────────────────────┘
```

Here, we can see that 3 numbers go in and 2 numbers come out, because the layer has 2 neurons. The bias does not change the shape. It only shifts each number.

**A full layer of neurons is exactly one matrix multiplication plus a bias.** A layer with 1,000 neurons is still one line of code. Only the shape of W changes.

We have a detailed blog on [feed-forward networks in LLMs](https://outcomeschool.com/blog/feed-forward-networks-in-llms) that explains how two such layers work inside every Transformer layer.

The shape of W tells us everything about the layer:

**W shape = (number of inputs) x (number of neurons)**

**Note:** Some libraries store W the other way round, as (number of neurons) x (number of inputs), and flip it (swap its rows and columns) before multiplying. The idea stays the same.

A deep neural network is many such layers, one after another. The output of one layer becomes the input of the next layer.

## Processing Many Inputs at Once

In the example above, we passed only one input. But in practice, we pass many inputs together. We call a group of inputs processed together a **batch**.

Let's say we have 2 inputs instead of 1:

```text
input 1 = [1, 2, 3]
input 2 = [4, 5, 6]
```

We could run the layer twice, once for each input. But there is a better way. We stack the inputs as rows of one matrix X:

```text
X = [ 1  2  3 ]    <- input 1
    [ 4  5  6 ]    <- input 2
```

Now, X is a 2 x 3 matrix, and we do one bigger multiplication:

**(2 x 3) @ (3 x 2) = (2 x 2)**

Each row of the answer is the output of the layer for one input. Let's see the code for this:

```python
import numpy as np
X = np.array([[1, 2, 3],
              [4, 5, 6]])
W = np.array([[2, 0],
              [1, 1],
              [0, 3]])
b = np.array([1, -2])
print(X @ W + b)
```

This will print the following:

```text
[[ 5  9]
 [14 21]]
```

Here, we can see that the first row, [5, 9], is the same answer we got for input 1 before. The second row, [14, 21], is the answer for input 2. Let's check it: (4 \* 2 + 5 \* 1 + 6 \* 0) + 1 = 13 + 1 = 14, and (4 \* 0 + 5 \* 1 + 6 \* 3) + (-2) = 23 - 2 = 21.

Notice that the bias b is a single row of 2 numbers, but the answer has 2 rows, one for each input. NumPy adds the same bias to every row automatically. This is called **broadcasting**.

We use the same W for every input. Only the number of rows in X changes. And one big multiplication is much faster than many small ones, because the hardware can work on all the rows together. We will see why in the next section.

Now, let's take a bigger example. We have a batch of 32 inputs, each with 784 numbers. The first layer has 128 neurons, so its weight matrix W1 is 784 x 128. The second layer has 10 neurons, and it receives 128 numbers from the first layer, so its weight matrix W2 is 128 x 10. Let's see the shapes flowing through both layers as a diagram:

```text
┌──────────────────────────────────────────┐
│ batch X: 32 inputs, 784 numbers each     │
│ shape 32 x 784                           │
└──────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────┐
│ layer 1: W1 shape 784 x 128              │
│ (32 x 784) @ (784 x 128) = (32 x 128)    │
└──────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────┐
│ layer 2: W2 shape 128 x 10               │
│ (32 x 128) @ (128 x 10) = (32 x 10)      │
└──────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────┐
│ output: 32 rows, 10 numbers each         │
│ shape 32 x 10                            │
└──────────────────────────────────────────┘
```

Here, we can see that the number of rows stays 32 all the way down, because every row is one input. Only the number of columns changes, and it always becomes the number of neurons in that layer. We leave the bias out of this diagram, because it does not change the shape.

## Why is the GPU Perfect for Matrix Multiplication?

Now, the next big question is: why do we need a GPU for this?

Let's count the work. When we multiply an (m x n) matrix with an (n x p) matrix, the answer has m \* p numbers, and each of them is a dot product with n multiplications. So, we need m \* n \* p multiplications in total. For the first layer in the example above:

**32 \* 784 \* 128 = 3,211,264 multiplications**

That is more than 3 million multiplications for one layer and one small batch. Large models do billions of them for every single input.

Now, let's look back at our worked example. To find 58, we needed only row 1 of A and column 1 of B. To find 154, we needed only row 2 of A and column 2 of B. **No number in the answer depends on any other number in the answer.** So, all of them can be computed at the same time.

A chip does its calculations using **cores**. A core is one worker inside the chip that can do calculations on its own. A **CPU** has a small number of very powerful cores. It is great at doing a few complex tasks one after another.

A **GPU** has thousands of smaller, simpler cores. Each core can do a multiply and an add very quickly. Since every number in the answer is an independent dot product, the GPU gives different dot products to different cores, and they all run in parallel.

Let's say we have to check 10,000 exam answer sheets. One brilliant professor checking them one by one will take a long time. A thousand teachers, each checking 10 sheets at the same time, will finish much faster. The CPU is the brilliant professor, and the GPU is the thousand teachers.

Let's see this for our 2 x 2 example as a diagram:

```text
┌─────────────────────────────────────────────┐
│ A @ B needs 4 dot products                  │
└─────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ GPU: all 4 dot products at the same time    │
│                                             │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │
│ │ core 1 │ │ core 2 │ │ core 3 │ │ core 4 │ │
│ │   58   │ │   64   │ │  139   │ │  154   │ │
│ └────────┘ └────────┘ └────────┘ └────────┘ │
└─────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ C = [[58, 64], [139, 154]]                  │
└─────────────────────────────────────────────┘
```

Here, we can see that each core computes one number of C, and no core waits for another core. In a real GPU, thousands of cores do this together for much bigger matrices.

Modern GPUs also have special units built only for matrix multiplication. This is why neural networks are trained and run on GPUs.

We have a detailed blog on [how a GPU works for deep learning](https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning) that explains this step by step.

Now we must have understood how matrix multiplication works in neural networks, from a single dot product to a full batch of inputs running through many layers on a GPU.

## Frequently Asked Questions

### What does the @ symbol mean in NumPy?

The @ symbol means matrix multiplication in NumPy. When we write A @ B, NumPy takes the dot product of every row of A with every column of B and gives us the answer matrix. If the inside numbers of the two shapes do not match, NumPy stops with a shape mismatch error.

### What is the shape of the weight matrix of a layer?

The weight matrix W of a layer has the shape (number of inputs) x (number of neurons). Each column of W holds the weights of one neuron. Some libraries store W the other way round, as (number of neurons) x (number of inputs), and flip it before multiplying, but the idea stays the same.

### How many multiplications does a matrix multiplication need?

Multiplying an (m x n) matrix with an (n x p) matrix needs m \* n \* p multiplications. The answer has m \* p numbers, and each of them is a dot product with n multiplications. For a batch of 32 inputs with 784 numbers each going into a layer of 128 neurons, that is 3,211,264 multiplications.

### Is the activation function part of the matrix multiplication?

No. The activation function is not part of the matrix multiplication. A layer first does the matrix multiplication and adds the bias, and then the neuron usually passes the result through an activation function, a small function that helps the network learn complex patterns.
