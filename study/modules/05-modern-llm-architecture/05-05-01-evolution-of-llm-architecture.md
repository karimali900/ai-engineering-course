---
title: Evolution of LLM Architecture
module: 5
module_title: Modern LLM Architecture
lesson: '5.1'
source: https://outcomeschool.com/blog/evolution-of-llm-architecture
published: September 21, 2026
tags:
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 5985
reading_time: 30
status: full
---
# Evolution of LLM Architecture

> **Module 5 · Lesson 5.1**  
> Source: [Outcome School](https://outcomeschool.com/blog/evolution-of-llm-architecture) · Published: September 21, 2026 · Reading time: ~30 min · Tags: `llm`, `ai`, `machine-learning`

---

![Evolution of LLM Architecture](../../assets/images/05-05-01-evolution-of-llm-architecture/evolution-of-llm-architecture.png)

LLM architecture evolved in stages: from RNNs that read one word at a time, to Attention, to the Transformer, to making models bigger, and then to Mixture of Experts (MoE) that makes big models cheaper to run.

In this blog, we will learn about the Evolution of LLM Architecture, the step-by-step journey of how the design of large language models changed from simple word-by-word readers to the massive AI models we use today. We will also see why the early models kept forgetting, how attention solved that problem, how the Transformer removed the slow parts, how making models bigger made them smarter, how Mixture of Experts made big models cheaper to run, what problems still remain, and what is coming next.

We will cover the following:

- What is an LLM Architecture?
- Stage 1: Reading one word at a time (RNN)
- Stage 2: Attention
- Stage 3: The Transformer
- Stage 4: Scaling
- Stage 5: Mixture of Experts (MoE)
- Stage 6: New Directions
- Summary of the evolution

Let's get started.

## What is an LLM Architecture?

**An LLM Architecture is the blueprint of a large language model. It describes how the model reads text, how it remembers what it has read, and how it produces the next word.**

Let's break the name.

**LLM = Large + Language + Model**

- **Language**: it works with text, the words we read and write every day.
- **Model**: it is a computer program that has learned patterns from a huge amount of text.
- **Large**: it has learned from a very large amount of text and has a very large number of internal settings.

**Architecture** is simply the design. Let's say we are building a house. The architecture is the plan that tells us where the rooms go, how big the doors are, and how the water flows. The bricks and cement are the same for every house, but the plan decides how good the house is.

Similarly, in an LLM, the numbers and the math are similar across models, but the architecture decides how the model reads, remembers, and answers.

Every big step in LLM architecture happened because the previous design had a problem.

- The first models forgot what they read.
- Then attention solved forgetting, but the models were still slow.
- Then the Transformer made them fast, but nobody knew how big to make them.
- Then scaling made them smart, but too costly to run.
- Then Mixture of Experts made them cheaper.
- And the story is still going on.

So, the best way to understand today's LLM is to walk through this timeline, one problem and one solution at a time.

Do not worry, we will learn about each of them in detail.

## Stage 1: Reading one word at a time (RNN)

Before Transformers, the most popular design for reading text was the **[Recurrent Neural Network (RNN)](https://outcomeschool.com/blog/recurrent-neural-network)**.

A neural network is a computer program made of a very large number of connected numbers that learns patterns from examples. Showing it a lot of examples so that it learns from them is called **training**. Do not worry about the internal details. For this blog, we only need to know how each design reads text.

**Note:** A model does not read whole words. It first cuts the text into small pieces called **[tokens](https://outcomeschool.com/blog/tokenization-in-llms)**. A token can be a full word, a part of a word, or a punctuation mark. For the sake of understanding, we will say word everywhere in this blog, but wherever we say word, the model is really working with a token.

Suppose we give an RNN the sentence: "The cat sat on the mat."

An RNN reads it one word at a time, from left to right. After reading each word, it updates a single small memory and then moves to the next word. The memory is like a tiny note. After reading "The", the note has something about "The". After "cat", the note is rewritten to remember "The cat". And so on, till the end.

At the end, the whole sentence is squeezed into that one small note.

Let's understand this with a picture:

```text
 Word:     The       cat       sat       on        the       mat
            |         |         |         |         |         |
            v         v         v         v         v         v
 Note:   [note] -> [note] -> [note] -> [note] -> [note] -> [note]
                                                              |
                                                              v
                                                   the whole sentence
                                                   lives in this one note
```

Here, there is only one note. The arrow from one note to the next shows that the same note is rewritten after every word. The only thing carried forward from the past is this note, nothing else.

This worked for short sentences. But, here is the catch.

**Problem 1: It forgets.**

Let's say the text is very long, like a full paragraph. By the time the model reaches the end, the note has been rewritten so many times that the early words are almost gone. If the paragraph starts with "Riya went to the market" and ends with "and then she bought", the model struggles to remember that "she" means Riya.

```text
 Riya  went  to  the  market  and  then  she  bought
  |                                       |
  |   the note is rewritten again and     |
  |   again between these two words       |
  v                                       v
 "Riya" is written into       by now "Riya" has mostly
 the note at the very start   faded out of the note
```

Here, we can see that "Riya" entered the note at the start, but every word after it overwrote the note a little more. By the time the model reaches "she", very less of "Riya" is left.

**Problem 2: It is slow to train.**

The model must read word 1 before word 2, and word 2 before word 3. Means, it cannot read all the words at the same time. So, even if we have a very powerful computer that can do thousands of things in parallel, the RNN uses it one step at a time.

Improved versions of RNN, called LSTM and GRU, reduced the forgetting a lot, but they did not remove it, and the slow one-by-one reading remained.

The issue with this approach is forgetting and slow training. Let's see how the next approach solve this issue.

## Stage 2: Attention

Here comes the **Attention** into the picture.

**Attention is a mechanism that lets the model look back at every word in the input and decide how much to focus on each one while processing the current word.**

In simple words, instead of keeping one tiny note, we keep the whole page open in front of us. When we need to understand a word, we look at whichever earlier words matter for it.

Let's see the difference with a picture:

```text
 RNN:
   Riya -> went -> to -> the -> market -> and -> then -> she
   (one small note passed along the chain, rewritten at each step)
 Attention:
   Riya   went   to   the   market   and   then   she
    ^      ^      ^    ^      ^       ^      ^     |
    |      |      |    |      |       |      |     |
    +------+------+----+------+-------+------+-----+
             "she" looks directly at every earlier word
```

Here, in the RNN, "she" can only see the note that reached it through the chain. In attention, "she" has a direct line to every earlier word. Nothing is lost on the way.

**Attention = Look at every word + Decide how much each one matters + Mix them accordingly**

Let's take the example again: "Riya went to the market and then she bought mangoes."

When the model is processing the word "she", attention lets it look at all the words before it and ask: which words help me understand "she"? The answer is "Riya". So, the model gives high attention to "Riya" and low attention to words like "to" and "the".

### How attention decides where to focus

The best way to learn this is by taking an example.

Suppose the model is processing "she". For the sake of understanding, let's look at only 4 of the earlier words. Attention gives each word a score that tells how important it is. Then it converts those scores into weights that add up to 1.

- Riya: 0.70
- went: 0.10
- market: 0.15
- then: 0.05

Here, we can see that "Riya" gets 70 percent of the focus. The model then builds its understanding of "she" mostly from "Riya", a little from "market", and very less from the others.

Let's see how the model builds "she" from these weights:

```text
   0.70 x Riya    ----+
   0.10 x went    ----+
   0.15 x market  ----+----> understanding of "she"
   0.05 x then    ----+
   ----
   1.00  (the weights add up to 1)
```

Here, each earlier word is multiplied by its weight and then all of them are added together. Since "Riya" has the biggest weight, the result is mostly "Riya".

That is all attention is. **A weighted mix of the other words, where the weights say how much each word matters.**

This simple idea is the heart of every modern LLM.

### Query, Key, and Value

Inside attention, every word plays three roles. Let's take an analogy of a library.

- **Query**: the question we are asking. When we are at "she", the query is "who is this person?"
- **Key**: the label on every book. Each earlier word carries a label that says what it is about. The word "Riya" carries a label like "a person's name".
- **Value**: the content inside the book. The actual information that the word carries.

The model compares the query with every key. The keys that match well get high scores. Then it collects the values, weighted by those scores. That gives us the weighted mix we saw above.

Here is how the flow looks:

```text
 Query from "she": who is this person?
          |
          v
 Compare the query with every key:
   Key of "Riya"   : a person's name  -> strong match
   Key of "went"   : an action        -> weak match
   Key of "market" : a place          -> weak match
          |
          v
 Collect the values, weighted by the match
          |
          v
 Understanding of "she", built mostly from the value of "Riya"
```

Here, the query is the question, the keys decide which words answer it well, and the values are the information we finally collect. The key only helps in matching. The actual content comes from the value.

We have a detailed blog on [the math behind Q, K, and V](https://outcomeschool.com/blog/math-behind-attention-qkv) that explains this step by step with real numbers.

### Self-Attention

When the words of a sentence pay attention to other words of the same sentence, we call it as **[Self-Attention](https://outcomeschool.com/blog/self-attention-in-transformers)**. The sentence is looking at itself. This is the form of attention used inside LLMs.

### Multi-Head Attention

One attention can focus on one kind of relationship at a time. But a sentence has many relationships. "she" relates to "Riya" by meaning, "bought" relates to "mangoes" by grammar, and so on.

So, instead of one attention, we run several attentions side by side. Each one is called a **head**. One head learns to track names, another learns to track grammar, another learns to track position, and etc. Then we combine what all the heads found.

This is called **[Multi-Head Attention](https://outcomeschool.com/blog/multi-head-attention-in-transformers)**. It is like having a team of readers where each reader is looking for a different thing in the same sentence.

```text
                   The sentence
                        |
         +--------------+--------------+
         |              |              |
         v              v              v
    +----------+   +----------+   +----------+
    |  Head 1  |   |  Head 2  |   |  Head 3  |
    |  tracks  |   |  tracks  |   |  tracks  |
    |  names   |   |  grammar |   | position |
    +----------+   +----------+   +----------+
         |              |              |
         +--------------+--------------+
                        |
                        v
               Combine all the heads
```

Here, all the heads read the same sentence at the same time, but each head is looking for a different kind of relationship. At the end, we combine what all of them found into one result.

Attention solved the forgetting problem, because now no word in the input is ever squeezed out of memory. Every word can be looked at directly.

But, in the beginning, attention was added on top of RNNs. The RNN still read the input one word at a time, and attention only helped the model look back at what the RNN had already read. So, the one-by-one slow reading was still there.

The issue with this approach is that the model still read slowly, one word at a time. Let's see how the next approach solve this issue.

## Stage 3: The Transformer

In 2017, a research paper with the title "Attention Is All You Need" asked a bold question: if attention is doing the real work, why keep the RNN at all?

So, they removed the RNN completely and built a model only from attention and a few simple pieces of math. That model is called the **[Transformer](https://outcomeschool.com/blog/decoding-transformer-architecture)**.

**A Transformer is a model that reads all the words of the input at the same time and uses attention to understand how they relate to each other.**

### What is inside a Transformer

A Transformer is made of blocks stacked on top of each other. Each block has two main parts:

- **Multi-Head Attention**: the words look at each other and gather information. This is the looking step.
- **[Feed-Forward Network](https://outcomeschool.com/blog/feed-forward-networks-in-llms)**: a simple layer of math that each word passes through on its own to process what it gathered. This is the thinking step.

We stack many such blocks. Early blocks learn simple things like grammar. Deeper blocks learn bigger things like meaning and reasoning. A small model has around 12 blocks. A large model has 100 or more.

Here is how the blocks are stacked:

```text
             Input words
                  |
                  v
   +-----------------------------+
   |  Block 1                    |
   |   Multi-Head Attention      |  <- looking step
   |   Feed-Forward Network      |  <- thinking step
   +-----------------------------+
                  |
                  v
   +-----------------------------+
   |  Block 2                    |
   |   Multi-Head Attention      |
   |   Feed-Forward Network      |
   +-----------------------------+
                  |
                  v
                . . .
                  |
                  v
   +-----------------------------+
   |  Block N                    |
   |   Multi-Head Attention      |
   |   Feed-Forward Network      |
   +-----------------------------+
                  |
                  v
        Predict the next word
```

Here, the words enter at the top, pass through every block one after another, and the last block predicts the next word. Every block does the same two steps: look, then think.

### The word order problem

There is one interesting problem. Since the Transformer reads all the words at once, it does not naturally know which word came first. "Dog bites man" and "Man bites dog" would look the same to it.

So, here comes the **Positional Encoding** to the rescue. Before the words enter the model, we add a small signal to each word that says its position: word 1, word 2, word 3, and so on. Now, the model knows the order.

The original Transformer used a fixed signal for this. Modern LLMs use newer ways to do the same job, like **[Rotary Position Embedding (RoPE)](https://outcomeschool.com/blog/math-behind-rope-rotary-position-embedding)**, which is used in LLaMA and many other models. The method changed, but the idea is the same: tell the model where each word sits.

### Encoder, Decoder, and Decoder-only

The original Transformer had two halves.

- **Encoder**: reads the input and understands it.
- **Decoder**: writes the output one word at a time, looking at what the encoder understood and at what it has already written.

This was built for translation. Read English, write French.

Later, researchers found that for generating text, we only need the decoder half. Give it some words, and it predicts the next word. Then add that word to the input, and predict the next. This is the **[Decoder-only Transformer](https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers)**, and it is the design used by GPT and almost every chat model today.

```text
 Encoder-Decoder (built for translation):
   "The cat sat"  --->  [ Encoder ]  --->  [ Decoder ]  --->  "Le chat s'est assis"
 Decoder-only (used by chat models):
   "The capital of India is"      --->  [ Decoder ]  --->  "New"
   "The capital of India is New"  --->  [ Decoder ]  --->  "Delhi"
```

Here, the decoder-only model has a single stream. The word it produces is added back to the input, and it predicts again. This loop continues till the answer is complete.

This loop is called autoregressive generation, and we have a detailed blog on [Autoregressive Models](https://outcomeschool.com/blog/autoregressive-models) that explains how it works.

### Why the Transformer won

The Transformer processes all the words in parallel. This matched perfectly with [GPUs](https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning), which are chips built to do thousands of small calculations at the same time. Training that took weeks on RNNs took days on Transformers.

```text
 RNN (one word per step):
   Step 1    Step 2    Step 3    Step 4    Step 5    Step 6
    The   ->  cat   ->  sat   ->  on    ->  the   ->  mat
 Transformer (all words in one step):
   Step 1
    The     cat     sat     on      the     mat
     |       |       |       |       |       |
     +-------+-------+-------+-------+-------+
                  all processed together
```

Here, the RNN needs 6 steps for 6 words, and each step must wait for the previous one to finish. The Transformer handles all 6 words in a single step, so all the GPU cores stay busy at the same time.

We have a detailed blog on [how RNNs and Transformers differ](https://outcomeschool.com/blog/how-do-rnns-and-transformers-differ) that covers this comparison end to end.

**Note:** This parallel reading applies to the input and to training. While writing the answer, the model still produces one word at a time, as we saw in the decoder-only loop above. Reading is parallel, writing is one by one. Keep this in mind, it will matter when we reach the KV Cache later.

And that speed opened the door to the next stage. If training is fast, why not train a bigger model on more data?

This was all about the Transformer. It solved slow training. Now, the next big question is: how big do we make it?

## Stage 4: Scaling

**Scaling means making the model bigger in three ways: more parameters, more training data, and more compute.**

Let's understand each.

- **Parameters**: the internal settings of the model. Let's say a model is a giant board with billions of tiny knobs. Training turns each knob a little to make the predictions better. The number of knobs is the number of parameters.
- **Data**: the text the model learns from. Books, websites, articles, code, and etc.
- **Compute**: the total amount of calculation done during training. More compute means more GPUs running for more time.

### The surprising discovery

Around 2020, researchers noticed something surprising. When they increased parameters, data, and compute together, the model got better in a smooth and predictable way. There was no sudden wall. Bigger kept getting better.

These are called **Scaling Laws**. They gave a formula that said: if we spend this much compute, the model will reach roughly this much quality.

Hence, models grew very fast.

- GPT-2 had about 1.5 billion parameters.
- GPT-3 had about 175 billion parameters, more than 100 times bigger, just one year later.

And GPT-3 did things that GPT-2 could not. It could write essays, answer questions, and even write code, that too without being trained for those specific tasks. These new abilities that appear only at a large size are called **emergent abilities**.

**Note:** Some researchers argue that these abilities do not appear suddenly. They grow smoothly with size and only look sudden because of how we measure them. The term is still widely used, so it is good to know it.

### Balancing data and size

Then came a correction. In 2022, a research paper called Chinchilla found that many big models were undertrained. They had too many parameters and too little data.

The lesson was simple: **for the best result, grow the data along with the parameters.** A smaller model trained on much more data can beat a bigger model trained on less data. This is why later models like LLaMA were trained on trillions of tokens.

### The cost problem

Scaling worked, but it created a new problem.

In a normal Transformer, every parameter is used for every single word. If a model has 175 billion parameters and we ask it a question of 100 words, all 175 billion parameters do work for each of those 100 words. This is called a **dense** model, because everything is active all the time.

```text
 Dense model:
   word 1    --->  all 175 billion parameters work  --->  output
   word 2    --->  all 175 billion parameters work  --->  output
   word 3    --->  all 175 billion parameters work  --->  output
    ...
   word 100  --->  all 175 billion parameters work  --->  output
```

Here, whether the word is a simple "the" or a difficult technical term, the full model works on it. There is no way to do less work for an easy word.

So, doubling the size of the model doubles the cost of every answer. Training became very costly, and running the model for millions of users became even more costly.

The issue with this approach is that every increase in size brings the same increase in running cost. Let's see how the next approach solve this issue.

## Stage 5: Mixture of Experts (MoE)

Here comes the **[Mixture of Experts (MoE)](https://outcomeschool.com/blog/mixture-of-experts)** to the rescue.

**Mixture of Experts is an architecture where the model is divided into many smaller parts called experts, and for each word, only a few experts are used.**

Let's decompose it.

**Mixture of Experts = Many Experts + A Router that picks a few of them**

Let's say we go to a big hospital. The hospital has a heart specialist, a bone specialist, a skin specialist, and an eye specialist. When we walk in, the receptionist listens to our problem and sends us to one or two relevant doctors. All four doctors do not examine every patient.

- The doctors are the **experts**.
- The receptionist is the **router**, also called the gate.
- Sending each patient to only a few doctors is called **sparse activation**.

### How MoE works inside the Transformer

Remember the Feed-Forward Network inside every Transformer block, the thinking step after attention? In an MoE model, that single feed-forward network is replaced by many feed-forward networks, the experts. A small router sits in front of them.

For every word:

- The router looks at the word and gives a score to each expert.
- It picks the top few experts, usually the top 1 or top 2.
- Only those experts process the word.
- Their outputs are combined and passed forward.

The attention part stays the same. Only the thinking step becomes a team of specialists.

Let's understand this with a picture:

```text
             Word comes in
                    |
                    v
 +--------------------------------------+
 |         Multi-Head Attention         |   same as before
 +--------------------------------------+
                    |
                    v
 +--------------------------------------+
 |                Router                |   gives a score to each expert
 +--------------------------------------+
   |    |    |    |    |    |    |    |
  0.4  0.1  0.3  0.0  0.1  0.0  0.1  0.0     scores
   |         |
   v         v
 [E1] [E2] [E3] [E4] [E5] [E6] [E7] [E8]     8 experts
  on   off  on   off  off  off  off  off     only the top 2 work
   |         |
   +----+----+
        |
        v
 Combine the two outputs and pass forward
```

Here, the router gave the highest scores to Expert 1 and Expert 3, so only those two do the work for this word. The other six sit idle for this word. For the next word, the router can pick a different pair.

### Total parameters vs active parameters

This is the key idea, so let's take numbers.

Suppose we start with a model of about 7 billion parameters and, in each block, replace its single Feed-Forward Network (the thinking step) with 8 expert Feed-Forward Networks. This is the basic design of Mixtral 8x7B. The name means 8 experts built on the architecture of a 7 billion base model. The model does not become 8 x 7 = 56 billion, because the attention part and the other shared pieces are not copied. Only the Feed-Forward Network is copied 8 times. Together with the shared parts, the model has about 47 billion parameters in total.

**Note:** The numbers here are rounded for the sake of understanding.

Now, for each word, the router picks only 2 of the 8 experts. So, the work done for each word uses about 13 billion parameters.

- **Total parameters**: about 47 billion. This is the knowledge the model holds.
- **Active parameters**: about 13 billion. This is the work done per word.

```text
 Total parameters (what the model knows):
   [ shared parts ] [E1] [E2] [E3] [E4] [E5] [E6] [E7] [E8]   = about 47 billion
 Active parameters (what works for one word):
   [ shared parts ] [E1]      [E3]                            = about 13 billion
```

Here, all 8 experts live inside the model, but for any one word, only 2 of them wake up along with the shared parts.

Means, the model has the knowledge of a 47 billion model but a running cost close to that of a 13 billion model. It is not exactly equal, because the router and the shared parts also do some work, but it is far cheaper than running all 47 billion. That's the beauty of MoE.

This way we can use MoE to solve the interesting problem of cost without giving up knowledge.

Bigger models like DeepSeek-V3 push this much further. It has about 671 billion total parameters, but only about 37 billion are active for each word.

### What each expert learns

One more thing to notice: we do not tell the experts what to specialize in. During training, the router and the experts learn together. Some experts end up handling punctuation, some handle numbers, some handle parts of code, and some handle a particular kind of word. The split is not always clean, but it happens on its own.

### The problems with MoE

MoE is not free. It has its own issues.

- **Memory**: even though only 2 experts work per word, all 8 must be loaded in memory, because the next word can go to a different pair. So, MoE saves compute but not memory.
- **Load balancing**: if the router keeps sending everything to the same two experts, the other experts never learn. So, we add a small extra rule during training that pushes the router to spread the work. Without this, MoE fails.
- **Training complexity**: routing decisions make training less stable and harder to get right.

Still, MoE is the reason we can have models with hundreds of billions of parameters that respond in reasonable time. Most of the biggest models today use MoE in some form.

This was all about Mixture of Experts. It solved the cost of the thinking step. But the attention step has its own cost, and that brings us to what is happening now.

## Stage 6: New Directions

Researchers are now working in a few directions at the same time. Let's look at the important ones.

### The long context problem

The text we give to the model at one time is called the **context**. Today, we want to give it whole books, long conversations, and big codebases. That creates a problem.

Attention compares every word with every other word. If the input has 1,000 words, that is 1,000 x 1,000 = 1 million comparisons. If the input has 100,000 words, that is 10 billion comparisons. Doubling the input makes these comparisons four times costlier.

```text
 4 words  ->  4 x 4 = 16 comparisons
          The   cat   sat   on
   The     x     x     x     x
   cat     x     x     x     x
   sat     x     x     x     x
   on      x     x     x     x
 8 words  ->  8 x 8 = 64 comparisons   (2 times the words, 4 times the cost)
```

Here, every row is a word looking at every column. Adding one word adds a full new row and a full new column, so the grid grows much faster than the input.

Also, while generating the answer, the model stores the keys and values of every earlier word so that it does not calculate them again. This storage is called the **[KV Cache](https://outcomeschool.com/blog/kv-cache-in-llms)**. For long inputs, the KV Cache becomes huge and eats up memory.

A few designs came to fix this:

- **[Grouped Query Attention (GQA)](https://outcomeschool.com/blog/grouped-query-attention)**: many attention heads share the same keys and values instead of each head having its own. This shrinks the KV Cache a lot with very less loss in quality. Used in LLaMA 3 and many other models.
- **[Multi-Head Latent Attention (MLA)](https://outcomeschool.com/blog/kv-cache-compression)**: compresses the keys and values into a small form before storing them, and expands them back when needed. Used in DeepSeek models.
- **[Sliding Window Attention](https://outcomeschool.com/blog/how-does-sliding-window-attention-work)**: each word looks only at a fixed window of nearby words instead of everything. Information still travels far by passing through many blocks. Used in Mistral.

Let's see each of them with a picture. First, GQA:

```text
 Multi-Head Attention:                Grouped Query Attention:
   Head 1 -> own Key + Value            Head 1 --+
   Head 2 -> own Key + Value            Head 2 --+--> shared Key + Value (group A)
   Head 3 -> own Key + Value            Head 3 --+
   Head 4 -> own Key + Value            Head 4 --+
   Head 5 -> own Key + Value            Head 5 --+
   Head 6 -> own Key + Value            Head 6 --+--> shared Key + Value (group B)
   Head 7 -> own Key + Value            Head 7 --+
   Head 8 -> own Key + Value            Head 8 --+
   8 sets stored in the KV Cache        2 sets stored in the KV Cache
```

Here, the heads are divided into groups, and all the heads in one group share one set of keys and values. With 8 heads in 2 groups, the KV Cache becomes four times smaller. Each head still asks its own query, so the quality stays almost the same.

Now, let's see MLA:

```text
 Normal attention:
   Key + Value (big)  ------------------------------->  stored in KV Cache (big)
 Multi-Head Latent Attention:
   Key + Value (big)  --> compress -->  small form  -->  stored in KV Cache (small)
                                             |
                                             v
                          expand back to full size only when needed
```

Here, instead of storing the big keys and values, MLA stores a small compressed form. When the model needs them, it expands the small form back. So, the KV Cache holds much less, and the model still gets the full information when it looks back.

Finally, let's see Sliding Window Attention:

```text
 Full attention:
   w1   w2   w3   w4   w5   w6   w7   w8
    ^    ^    ^    ^    ^    ^    ^    |
    +----+----+----+----+----+----+----+
          w8 looks at all 7 earlier words
 Sliding Window Attention (window = 3):
   w1   w2   w3   w4   w5   w6   w7   w8
                        ^    ^    ^    |
                        +----+----+----+
          w8 looks only at the 3 nearest words
 How information still travels far:
   Block 1:  w5 gathers from w2, w3, w4
   Block 2:  w8 gathers from w5, w6, w7, and w5 already carries w2, w3, w4
```

Here, in Block 1, w5 has already gathered information from w2, w3, and w4. In Block 2, when w8 looks at w5, it indirectly gets that information too. So, even with a small window, information from far away still reaches, one block at a time.

Because of these ideas, models moved from reading about 2,000 tokens at a time to reading a million tokens at a time.

### A new kind of memory: State Space Models

Some researchers went back to the idea of reading one word at a time, but with a much smarter memory. These are called **State Space Models**, and the popular one is **Mamba**.

In simple words, Mamba keeps a running memory like an RNN, so its cost grows in a straight line with the input length instead of squaring. But unlike the old RNN, it looks at each incoming word and decides what to keep and what to throw away from memory. So, important information from far back survives much better than it did in the old RNN.

Here is a rough picture of how the cost grows. The numbers are only for comparison, not real measurements:

```text
 Input length:      1,000     2,000     4,000     8,000  words
 Attention cost:    1 unit    4 units   16 units  64 units   (squares)
 Mamba cost:        1 unit    2 units   4 units   8 units    (straight line)
```

Here, every time the input doubles, the attention cost becomes 4 times, but the Mamba cost only becomes 2 times. For very long inputs, this difference becomes huge.

Today, we also see **hybrid** models that mix a few attention blocks with many Mamba blocks, in order to get the accuracy of attention with the speed of Mamba.

### One model for text, images, and audio

Early LLMs read only text. Now, the same Transformer design is being used for images, audio, and video. An image is [cut into small patches](https://outcomeschool.com/blog/decoding-vision-transformer-vit), each patch is turned into a token just like a word, and the same attention handles it. Audio and video are handled in a similar way. These are called **[multimodal](https://outcomeschool.com/blog/multimodal-ai)** models.

### Thinking longer instead of growing bigger

For years, the way to a smarter model was a bigger model. Now, there is a second way. Let the model think for longer before answering.

[Reasoning models](https://outcomeschool.com/blog/large-reasoning-models) generate a long chain of thinking steps before giving the final answer. In those steps, they often try different paths and check their own work. This is called scaling at **inference time**. Inference is just the word for the time when the model is answering. Means, we spend more compute when answering instead of only when training.

So, the scaling story now has two directions: scale the training, and scale the thinking.

## Summary of the evolution

Here is the whole journey in one picture:

```text
 RNN  --->  Attention  --->  Transformer  --->  Scaling  --->  MoE  --->  New Directions
 forgets    fixes            removes the        makes the      cuts the   long context,
 and slow   forgetting       slow RNN           model smart    cost       Mamba, reasoning
```

Here, every arrow is a problem being solved. Each stage kept what worked in the previous stage and fixed the biggest thing that did not.

Let me tabulate the whole journey for your better understanding.

| Stage | Key idea | Problem it solved | Problem it left behind |
| --- | --- | --- | --- |
| RNN | Read one word at a time with a single memory | Could read text of any length | Forgot early words, slow to train |
| Attention | Look at every earlier word with weights | Forgetting | Still slow with RNN underneath |
| Transformer | Only attention, all words in parallel | Slow training | How big to make it |
| Scaling | More parameters, data, and compute | Model quality | Cost grows with size |
| Mixture of Experts | Use only a few experts per word | Running cost of large models | Memory, load balancing |
| New Directions | GQA, MLA, Mamba, multimodal, reasoning | Long context, new inputs, smarter answers | Still evolving |

Here, we can see the pattern clearly. Every stage kept the good part of the previous stage and fixed its biggest problem.

- Attention kept the idea of reading text and fixed forgetting.
- Transformer kept attention and removed the slow part.
- Scaling kept the Transformer and made it bigger.
- MoE kept the size and cut the cost.
- The newer ideas keep all of it and push further, giving us longer context, new kinds of input, and smarter answers.

Now we must have understood the evolution of LLM architecture, from attention to scaling to Mixture of Experts and beyond. The next time we hear about a new model, we can ask a simple question: which problem from this timeline is it trying to solve?

## Frequently Asked Questions

### Does a Mixture of Experts model use less memory than a dense model?

No. MoE saves compute but not memory. Even though only a few experts work for each word, all the experts must be loaded in memory, because the next word can go to a different pair. So the running cost per word drops, but the full model still has to sit in memory.

### Is Mixtral 8x7B a 56 billion parameter model?

No. Mixtral 8x7B has about 47 billion parameters in total, not 56 billion. Only the Feed-Forward Network is copied 8 times, while the attention part and the other shared pieces are not copied. For each word, only 2 of the 8 experts are used, so about 13 billion parameters are active.

### Is a bigger model always better than a smaller one?

No. The Chinchilla paper found that many big models were undertrained, with too many parameters and too little data. A smaller model trained on much more data can beat a bigger model trained on less data. So, for the best result, we should grow the data along with the parameters.

### Does a Transformer write the whole answer in parallel?

No. The Transformer reads the input in parallel, and training is parallel too. But while writing the answer, the model still produces one word at a time. Each new word is added back to the input, and the model predicts again until the answer is complete.

### Is Mamba just an RNN?

No. Mamba keeps a running memory like an RNN, so its cost grows in a straight line with the input length. But unlike the old RNN, it looks at each incoming word and decides what to keep and what to throw away. So important information from far back survives much better.
