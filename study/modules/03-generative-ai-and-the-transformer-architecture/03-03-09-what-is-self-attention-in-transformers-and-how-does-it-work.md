---
title: What is Self Attention in Transformers and How Does It Work?
module: 3
module_title: Generative AI and the Transformer Architecture
lesson: '3.9'
source: https://outcomeschool.com/blog/self-attention-in-transformers
published: May 29, 2026
tags:
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 2562
reading_time: 13
status: full
---
# What is Self Attention in Transformers and How Does It Work?

> **Module 3 · Lesson 3.9**  
> Source: [Outcome School](https://outcomeschool.com/blog/self-attention-in-transformers) · Published: May 29, 2026 · Reading time: ~13 min · Tags: `llm`, `ai`, `machine-learning`

---

![Self Attention in Transformers](../../assets/images/03-03-09-what-is-self-attention-in-transformers-and-how-does-it-work/self-attention-in-transformers.png)

Self Attention is the mechanism that lets every word in a sentence look at every other word in the same sentence to understand its meaning. It is the heart of modern Large Language Models like BERT and GPT.

In this blog, we will learn about Self Attention in Transformers. We will also see why we need it, what Query, Key, and Value are, how it works step by step with a simple example, and why it works so well.

We will cover the following:

- What is Self Attention?
- Why do we need Self Attention?
- Query, Key, and Value vectors
- Step-by-step working of Self Attention
- A simple example walk-through
- Why Self Attention works so well
- Multi-Head Self Attention
- Where Self Attention is used

Let's get started.

### What is Self Attention?

**Self Attention is a mechanism that allows every token in a sequence to look at every other token in the same sequence, including itself, to understand the context.**

In simple words, **Self Attention = Self + Attention**. The word "Attention" means each token decides how much it should focus on the other tokens.

So, every word in a sentence looks at every other word in the same sentence and figures out which words matter the most for its meaning.

### Why do we need Self Attention?

The best way to learn this is by taking an example.

Consider the sentence:

> The animal did not cross the street because it was too tired.

Now, the question is: what does the word `it` refer to?

As humans, we know that `it` refers to `the animal`, because the animal was too tired to cross.

Now, let's read one more sentence:

> The animal did not cross the street because it was too wide.

Same structure. Same word `it`. But now, what does `it` refer to?

Here, `it` refers to `the street`, because the street was too wide.

We changed just one word - from `tired` to `wide` - and the meaning of `it` completely changed.

So, how did our brain figure that out? Our brain looked at the surrounding words to understand the meaning of `it`. The word `tired` pulled our attention towards `the animal`. The word `wide` pulled our attention towards `the street`.

This is exactly what happens inside the Large Language Model. Every word looks at every other word in the same sentence to understand its meaning. The model gives more attention to the words that matter and less attention to the words that do not matter. This mechanism is called **Attention**.

Now, notice that every word here is looking at the other words within the SAME sentence. The sentence is attending to itself. This is why we call it **Self Attention**.

In the first sentence, `it` pays strong attention to `animal`. In the second sentence, `it` pays strong attention to `street`. That is how the model captures the true meaning of `it` in both cases.

Without Self Attention, the word `it` would just be a generic token with no real meaning. And Self Attention is the core idea behind every modern Large Language Model.

### Query, Key, and Value vectors

For every token, Self Attention needs to answer two questions:

- Which other tokens in this sentence are important for me?
- How much should I focus on each of them?

To answer these questions, we create three vectors for every input token:

- **Query (Q):** what this token is looking for.
- **Key (K):** what this token offers to others.
- **Value (V):** the actual information this token carries.

The word "Self" in Self Attention comes from one very important fact:

> Query, Key, and Value all come from the SAME input sequence.

This is what makes it "Self" Attention. The same sequence creates the questions, the same sequence creates the keys to match those questions, and the same sequence provides the values. The sequence is attending to itself.

In simple words, if our input sentence is "The animal did not cross the street", then Q, K, and V are all derived from "The animal did not cross the street" itself.

We have a detailed blog on the [Math behind Attention - Q, K, and V](https://outcomeschool.com/blog/math-behind-attention-qkv) that covers this in depth.

**Note:** This is the key difference between Self Attention and [Cross Attention](https://outcomeschool.com/blog/cross-attention-in-transformers). In Cross Attention, the Query comes from one sequence and the Key and Value come from another sequence. But in Self Attention, all three come from the same sequence.

For the sake of understanding, let's take an analogy.

Suppose we are in a library and we are looking for a book on machine learning.

- The **Query** is the topic we are searching for: "machine learning".
- The **Key** is the label written on every book on the shelf.
- The **Value** is the actual content inside the book.

We compare our Query with every Key. The Keys that match our Query give us the most relevant Values.

Self Attention works in the same way.

### Step-by-step working of Self Attention

Now, it's time to learn the exact steps of Self Attention.

**Step 1:** We start with the input embeddings. Every token in the sentence is converted into a vector.

**Step 2:** We create three vectors for every token by multiplying the embedding with three different weight matrices.

- Q = Input x W\_Q
- K = Input x W\_K
- V = Input x W\_V

Here, `W_Q`, `W_K`, and `W_V` are weight matrices that the model learns during training.

**Step 3:** We compute the dot product of `Q` with the transpose of `K`. This is a [matrix multiplication](https://outcomeschool.com/blog/matrix-multiplication-in-neural-networks) that gives us the attention scores. We use the transpose so that the shapes align correctly for the multiplication.

- Scores = Q . K^T

The score tells us how much one token should attend to another token. A higher score means a stronger match between the Query of one token and the Key of another token.

**Step 4:** We scale the scores by dividing them by the square root of the dimension of the Key vectors. Here, `d_k` is the dimension of the Key vector.

- Scaled Scores = (Q . K^T) / sqrt(d\_k)

This scaling is done to keep the numbers in a stable range so that the softmax does not produce extreme values. Without this scaling, the gradients can become very small during training. We have a detailed blog on the [Math behind √dₖ Scaling Factor in Attention](https://outcomeschool.com/blog/scaling-dot-product-attention) that explains this step by step.

**Step 5:** We apply softmax on the scaled scores. This converts the scores into probabilities. Every row of the matrix now sums to 1.

- Attention Weights = softmax((Q . K^T) / sqrt(d\_k))

These weights tell us, for every token, how much attention it should pay to every other token.

**Step 6:** We multiply the attention weights by the Value matrix `V`. This gives us the final output.

- Output = Attention Weights . V

The output is a new representation of every token where the meaning of the token is enriched by the context of the other tokens.

So, the full Self Attention formula is:

**Attention(Q, K, V) = softmax((Q . K^T) / sqrt(d\_k)) . V**

Here, we can visualize the full flow of Self Attention as below:

```
        Input Embeddings
               |
               ↓
   +-----------+-----------+
   |           |           |
   ↓           ↓           ↓
   Q           K           V
   |           |           |
   +-----+-----+           |
         |                 |
         ↓                 |
       Q . K^T             |
         |                 |
         ↓                 |
   Divide by sqrt(d_k)     |
         |                 |
         ↓                 |
       Softmax             |
         |                 |
         ↓                 |
   Attention Weights       |
         |                 |
         +--------+--------+
                  |
                  ↓
              Multiply
                  |
                  ↓
               Output
```

Here, we can see that Q, K, and V are all created from the same input. Then Q and K are used to compute the attention weights, and V is used to compute the final output.

### A simple example walk-through

Let's take a small example to make this concrete.

Consider the sentence:

> I love AI

We have three tokens: `I`, `love`, `AI`.

**Step 1:** Every token is converted into an embedding vector.

**Step 2:** We create Q, K, and V vectors for every token using the learned weight matrices. So now, we have:

- Q for `I`, Q for `love`, Q for `AI`
- K for `I`, K for `love`, K for `AI`
- V for `I`, V for `love`, V for `AI`

**Step 3:** For the token `I`, we take its Query vector and compute the dot product with the Key vectors of all three tokens: `I`, `love`, and `AI`. This gives us three scores.

**Step 4:** We scale these scores by `sqrt(d_k)`.

**Step 5:** We apply softmax to get the attention weights. Just for the sake of understanding, let's say the result for the token `I` is:

- Weight for `I` = 0.070
- Weight for `love` = 0.707
- Weight for `AI` = 0.223

This means the token `I` is paying 7% attention to itself, 70.7% to `love`, and 22.3% to `AI`.

The same calculation happens for every token. So, the full attention weight matrix looks like below:

```
                  Attends to
                 I     love    AI
            +-------+-------+-------+
         I  | 0.070 | 0.707 | 0.223 |
            +-------+-------+-------+
From   love | 0.333 | 0.333 | 0.333 |
            +-------+-------+-------+
         AI | 0.168 | 0.533 | 0.299 |
            +-------+-------+-------+
```

Here, every row sums to 1 because of softmax. The numbers are just for the sake of understanding. Each row tells us how much attention that token is paying to every other token in the sentence. Because every row must sum to 1, a token has to give its attention away even when nothing is worth attending to, which is why the first tokens end up acting as [attention sinks](https://outcomeschool.com/blog/how-do-attention-sinks-work).

**Step 6:** We compute the final output for `I` as a weighted sum of the Value vectors:

- Output for `I` = 0.070 x V(`I`) + 0.707 x V(`love`) + 0.223 x V(`AI`)

This output is the new representation of `I` that carries the context of the entire sentence. Since `love` got the highest weight, the new representation of `I` is heavily influenced by the meaning of `love`.

The same process happens for every other token at the same time. So, in one shot, we get the new context-aware representation of every token in the sentence.

It works perfectly.

### Why Self Attention works so well

Now, let's understand why Self Attention works so well.

Before Self Attention, models like [RNN](https://outcomeschool.com/blog/recurrent-neural-network) and LSTM [processed tokens one by one in a sequence](https://outcomeschool.com/blog/how-do-rnns-and-transformers-differ). This was slow and the connection between far-apart words became weak. [Self Attention solved both of these problems](https://outcomeschool.com/blog/evolution-of-llm-architecture).

- **Parallelization:** All tokens are processed at the same time. We do not have to wait for one token to finish before processing the next. This makes training very fast on GPUs.
- **Long-range dependencies:** Every token can directly look at every other token, even if they are very far apart in the sentence. There is no decay over distance. The price of this is cost, which is why long-context models often switch to [Sliding Window Attention](https://outcomeschool.com/blog/how-does-sliding-window-attention-work), where every token looks only at its nearby tokens.
- **Contextual understanding:** Every token gets a richer meaning based on the surrounding words. The same word can have a different representation in different sentences depending on the context.
- **Flexibility:** Self Attention does not care about the order of computation. It can handle long sequences and capture complex relationships.

That's the beauty of Self Attention.

### Multi-Head Self Attention

Now, let's briefly learn about [Multi-Head Self Attention](https://outcomeschool.com/blog/multi-head-attention-in-transformers).

In Self Attention, we have only one set of Q, K, and V. But one set is not enough to capture all the different types of relationships in a sentence.

So, here comes Multi-Head Self Attention into the picture.

In Multi-Head Self Attention, we run Self Attention multiple times in parallel, each with its own set of `W_Q`, `W_K`, and `W_V`. Every parallel run is called a "head". Each head learns to focus on a different aspect of the sentence.

For example:

- One head may focus on the subject-object relationship.
- Another head may focus on the verb tense.
- Another head may focus on long-range word dependencies.

After all the heads have done their work, we concatenate their outputs and pass them through one more linear layer. This gives us the final output of Multi-Head Self Attention.

We can visualize Multi-Head Self Attention as below:

```
                  Input
                    |
   +--------+-------+-------+--------+
   |        |               |        |
   ↓        ↓               ↓        ↓
 Head 1   Head 2    ...   Head N-1  Head N
   |        |               |        |
   ↓        ↓               ↓        ↓
 Output1  Output2          OutputN-1 OutputN
   |        |               |        |
   +--------+-------+-------+--------+
                    |
                    ↓
              Concatenate
                    |
                    ↓
               Linear Layer
                    |
                    ↓
              Final Output
```

Here, every head runs Self Attention in parallel with its own `W_Q`, `W_K`, and `W_V`. Their outputs are joined together and passed through a linear layer to produce the final output.

So, **Multi-Head Self Attention = many Self Attentions running in parallel**.

This way, the model captures many different types of relationships in the same sentence at the same time.

### Where Self Attention is used

Now, let's see where Self Attention is used.

- **Encoder of Transformers:** Self Attention is the core building block of [the encoder](https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers). Every encoder layer uses Self Attention so that every input token can look at every other input token.
- **Decoder of Transformers (Masked Self Attention):** The decoder also uses Self Attention, but with a small change. The decoder generates one token at a time, and a token must not look at future tokens. So, we use [Masked Self Attention](https://outcomeschool.com/blog/causal-masking-in-attention), where the future tokens are hidden using a mask. Every token can look at itself and the tokens before it, but not the tokens after it.

Self Attention is the reason why models like BERT, GPT, and many other modern Large Language Models work so well. Without Self Attention, the [Transformer architecture](https://outcomeschool.com/blog/decoding-transformer-architecture) would not exist as we know it today.

This was all about Self Attention in Transformers.

Now we must have understood what Self Attention is, how it works step by step, and why it works so well.

## Frequently Asked Questions

### What is the difference between Self Attention and Cross Attention?

In Self Attention, the Query, Key, and Value all come from the same input sequence. In Cross Attention, the Query comes from one sequence and the Key and Value come from another sequence. This is why Self Attention is described as a sequence attending to itself.

### Does Self Attention process tokens one by one like an RNN?

No. Self Attention processes all tokens at the same time, so we do not wait for one token to finish before processing the next. RNN and LSTM processed tokens one by one, which was slow. Parallel processing makes training very fast on GPUs.

### Does a token pay attention to itself in Self Attention?

Yes. Every token looks at every other token in the same sequence, including itself. For example, in the sentence "I love AI", the token `I` can pay some attention to itself along with `love` and `AI`, and the weights for each row sum to 1.

### Why does the decoder use Masked Self Attention?

The decoder generates one token at a time, and a token must not look at future tokens. So, a mask hides the future tokens. Every token can look at itself and the tokens before it, but not the tokens after it.

### Are the Q, K, and V weight matrices fixed?

No. The weight matrices `W_Q`, `W_K`, and `W_V` are learned by the model during training. We multiply each input embedding by these three matrices to create the Query, Key, and Value vectors for every token.
