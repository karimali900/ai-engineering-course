---
title: Encoder vs Decoder in Transformers
module: 3
module_title: Generative AI and the Transformer Architecture
lesson: '3.8'
source: https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers
published: August 6, 2026
tags:
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 2018
reading_time: 10
status: full
---
# Encoder vs Decoder in Transformers

> **Module 3 · Lesson 3.8**  
> Source: [Outcome School](https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers) · Published: August 6, 2026 · Reading time: ~10 min · Tags: `llm`, `ai`, `machine-learning`

---

![Encoder vs Decoder in Transformers](../../assets/images/03-03-08-encoder-vs-decoder-in-transformers/encoder-vs-decoder-in-transformers.png)

In Transformers, the Encoder reads the whole input at once, in both directions, to understand it. The Decoder generates the output one token at a time, and it can look only backward.

In this blog, we will learn about Encoder vs Decoder in Transformers, the two building blocks behind almost every modern AI model that works with language. We will also see how the Encoder and the Decoder differ from each other, how each one works with simple examples, why one of them reads in both directions while the other one looks only backward, what the three types of Transformers are, and when to use which one.

We will cover the following:

- What is a Transformer?
- A word about tokens
- What is an Encoder?
- What is a Decoder?
- The one big difference
- The three types of Transformers
- Let's tabulate the difference
- When to use which one?
- Summary

Let's get started.

## What is a Transformer?

Before jumping into Encoder and Decoder, we must know what a Transformer is.

**A Transformer is the architecture behind most modern AI models that work with language.** The AI tools we use today, like ChatGPT, Claude, and Gemini, are all built using the [Transformer architecture](https://outcomeschool.com/blog/decoding-transformer-architecture).

The Transformer became famous because it is very good at understanding the relationship between words. It can look at a sentence and figure out how each word connects to the other words. This is what makes it so powerful with language.

Now, a Transformer is built from two main building blocks. One block is called the Encoder, and the other block is called the Decoder. In this blog, we will understand both of them and see how they differ.

Before that, we need to understand one small word, the token.

## A word about tokens

When a Transformer reads text, it does not read whole sentences at once. It breaks the text into small pieces. Each small piece is called a token.

A token is usually a word or a part of a word. For the sake of understanding, we can just think of a token as a word.

So, the sentence "I love AI" becomes three tokens: "I", "love", and "AI". The Transformer works on these tokens.

The exact rule for splitting the text into tokens comes from a [tokenization](https://outcomeschool.com/blog/tokenization-in-llms) algorithm. We have a detailed blog on [Byte Pair Encoding in LLMs](https://outcomeschool.com/blog/bpe-in-llms) that explains how this works.

Now that we know about tokens, let's understand the Encoder.

## What is an Encoder?

**The Encoder reads the whole input and builds a deep understanding of it.**

In simple words, the job of the Encoder is to understand. It takes all the tokens of the input, looks at them together, and creates a rich meaning for each token.

Here is the most important point about the Encoder. It can look at all the tokens at the same time, both to the left and to the right of any word. It reads the whole sentence at once. This is why we say the Encoder looks in both directions.

Let's understand why both directions matter. Consider the sentence, "The bank of the river was muddy." Here, the word "bank" is confusing. It could mean a money bank or the side of a river. To understand it correctly, we must read the word "river" that comes later. The Encoder can do this, because it reads the full sentence at once and looks in both directions.

We can picture the Encoder like below:

```
   Input tokens:   [The]  [bank]  [of]  [the]  [river]  [was]  [muddy]
                     Every token looks at ALL other tokens
                      (both left and right, all at once)
                                    |
                                    v
   Output:   a deep understanding (meaning) for each token
```

Here, we can see that each token is allowed to look at every other token in the sentence. This looking at each other is done by a mechanism called [Self Attention](https://outcomeschool.com/blog/self-attention-in-transformers). Because of this, the Encoder understands the full meaning very well.

So, the Encoder is like a careful reader. It reads the whole thing first and understands it deeply. It does not write anything new. It only understands.

## What is a Decoder?

Now that we have learned about the Encoder, it's time to learn about the Decoder.

**The Decoder generates the output, one token at a time.**

In simple words, the job of the Decoder is to write. It produces the answer token by token, from left to right, just like we write a sentence word by word.

Here is the most important point about the Decoder. While writing, it can only look at the tokens that came before. It cannot look at the future tokens, because those tokens are not written yet. This makes sense. When we write a sentence, we do not know the next word until we write it. Inside the model, this is enforced by a [causal mask](https://outcomeschool.com/blog/causal-masking-in-attention) that hides the future tokens.

Let's understand this with an example. Suppose the Decoder is writing "The sky is blue". When it is about to write "blue", it can look at "The", "sky", and "is". But it cannot look at "blue" itself, because that is the word it is trying to guess right now.

We can picture the Decoder like below:

```
   Step 1:  <start>                 ->  predict next  ->  "The"
   Step 2:  <start> The             ->  predict next  ->  "sky"
   Step 3:  <start> The sky         ->  predict next  ->  "is"
   Step 4:  <start> The sky is      ->  predict next  ->  "blue"
   (each step can only look back at the words already written)
```

Here, we can see that the Decoder builds the sentence one word at a time, always looking only at the words behind it.

So, the Decoder is like a writer. It creates new text step by step, using only what it has written so far. This way of generating, where each new token depends on the tokens that came before it, is what makes it an [autoregressive model](https://outcomeschool.com/blog/autoregressive-models).

## The one big difference

If we forget everything else, we must remember this one line.

> The Encoder reads and understands the whole input at once. The Decoder writes new output one token at a time, looking only at the past.

That is the heart of the difference. The Encoder is a reader that looks in both directions. The Decoder is a writer that looks only backward.

## The three types of Transformers

Now, here is something interesting. We can build a Transformer using only the Encoder, only the Decoder, or both together. This gives us three types of Transformers, and each one is good for a different job.

Let's understand all three.

**1. Encoder-only:** This uses only the Encoder. Its job is pure understanding. It is great for tasks like deciding if a review is positive or negative, or turning text into [embeddings](https://outcomeschool.com/blog/what-are-embeddings) for search. A famous example is a model called BERT.

**2. Decoder-only:** This uses only the Decoder. Its job is pure generation. It writes text one token at a time. [Most modern chat AI models are decoder-only](https://outcomeschool.com/blog/evolution-of-llm-architecture), like the models behind ChatGPT, Claude, and Gemini.

**3. Encoder-Decoder:** This uses both blocks together. The Encoder first reads and understands the input. Then the Decoder writes the output based on that understanding. This is great for tasks where we take one full text and turn it into another, like translating a sentence from English to French. A famous example is a model called T5.

We can picture the three types like below:

```
   Encoder-only        Decoder-only        Encoder-Decoder
   ------------        ------------        ---------------
   Encoder             Decoder             Encoder + Decoder
       |                   |                   |
       v                   v                   v
   understand          generate            understand, then
   the input           the output          generate
       |                   |                   |
       v                   v                   v
   (BERT)              (ChatGPT)           (T5)
```

Here, we can see the three types at a glance. The Encoder-only type only understands. The Decoder-only type only generates. The Encoder-Decoder type first understands and then generates.

That pure understanding is what makes the Encoder-only type a great fit for search. We have a detailed blog on [Decoding ColBERT](https://outcomeschool.com/blog/decoding-colbert) that explains how a BERT encoder is turned into a fast, word-level retrieval model.

Let's understand the Encoder-Decoder flow with a translation example like below:

```
   English input: "I love AI"
          |
          v
   +---------------+
   |    Encoder    |   reads and understands the full English sentence
   +---------------+
          |
          |  passes the understanding to the Decoder
          v
   +---------------+
   |    Decoder    |   writes the French output, one token at a time
   +---------------+
          |
          v
   French output: "J'aime l'IA"
```

Here, we can see the teamwork. The Encoder understands the English sentence fully. Then the Decoder uses that understanding to write the French sentence step by step. The bridge that carries this understanding from the Encoder into the Decoder is [Cross Attention](https://outcomeschool.com/blog/cross-attention-in-transformers).

## Let's tabulate the difference

Let me tabulate the differences between the Encoder and the Decoder for your better understanding.

| Point | Encoder | Decoder |
| --- | --- | --- |
| Main job | Understand the input | Generate the output |
| How it reads | Looks at all tokens at once | Writes one token at a time |
| Direction | Both directions (left and right) | Only backward (past tokens) |
| Good for | Understanding tasks | Writing tasks |
| Example model | BERT | The models behind ChatGPT, Claude |

## When to use which one?

This is the real question. Let's make it very simple.

The trick is to look at the task we want to solve.

- If our task is to understand text, like sorting reviews or searching, we use an Encoder-only model.
- If our task is to generate text, like chatting or writing, we use a Decoder-only model.
- If our task is to take one full text and turn it into another, like translation or summarization, we use an Encoder-Decoder model.

So, we must always ask ourselves: do we want to understand, to generate, or to convert one text into another? The answer decides which one to use.

**Note:** Today, most popular chat AI models are decoder-only. This is because a good writer must also understand well, and it turns out that a large Decoder learns to do both understanding and writing at the same time. This is why decoder-only models power most of the AI chat tools we use today.

## Summary

Let's quickly recap what we have learned.

- A Transformer is the architecture behind most modern language AI, and it is built from two blocks: the Encoder and the Decoder.
- The Encoder reads the whole input at once and understands it deeply, looking in both directions.
- The Decoder writes the output one token at a time, looking only at the past tokens.
- We can build three types: Encoder-only for understanding, Decoder-only for generation, and Encoder-Decoder for converting one text into another.
- Most modern chat AI models today are decoder-only.

This is how the Encoder and the Decoder work as the two building blocks of a Transformer.

Now, we must have understood Encoder vs Decoder in Transformers.

## Frequently Asked Questions

### Is ChatGPT an encoder model or a decoder model?

ChatGPT is built on a decoder-only model. Most modern chat AI models, like the models behind ChatGPT, Claude, and Gemini, are decoder-only. Their job is pure generation, writing text one token at a time while looking only at the tokens that came before.

### Why are most chat models decoder-only if they also need to understand text?

A good writer must also understand well, and a large Decoder learns to do both understanding and writing at the same time. This is why decoder-only models power most of the AI chat tools we use today.

### Can BERT be used to generate text like ChatGPT?

No. BERT is an Encoder-only model, and its job is pure understanding. It does not write anything new. It is great for tasks like deciding if a review is positive or negative, or turning text into embeddings for search.

### How does the Decoder use what the Encoder understood?

The Decoder uses Cross Attention. In an Encoder-Decoder model, the Encoder first reads and understands the full input. Cross Attention is the bridge that carries this understanding into the Decoder, which then writes the output one token at a time, like a French translation of an English sentence.
