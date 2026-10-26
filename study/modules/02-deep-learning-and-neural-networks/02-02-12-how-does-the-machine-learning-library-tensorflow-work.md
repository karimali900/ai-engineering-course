---
title: How Does The Machine Learning Library TensorFlow Work?
module: 2
module_title: Deep Learning and Neural Networks
lesson: '2.12'
source: https://outcomeschool.com/blog/how-does-the-machine-learning-library-tensorflow-work
published: August 2, 2019
tags:
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 1206
reading_time: 6
status: full
---
# How Does The Machine Learning Library TensorFlow Work?

> **Module 2 · Lesson 2.12**  
> Source: [Outcome School](https://outcomeschool.com/blog/how-does-the-machine-learning-library-tensorflow-work) · Published: August 2, 2019 · Reading time: ~6 min · Tags: `ai`, `machine-learning`

---

![How Does The Machine Learning Library TensorFlow Work?](../../assets/images/02-02-12-how-does-the-machine-learning-library-tensorflow-work/how-does-the-machine-learning-library-tensorflow-work.png)

TensorFlow is an open-source machine learning framework. It works by letting us build a data flow graph, where each node is an operation, and then executing that graph on one or more CPUs or GPUs.

In this blog, we will learn how the Machine Learning library TensorFlow works.

Let's get started.

TensorFlow is an open-source machine learning framework for everyone. As I believe, when we know the internals of a library, we can get the most out of it. And we feel much more confident while working with that library. Today, TensorFlow is being used by the top companies like Google, Uber, Airbnb, Nvidia, Dropbox, etc.

Believe me, you can achieve anything out of it. It is mainly designed for deep [neural network](https://outcomeschool.com/blog/neural-network) models.

**TensorFlow supports the following:**

- TensorFlow lets you deploy computation to one or more CPUs or [GPUs](https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning) in a desktop, server, or mobile device in a very simple way. This way the things can be done very fast.
- TensorFlow lets you express your computation as a data flow graph.
- TensorFlow lets you visualize the graph using the in-built tensorboard. You can inspect and debug the graph very easily.
- TensorFlow gives the best performance with an ability to iterate quickly, train models faster and run more experiments.
- TensorFlow runs on nearly everything: GPUs and CPUs - including mobile and embedded platforms (see [TensorFlow Lite on Android](https://outcomeschool.com/blog/android-tensorflow-lite-machine-learning-example)) - and even tensor processing units (TPUs), which are specialized hardware to do the tensor math on.

PyTorch is another widely used library for the same kind of work. We have a blog on [how PyTorch works](https://outcomeschool.com/blog/how-does-pytorch-work) that covers it in depth.

How does the TensorFlow flexible enough to support all the above features?

The architecture of the TensorFlow helps it supporting all the above and much more.

First of all, you must know that in TensorFlow, you build a graph in which you define the constants, variables, operations and then you execute it. The graph is a data structure which consists of all the constants, variables and operations that you want to do.

The node represents an operation.

The edges are carriers of data structures (tensors), where an output of one operation (from one node) becomes the input for another operation.

You do the things in TensorFlow library like below.

```python
import tensorflow as tf
# Basic constant operations
# The value returned by the constructor represents the output
# of the Constant op.
a = tf.constant(2)
b = tf.constant(3)
# Launch the default graph.
with tf.Session() as sess:
    print "a: %i" % sess.run(a), "b: %i" % sess.run(b)
    print "Addition with constants: %i" % sess.run(a+b)
    print "Multiplication with constants: %i" % sess.run(a*b)
# a=2, b=3
# Addition with constants: 5
# Multiplication with constants: 6
# Basic Operations with variable as graph input
# The value returned by the constructor represents the output
# of the Variable op. (define as input when running session)
# tf Graph input
a = tf.placeholder(tf.int16)
b = tf.placeholder(tf.int16)
# Define some operations
add = tf.add(a, b)
mul = tf.multiply(a, b)
# Launch the default graph.
with tf.Session() as sess:
    # Run every operation with variable input
    print "Addition with variables: %i" % sess.run(add, feed_dict={a: 2, b: 3})
    print "Multiplication with variables: %i" % sess.run(mul, feed_dict={a: 2, b: 3})
# Addition with variables: 5
# Multiplication with variables: 6
```

Let’s see it by building a mini TensorFlow. We will try to build a small library just for understanding how the TensorFlow works.

Create a class for the operations called TFOperation.

```python
class TFOperation():
def __init__(self, input_nodes=[]):
    self.input_nodes = input_nodes
    self.output_nodes = []
    for node in input_nodes:
        node.output_nodes.append(self)
    _default_graph.operations.append(self)
def compute(self):
    pass
```

Then, extend TFOperation class to make add class.

```python
class add(TFOperation, object):
    def __init__(self,x,y):
        super(add, self).__init__([x,y])
    def compute(self, x_var, y_var):
        self.inputs = [x_var, y_var]
        return x_var + y_var
```

Similarly, we can extend the TFOperation to make multiply class.

```python
class multiply(TFOperation, object):
    def __init__(self,x,y):
        super(multiply, self).__init__([x,y])
    def compute(self, x_var, y_var):
        self.inputs = [x_var, y_var]
        return x_var * y_var
```

Now, create the Placeholder class for the variables.

```python
class Placeholder():
    def __init__(self):
        self.output_nodes = []
        _default_graph.placeholders.append(self)
```

Now, create the Constant class.

```python
class Constant():
    def __init__(self, initial_value=None):
        self.value = initial_value
        self.output_nodes = []
        _default_graph.variables.append(self)
```

Then, we will create the Graph class.

```python
class Graph():
    def __init__(self):
        self.operations = []
        self.placeholders = []
        self.variables = []
    def set_as_default(self):
        global _default_graph
        _default_graph = self
```

Now, let's make the utility function `traverse_postorder` so that the operations happen in the correct order.

```python
def traverse_postorder(operation):
    nodes_postorder = []
    def recurse(node):
        if isinstance(node, TFOperation):
            for input_node in node.input_nodes:
                recurse(input_node)
        nodes_postorder.append(node)
    recurse(operation)
    return nodes_postorder
```

Finally create the Session class.

```python
import numpy as np
class Session():
    def run(self, operation, feed_dict={}):
        nodes_postorder = traverse_postorder(operation)
        for node in nodes_postorder:
            if isinstance(node, Placeholder):
                node.output = feed_dict[node]
            elif isinstance(node, Constant):
                node.output = node.value
            else:
                # OPERATION
                node.inputs = [input_node.output for input_node in node.input_nodes]
                node.output = node.compute(*node.inputs)
            if type(node.output) == list:
                node.output = np.array(node.output)
        return operation.output
```

So, our mini TensorFlow library is ready.

Let’s do some operations with constants and placeholder(variables).

We will do the following operations with our mini TensorFlow library.

```python
y = mx + c
m = 10
c = 1
y = 10x + 1
```

```python
# Create the Graph
g = Graph()
# Set the graph as default
g.set_as_default()
# Create a constant
m = Constant(10)
# Create an another constant
c = Constant(1)
# Create a variable using Placeholder
x = Placeholder()
# Create add and multiply operation
y = add(multiply(m,x), c)
# Create the session
sess = Session()
# Run the session to get the result
result = sess.run(operation=y, feed_dict={x:10})
# Print the result
print(result)
```

So, this is how the TensorFlow works.

## Frequently Asked Questions

### What is a graph in TensorFlow?

A graph is a data structure that holds all the constants, variables, and operations that we want to run. Each node represents an operation. The edges carry tensors, where the output of one node becomes the input for another node.

### Can TensorFlow run on mobile devices?

Yes. TensorFlow lets us deploy computation to one or more CPUs or GPUs in a desktop, server, or mobile device. It runs on nearly everything, including mobile and embedded platforms, and even on tensor processing units (TPUs).

### What is the difference between a Placeholder and a Constant in TensorFlow?

A Constant holds a fixed value that we give it when we create it. A Placeholder is used for a variable input, and it gets its value only when we run the session, through the `feed_dict`.

### Why are the operations traversed in postorder before running them?

Postorder traversal makes the operations happen in the correct order. It visits all the input nodes of an operation before the operation itself. So, when the session computes a node, the outputs of its inputs are already ready.
