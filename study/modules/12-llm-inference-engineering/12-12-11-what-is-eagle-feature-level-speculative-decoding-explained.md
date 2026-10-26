---
title: What is EAGLE? Feature-Level Speculative Decoding Explained
module: 12
module_title: LLM Inference Engineering
lesson: '12.11'
source: https://outcomeschool.com/blog/decoding-eagle
published: September 1, 2026
tags:
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 1607
reading_time: 8
status: full
---
# What is EAGLE? Feature-Level Speculative Decoding Explained

> **Module 12 · Lesson 12.11**  
> Source: [Outcome School](https://outcomeschool.com/blog/decoding-eagle) · Published: September 1, 2026 · Reading time: ~8 min · Tags: `llm`, `ai`, `machine-learning`

---

![Decoding EAGLE](../../assets/images/12-12-11-what-is-eagle-feature-level-speculative-decoding-explained/decoding-eagle.png)

EAGLE is a speculative decoding method that makes a language model generate text faster without changing its output at all. It guesses the future tokens at the level of the model's internal features, not at the level of words.

In this blog, we will learn about EAGLE, a state-of-the-art way to speed up language model generation by drafting tokens at the feature level instead of the token level.

We will cover the following:

- What is EAGLE?
- A quick recap of speculative decoding
- The problem with token-level drafting
- The big idea: draft at the feature level
- Resolving the uncertainty by feeding back the token
- The math behind the speedup with small numbers
- EAGLE-2 and dynamic draft trees
- How EAGLE lives on today
- Quick Summary

Let's get started.

EAGLE was introduced in 2024 in the research papers "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty" and its follow-up "EAGLE-2", by Yuhui Li and collaborators at Peking University, Microsoft Research, and the University of Waterloo.

EAGLE is among the fastest lossless ways to speed up text generation, and it is built into many serving systems. It improves on earlier methods with one key insight about where to do the drafting. So, let's decode it piece by piece.

## What is EAGLE?

EAGLE is a speculative decoding method, a way to make a language model generate text faster without changing its output at all.

It works by having a small, cheap draft step guess several future tokens, which the big model then checks all at once. EAGLE's twist is that it does the guessing at the level of the model's internal **features**, not at the level of words. This makes the guesses much more accurate, which leads to a bigger speedup.

## A quick recap of speculative decoding

We covered [speculative decoding](https://outcomeschool.com/blog/speculative-decoding) and [Medusa](https://outcomeschool.com/blog/decoding-medusa) before. The short version: generating text one token at a time is slow because each token needs a full pass through the big model. That slow, one-token-at-a-time stage is the decode phase of inference. We have a detailed blog on [Prefill vs Decode](https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization) that explains why it is the bottleneck.

Speculative decoding fixes this by cheaply guessing several tokens ahead, then letting the big model verify them all in a single pass. If the guesses are right, we get several tokens for the cost of one verification. The better the guesses, the more tokens are accepted, and the bigger the speedup.

So the whole game is making accurate guesses cheaply. EAGLE found a better place to make them.

## The problem with token-level drafting

Earlier methods, like [Medusa](https://outcomeschool.com/blog/decoding-medusa), guess the next tokens directly. But predicting the exact next token is hard and uncertain.

Why? Because of sampling. Even the big model does not output one token, it outputs a probability distribution, and the actual token is [sampled from it with some randomness](https://outcomeschool.com/blog/how-does-temperature-control-llm-output). Predicting which token will be sampled is inherently noisy. So token-level guesses are often wrong, and wrong guesses get rejected, which limits the speedup.

We wanted a more predictable thing to guess. EAGLE found one.

## The big idea: draft at the feature level

EAGLE's insight is to guess the next **feature** instead of the next token.

A feature here means the model's internal hidden state, the rich vector it computes in its second-to-last layer, just before it turns that vector into a token. EAGLE observed that this feature sequence is much more **regular and predictable** than the token sequence. The randomness of sampling happens at the very last step, token selection, but the features flowing underneath are smooth.

So EAGLE trains a small, lightweight draft network that [autoregresses](https://outcomeschool.com/blog/autoregressive-models) at the feature level: it predicts the next feature from the previous features, and only at the end maps features to tokens. Because features are more predictable than tokens, these drafts are far more accurate, so more of them get accepted by the big model.

```
Medusa style:   guess the next TOKEN directly        (noisy, often rejected)
EAGLE style:    guess the next FEATURE, then the token (smooth, often accepted)
```

## Resolving the uncertainty by feeding back the token

There is a subtlety EAGLE had to fix, which gives the first paper its name: feature uncertainty.

The next feature actually depends on which token was sampled at the previous step. If we do not know the sampled token, the next feature is uncertain. EAGLE solves this by feeding the previously sampled token back into the draft network, along with the features.

So the draft network looks at both the smooth feature stream and the actual token that was just chosen, which removes the uncertainty and lets it predict the next feature accurately. This combination is what makes EAGLE's drafts so good.

## The math behind the speedup with small numbers

The speedup of any speculative method is simply how many tokens get accepted per verification pass, on average. We saw this with [Medusa](https://outcomeschool.com/blog/decoding-medusa).

Suppose token-level drafting gets, on average, `2.5` tokens accepted per pass:

```
token-level speedup = about 2.5 times
```

Because EAGLE's feature-level drafts are more accurate, more of them survive verification. Suppose it gets `3.5` tokens accepted per pass:

```
feature-level speedup = about 3.5 times
```

The whole gain comes from a higher acceptance rate: more guessed tokens are correct, so more are kept per pass. And because every kept token is still verified against the big model, the final output is exactly what the big model would have produced. The speedup is free in quality.

**Note:** Acceptance counts of `2.5` and `3.5` are just for the sake of understanding, so we can see the relationship. Real numbers depend on the model and task. The rule, more accurate drafts mean more accepted tokens mean more speedup, stays exactly the same.

## EAGLE-2 and dynamic draft trees

EAGLE-2 added another improvement. Instead of a fixed shape of guesses, it builds a **dynamic draft tree**.

The draft network does not just guess one chain of tokens. It guesses a tree of likely continuations. EAGLE-2 makes this tree **context-aware**: it spends more guesses where the draft network is confident and fewer where it is unsure, and it shapes the tree on the fly for each input. This squeezes out even more accepted tokens per pass, pushing the speedup higher, while still being lossless.

## How EAGLE lives on today

EAGLE is one of the leading speculative decoding methods in practice.

- It gives **some of the highest lossless speedups** available, often around `3` to `4` times faster generation, and is widely adopted.
- It is supported in major serving systems like [**vLLM**](https://outcomeschool.com/blog/how-does-vllm-work), [**SGLang**](https://outcomeschool.com/blog/how-does-sglang-work), and [**TensorRT-LLM**](https://outcomeschool.com/blog/how-does-tensorrt-llm-work), so many production deployments use it.
- Its core lesson, that drafting at the smoother feature level beats drafting at the noisy token level, influenced later fast-inference research, and it was extended further in EAGLE-3.

Speculative decoding is one piece of a much bigger toolkit for fast serving. We have a detailed blog on [LLM Inference Optimization](https://outcomeschool.com/blog/llm-inference-optimization) that covers these techniques end to end.

So EAGLE took the powerful idea of speculative decoding and made it sharper by guessing the model's smooth internal features instead of its noisy output tokens, getting more accepted tokens and a bigger speedup for free.

## Quick Summary

- **EAGLE** is a state-of-the-art speculative decoding method that speeds up generation losslessly.
- [Speculative decoding](https://outcomeschool.com/blog/speculative-decoding) guesses several tokens cheaply and verifies them in one pass, so better guesses mean more speedup.
- Guessing the exact next **token** is noisy because of sampling randomness, which limits earlier methods like [Medusa](https://outcomeschool.com/blog/decoding-medusa).
- EAGLE's big idea is to draft at the **feature level**, the smooth internal hidden state, which is far more predictable than tokens.
- It resolves **feature uncertainty** by feeding the previously sampled token back into the draft network.
- The speedup equals the **average accepted tokens per pass**, and more accurate feature-level drafts raise it, for example from `2.5` to `3.5` times.
- **EAGLE-2** adds context-aware **dynamic draft trees** for even more speedup, and EAGLE is used in vLLM, SGLang, and TensorRT-LLM.

Now, we have decoded EAGLE piece by piece and understood how drafting smooth internal features instead of noisy tokens makes speculative decoding faster while keeping the output identical.

## Frequently Asked Questions

### Does EAGLE change the output of the language model?

No. EAGLE makes generation faster without changing the output at all. Every drafted token is still verified against the big model, so the final output is exactly what the big model would have produced. The speedup is free in quality.

### Is EAGLE better than Medusa?

Yes. EAGLE usually gets a bigger speedup than Medusa. Medusa guesses the next tokens directly, and token-level guesses are noisy because of sampling randomness, so many get rejected. EAGLE guesses the next feature, which is smoother and more predictable, so more drafts are accepted per pass.

### How much faster does EAGLE make text generation?

EAGLE often gives around 3 to 4 times faster generation. This is among the highest lossless speedups available. The exact number depends on the model and task, since the speedup equals the average number of tokens accepted per verification pass.

### Is EAGLE used in production serving systems?

Yes. EAGLE is supported in major serving systems like vLLM, SGLang, and TensorRT-LLM, so many production deployments use it. It is one of the leading speculative decoding methods in practice, and it was extended further in EAGLE-3.
