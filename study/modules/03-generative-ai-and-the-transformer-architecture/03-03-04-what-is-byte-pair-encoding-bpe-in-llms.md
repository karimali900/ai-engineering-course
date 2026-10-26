---
title: What is Byte Pair Encoding (BPE) in LLMs?
module: 3
module_title: Generative AI and the Transformer Architecture
lesson: '3.4'
source: https://outcomeschool.com/blog/bpe-in-llms
published: March 31, 2026
tags:
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 2125
reading_time: 11
status: full
---
# What is Byte Pair Encoding (BPE) in LLMs?

> **Module 3 · Lesson 3.4**  
> Source: [Outcome School](https://outcomeschool.com/blog/bpe-in-llms) · Published: March 31, 2026 · Reading time: ~11 min · Tags: `llm`, `ai`, `machine-learning`

---

![Byte Pair Encoding in LLMs](../../assets/images/03-03-04-what-is-byte-pair-encoding-bpe-in-llms/bpe-in-llms.png)

BPE (Byte Pair Encoding) is the tokenization algorithm used by most modern Large Language Models (LLMs). It starts with single characters and keeps merging the most frequent pair of pieces until it builds a vocabulary of common subwords.

In this blog, we will learn about **BPE (Byte Pair Encoding)** - the tokenization algorithm used by most modern Large Language Models (LLMs) to break text into smaller pieces before processing it.

We will understand what BPE is, why it is needed, and how it works step by step with a simple example.

Let's get started.

## What is Tokenization?

Before we understand BPE, we must first understand [tokenization](https://www.youtube.com/watch?v=sK2s9I84EVI).

When we type a sentence like "I love teaching AI", we see words. But a model does not understand words directly. It works with numbers. So, the first step is to break the text into small pieces called **tokens**. Each token is then converted into a number. This process of breaking text into tokens is called [**tokenization**](https://outcomeschool.com/blog/tokenization-in-llms).

Think of it like a chocolate bar. The full bar is the sentence. Each small part you break off is a token. The model processes multiple tokens at a time.

Now, the question is: how do we decide where to cut? How big or small should each token be?

This is where different tokenization approaches come into the picture.

## The Problem: How to Break Text into Tokens?

There are different ways to break text into tokens. Let's look at the two simplest approaches and understand why they do not work well.

**Approach 1: Word-Level Tokenization**

The simplest idea is to treat each word as one token.

For the sentence "I love teaching", the tokens would be: "I", "love", "teaching".

This seems easy. But the issue with this approach is that the model needs to know every word in the language. Think about it - there are hundreds of thousands of words in English alone. And then there are names, technical terms, words from other languages, misspellings, and new words being created every day.

If the model sees a word it has never seen before - like "ChatGPT" or "tokenization" - it does not know what to do. It treats the entire unknown word as a single "unknown" token and loses all meaning.

**Approach 2: Character-Level Tokenization**

The other extreme is to treat each character as one token.

For the sentence "I love", the tokens would be: "I", " ", "l", "o", "v", "e".

Now the model can handle any word - because every word is made up of characters, and the number of unique characters is very small compared to the number of words. For example, English has only 26 letters. Even if we include digits, punctuation, and spaces, the total is still very small. No word is ever "unknown."

But the issue with this approach is that the tokens are too small. The model has to process many more tokens for the same text. A 10-word sentence can become 50+ tokens. This makes training very slow and makes it harder for the model to understand meaning - because a single character like "l" carries very little meaning on its own.

We needed a solution that gives us the best of both worlds - not too big, not too small. So, here comes **BPE** to the rescue.

## What is BPE (Byte Pair Encoding)?

**BPE (Byte Pair Encoding)** is a tokenization algorithm that breaks text into pieces that are somewhere between characters and words.

It works by repeatedly finding the most common **pair** of adjacent tokens and merging them into one.

So, BPE starts with individual characters and keeps merging the most frequent pairs until it builds up a vocabulary of common pieces - called **subwords**. These subwords can be full words (like "the"), parts of words (like "ing", "un", "tion"), or even single characters.

Think of it like learning shorthand. When you first start taking notes, you write every letter. But over time, you notice that some combinations appear very often - like "ing" or "tion". So, you create shortcuts for them. BPE does the same thing automatically.

## How BPE Works: Step by Step

The best way to learn this is by taking an example.

Let's say we have the following text that we want to build our vocabulary from:

```
low low low low low
lower lower
newest newest newest newest newest newest
widest widest widest
```

For the sake of understanding, let's count the word frequencies:

- "low" appears 5 times
- "lower" appears 2 times
- "newest" appears 6 times
- "widest" appears 3 times

### Step 1: Start with Characters

We start by breaking every word into individual characters. We also add a special end-of-word symbol "\_" at the end of each word so the model knows where words end.

```
l o w _        (frequency: 5)
l o w e r _    (frequency: 2)
n e w e s t _  (frequency: 6)
w i d e s t _  (frequency: 3)
```

Our initial vocabulary is all the individual characters: `{l, o, w, e, r, n, s, t, i, d, _}`

### Step 2: Find the Most Frequent Pair

Now, we look at all pairs of adjacent tokens across our entire text and count how often each pair appears.

For the sake of understanding, let's count a few important pairs:

- "e s" appears in "newest" (6 times) and "widest" (3 times) = 9 times
- "s t" appears in "newest" (6 times) and "widest" (3 times) = 9 times
- "t \_" appears in "newest" (6 times) and "widest" (3 times) = 9 times
- "l o" appears in "low" (5 times) and "lower" (2 times) = 7 times
- "o w" appears in "low" (5 times) and "lower" (2 times) = 7 times

The most frequent pair is "e s" with 9 occurrences. We merge this pair into a single token "es".

### Step 3: Merge and Update

After merging "e s" into "es", our words now look like this:

```
l o w _         (frequency: 5)
l o w e r _     (frequency: 2)
n e w es t _    (frequency: 6)
w i d es t _    (frequency: 3)
```

Our vocabulary is now: `{l, o, w, e, r, n, s, t, i, d, _, es}`

Here, we can see that "e" and "s" have been merged into "es" wherever they appeared together.

### Step 4: Repeat

We repeat the same process. We find the next most frequent pair. Now "es t" appears 9 times (6 from "newest" and 3 from "widest"). We merge it into "est".

```
l o w _         (frequency: 5)
l o w e r _     (frequency: 2)
n e w est _     (frequency: 6)
w i d est _     (frequency: 3)
```

Vocabulary: `{l, o, w, e, r, n, s, t, i, d, _, es, est}`

We keep repeating this process. The next merge could be "est \_" into "est\_". Then "l o" into "lo". Then "lo w" into "low". And so on.

With each merge, our vocabulary grows by one token, and our text gets represented using fewer, larger pieces.

### Step 5: Stop When Done

We keep merging until we reach a desired **vocabulary size**. This size is a number we choose in advance. Modern LLMs typically use vocabulary sizes between 32,000 and 256,000 tokens. For example, LLaMA 3 uses a vocabulary of about 128K tokens, while Gemma uses about 256K tokens.

The final vocabulary contains a mix of:

- Full common words like "the", "is", "and"
- Common subwords like "ing", "tion", "est", "un"
- Individual characters for rare combinations

This is how BPE builds its vocabulary.

## How BPE Tokenizes New Text

Once BPE has finished training, it has two things: a vocabulary and an **ordered list of merge rules**. The order matters. During training, BPE learned these merges in a specific sequence - first "e s" into "es", then "es t" into "est", then "l o" into "lo", and so on. This exact sequence is saved.

Now, when BPE needs to tokenize new text, it does not simply look up subwords in the vocabulary. Instead, it **replays the same merge rules in the same order they were learned during training**.

Let's say we want to tokenize the word "lowest". Here is how it works:

**Start:** Break the word into individual characters: `l o w e s t`

**Apply merge rule 1** ("e s" into "es"): `l o w es t`

**Apply merge rule 2** ("es t" into "est"): `l o w est`

**Apply merge rule 3** ("l o" into "lo"): `lo w est`

**Apply merge rule 4** ("lo w" into "low"): `low est`

Result: "lowest" is tokenized as ["low", "est"].

Similarly, for the word "newer":

**Start:** `n e w e r`

The merge rules are applied in order. The rules that match adjacent pairs in this word get applied step by step, eventually producing: ["new", "er"].

For a rare word like "widestness":

**Start:** `w i d e s t n e s s`

The merge rules are applied in order. Common merges like "es" into "es" and "est" into "est" will fire when they match. The remaining characters stay as smaller pieces. The word gets broken into known subwords from the vocabulary.

**Why does the order matter?** Because different merge orders can produce different results. If we just did a greedy lookup - trying to find the longest matching subwords in the vocabulary - we could get different tokenizations than what the model expects. By replaying the merge rules in the exact training order, we get consistent and correct tokenizations every time.

This is the beauty of BPE. It never encounters a completely unknown word. Even if a word has never been seen before, BPE can break it down into smaller pieces by applying the merge rules. In the worst case, it falls back to individual characters - but that rarely happens for common languages. Problem Solved.

This is how BPE tokenizes new text.

## Why BPE is Used in Modern LLMs

BPE is the tokenization algorithm used by most modern LLMs. Here is why:

**Handles unknown words:** BPE can tokenize any word, even words it has never seen before, by breaking them into known subword pieces. No word is ever completely "unknown."

**Efficient vocabulary size:** Instead of needing millions of entries for every possible word, BPE creates a compact vocabulary of 32,000 to 256,000 tokens that can represent any text. It makes our life easy.

**Balances meaning and efficiency:** Common words like "the" and "is" are kept as single tokens - fast to process and meaningful. Rare words are broken into subword pieces - still understandable and manageable. This gives us the best of both worlds.

**Works across languages:** BPE works at the character level, so it can handle any language, any script, and any special characters. The same algorithm works for English, Chinese, Arabic, code, and that too without any changes to the algorithm itself.

Models use a variant of BPE, but the core idea remains the same - BPE or its variants are at the heart of how modern LLMs read and process text.

Once the text is split into tokens, the Transformer takes over. We have a detailed blog on [Encoder vs Decoder in Transformers](https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers) that explains the two blocks which process these tokens.

Now, we have understood BPE (Byte Pair Encoding) and how it works.

## Frequently Asked Questions

### Is BPE better than word-level tokenization?

Yes. Word-level tokenization needs the model to know every word, and an unseen word like "ChatGPT" becomes a single "unknown" token that loses all meaning. BPE breaks such a word into known subword pieces instead. So, no word is ever completely unknown.

### Why not just use character-level tokenization?

Character-level tokenization makes the tokens too small. A 10-word sentence can become 50+ tokens, which makes training very slow. It also makes it harder for the model to understand meaning, because a single character carries very little meaning on its own. BPE sits between characters and words.

### What vocabulary size do LLMs use with BPE?

Modern LLMs typically use vocabulary sizes between 32,000 and 256,000 tokens. This size is a number we choose in advance, and BPE keeps merging pairs until it reaches it. For example, LLaMA 3 uses about 128K tokens, while Gemma uses about 256K tokens.

### Does BPE use a greedy longest-match lookup to tokenize new text?

No. BPE replays the ordered list of merge rules in the same sequence they were learned during training. A greedy lookup of the longest matching subwords could give different tokenizations than what the model expects. Replaying the merges in order gives consistent and correct tokenizations every time.

### Can BPE ever fail to tokenize a word?

No. BPE can break any word, even one it has never seen, into smaller pieces by applying the merge rules. In the worst case, it falls back to individual characters. That rarely happens for common languages.
