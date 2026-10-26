---
title: What is DeepSeek-V4 and How Does It Work? Architecture Explained
module: 5
module_title: Modern LLM Architecture
lesson: '5.7'
source: https://outcomeschool.com/blog/decoding-deepseek-v4
published: April 24, 2026
tags:
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 3956
reading_time: 20
status: full
---
# What is DeepSeek-V4 and How Does It Work? Architecture Explained

> **Module 5 · Lesson 5.7**  
> Source: [Outcome School](https://outcomeschool.com/blog/decoding-deepseek-v4) · Published: April 24, 2026 · Reading time: ~20 min · Tags: `llm`, `ai`, `machine-learning`

---

![Decoding DeepSeek-V4](../../assets/images/05-05-07-what-is-deepseek-v4-and-how-does-it-work-architecture-explained/decoding-deepseek-v4.png)

DeepSeek-V4 is a family of open Mixture-of-Experts language models that supports a one-million-token context, at roughly a tenth of the cost of DeepSeek-V3.2.

In this blog, we will learn about DeepSeek-V4, the new family of open Mixture-of-Experts language models that natively supports a one-million-token context with dramatically lower inference cost.

DeepSeek-V4 makes one-million-token context roughly a tenth as expensive as it was in DeepSeek-V3.2. It introduces a new attention design, a new way of doing residual connections, a new optimizer, and a new post-training pipeline. We will decode each of these one by one.

We will cover the following:

- The Big Picture
- Two Models: DeepSeek-V4-Pro and DeepSeek-V4-Flash
- Hybrid Attention with CSA and HCA
- Manifold-Constrained Hyper-Connections (mHC)
- Muon Optimizer
- FP4 Quantization-Aware Training
- Pre-Training
- Post-Training: Specialist Training and On-Policy Distillation
- Reasoning Modes
- Putting It All Together
- Quick Summary

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

DeepSeek-V4 is built to solve one core problem: **make ultra-long context cheap**. Modern [reasoning models](https://outcomeschool.com/blog/large-reasoning-models) and AI Agents need to handle very long inputs - long documents, long tool histories, long agent trajectories. The standard attention mechanism in a Transformer [becomes very expensive as the input gets longer](https://outcomeschool.com/blog/evolution-of-llm-architecture). DeepSeek-V4 redesigns attention so that even a one-million-token input remains practical.

In simple words:

**DeepSeek-V4 = DeepSeek-V3 + Hybrid Compressed Attention + Better Residual Connections + Muon Optimizer + On-Policy Distillation.**

Let's put this into perspective with real numbers. At a one-million-token context:

- DeepSeek-V4-Pro uses only **27%** of the per-token compute of DeepSeek-V3.2.
- DeepSeek-V4-Pro uses only **10%** of the KV cache size of DeepSeek-V3.2.
- DeepSeek-V4-Flash uses only **10%** of the per-token compute and **7%** of the KV cache size of DeepSeek-V3.2.

This is a massive efficiency gain. Now, let's decode each piece.

## Two Models: DeepSeek-V4-Pro and DeepSeek-V4-Flash

DeepSeek-V4 ships as two models. Both are **[Mixture-of-Experts (MoE)](https://outcomeschool.com/blog/mixture-of-experts)** models. In an MoE model, the feed-forward layer is split into many small expert networks, and a router picks only a few experts per token. This is how the total parameter count can be huge while the per-token compute stays small.

Let me tabulate the differences between the two models for your better understanding so that you can decide which one to use based on your use case.

| Model | Total Parameters | Activated Parameters | Transformer Layers | Context Length | Pre-training Tokens |
| --- | --- | --- | --- | --- | --- |
| DeepSeek-V4-Flash | 284B | 13B | 43 | 1M | 32T |
| DeepSeek-V4-Pro | 1.6T | 49B | 61 | 1M | 33T |

Here, "activated" means the parameters that actually run for each input token. In an MoE model, only a small fraction of the experts are active per token, so activated parameters are much smaller than total parameters.

Both models support a context of **one million tokens** natively. Both are trained on more than 32 trillion tokens.

DeepSeek-V4-Pro is the larger, more capable model. DeepSeek-V4-Flash is the smaller, faster, more cost-efficient model.

## Hybrid Attention with CSA and HCA

This is the most important change in DeepSeek-V4. Let's understand the problem first.

**The Problem.** Standard attention compares every query token with every other token. Suppose we have N tokens in the input. The cost grows like N x N. At one million tokens, this becomes one trillion comparisons across the full sequence. The KV cache, which is the memory of past keys and values, also grows linearly with N. Both of these become a serious bottleneck for long context.

We have a detailed blog on [KV Cache in LLMs](https://outcomeschool.com/blog/kv-cache-in-llms) that explains what KV cache is and why it matters, and another on [KV Cache Compression](https://outcomeschool.com/blog/kv-cache-compression) that covers the standard ways to shrink it.

**The Solution.** Here comes the hybrid attention design to the rescue. DeepSeek-V4 introduces two new attention types and uses both of them in an interleaved manner across layers:

- **CSA (Compressed Sparse Attention)** - lighter compression, but uses sparse selection.
- **HCA (Heavily Compressed Attention)** - heavier compression, but keeps attention dense.

Let's decode the names first.

**CSA = Compressed + Sparse + Attention.**

**HCA = Heavily + Compressed + Attention.**

The best way to learn this is by taking an example. Let's say we are reading a huge library of one million pages and we want to answer a question. Standard attention is like reading every single page from start to end before answering. It works, but it is painfully slow.

CSA and HCA both fix this, but in different ways. We will use this library example throughout to understand both. Let's decode each one.

### CSA: Compressed Sparse Attention

CSA does two things to make attention cheap.

**Step 1: Compress.** Instead of keeping the KV cache for every single token, CSA combines every `m` consecutive tokens into one compressed entry using learned softmax weights. Just for the sake of understanding, let's say `m = 4`. So every 4 tokens get combined into 1 entry in the KV cache. The KV cache shrinks by a factor of `m`.

In our library example, this is like grouping every 4 pages into one summary card. Instead of reading 1 million pages, we now have only 250K summary cards to look at.

**Step 2: Select.** After compression, CSA still does not look at every summary card. It uses a small **Lightning Indexer** to score each compressed entry against the current query, and then picks only the top-k most relevant ones. The Lightning Indexer runs in FP4 precision to keep this scoring step cheap.

In our library example, this is like a quick scanner who flips through the 250K summary cards, scores each one for relevance, and hands us only the top few cards. We then read only those few cards in detail. Most of the library is skipped completely.

For a deeper background on Q, K, V in attention, we have a detailed blog on [Math Behind Attention: Q, K, V](https://outcomeschool.com/blog/math-behind-attention-qkv).

Here is a simple ASCII picture:

```
All tokens:    [t1][t2][t3][t4][t5][t6][t7][t8] ...
                |__________|  |__________|
                  group 1       group 2
                     |             |
Compressed:        [C1]          [C2]          [C3] ...
                     |             |             |
Lightning Indexer scores each one against current query
                     |             |             |
                  score=0.9     score=0.2     score=0.8
                     |             |             |
Top-k selection:   [ C1 ]        ( C2 )        [ C3 ]
                   picked        skipped       picked
                     |                           |
                     +-------------+-------------+
                                   |
                                   v
                  Attention runs only on [C1] and [C3]
                         (the picked compressed entries)
```

So CSA first compresses many tokens into one, and then picks only the few compressed entries that look most relevant. This is how CSA brings the cost down. Both compute and memory are saved.

### HCA: Heavily Compressed Attention

This was all about CSA. Now, let's move to HCA.

HCA makes a different trade-off. It compresses much more aggressively, and because the compressed sequence is already tiny, dense attention on it is cheap. No need for sparse selection.

HCA uses a much larger group size `m'`, much bigger than `m` in CSA. For DeepSeek-V4, `m'` is set to 128. So instead of combining 4 tokens into one entry, HCA combines 128 tokens into one entry. The KV cache shrinks even more dramatically.

In our library example, this is like grouping every 128 pages into one summary card. Now we have only about 7,800 summary cards in total. Since the number of cards is already very small, we just read all of them, every time. There is no need to pick the top few.

So CSA and HCA are two different design points with the same goal - cheap long-context attention. CSA does mild compression plus sparse top-k selection. HCA does aggressive compression plus dense attention. The result for both: very low compute and very low memory.

This was all about HCA. Now, let's see how the actual model uses both.

In DeepSeek-V4, the layers are interleaved. For DeepSeek-V4-Flash, the first two layers use pure [sliding window attention](https://outcomeschool.com/blog/how-does-sliding-window-attention-work), and the rest alternate between CSA and HCA. For DeepSeek-V4-Pro, the first two layers use HCA, and the rest alternate between CSA and HCA. This way, different layers handle long context in slightly different ways, and together they cover both fine-grained selection (CSA) and broad coverage (HCA).

### Sliding Window Branch

Now, a natural question arises - what if compression blurs out important details from very recent tokens?

The answer is the **sliding window branch**. Both CSA and HCA also keep a small extra set of recent uncompressed KV entries. For DeepSeek-V4, this window size is 128 tokens.

In our library example, this is like always keeping the last 128 pages we just read on our desk in full. Compression is used for the older pages, but the most recent pages are right there in front of us, uncompressed and ready to read. This makes sure that local fine-grained dependencies are not lost.

### Attention Sink

One more small but clever trick. In the core attention of both CSA and HCA, DeepSeek-V4 adds a small set of learnable **sink logits** to the denominator of the softmax. This allows each attention head to have attention scores that sum to *less than* 1.

Why does this help? In standard attention, the scores are forced to sum to exactly 1. This means every query token must distribute all of its attention somewhere, even when nothing in the context is actually relevant. [Attention sinks](https://outcomeschool.com/blog/how-do-attention-sinks-work) let the model say "none of these are important right now" and spend less attention overall.

DeepSeek-V4 also applies [RMSNorm](https://outcomeschool.com/blog/rmsnorm-root-mean-square-layer-normalization) on the queries and compressed KV entries just before the core attention step. This is what keeps attention logits stable and prevents them from exploding.

**Note:** Put together, CSA, HCA, Sliding Window, and Attention Sink make one trade-off possible: **less memory, less compute, with no major loss in quality**. That is what makes one-million-token context practical.

## Manifold-Constrained Hyper-Connections (mHC)

This was all about attention. Now, let's move to the residual connections inside the Transformer.

Let's decode the name first.

**mHC = Manifold + Constrained + Hyper + Connections.**

In a normal Transformer, every layer adds its output to a "residual stream" - a single shared signal that flows from the bottom of the model to the top. Hyper-Connections (HC) widen this residual stream by a factor of `n_hc` (set to 4 in DeepSeek-V4), turning the single stream into multiple parallel streams. Three learned matrices (A, B, C) mix these streams at every layer, giving the model more flexibility in how information flows.

The issue with plain HC is that it becomes numerically unstable when we stack many layers. The signal can blow up or collapse. Training breaks down.

So, here comes mHC to the rescue. mHC fixes the problem by **constraining** the residual mapping matrix to lie on a special manifold called the Birkhoff polytope - the set of doubly stochastic matrices. A doubly stochastic matrix is a matrix whose every row sums to 1 and every column sums to 1. This simple constraint bounds the largest stretch factor (the spectral norm) of the matrix at 1, so the signal cannot blow up as it passes through dozens of layers.

The result is that deeper stacks train stably, and the model expressivity is preserved. It works perfectly.

## Muon Optimizer

This was all about mHC. Now, let's move to the optimizer.

DeepSeek-V4 swaps the optimizer for most of its parameters from AdamW to **Muon**.

**Muon = An optimizer that uses the full gradient matrix and orthogonalizes the update direction.**

Why does this matter? Most optimizers like AdamW treat each weight independently. Muon, on the other hand, looks at the full gradient matrix and applies an orthogonalization step before doing the weight update. This orthogonalization is done using Newton-Schulz iterations. It normalizes all the singular values of the update matrix to be close to 1, so no single direction in the update dominates. The result is faster convergence and more stable training.

A few important points:

- AdamW is still used for the embedding module, the prediction head, all RMSNorm modules, and the static parts of mHC.
- Muon is used for everything else.
- The DeepSeek team uses a hybrid Newton-Schulz iteration with carefully chosen coefficients for stable orthogonalization.

This gives us the best of both worlds. Muon brings faster convergence where it matters, and AdamW stays where it is already proven to work well.

## FP4 Quantization-Aware Training

Now, let's move to how DeepSeek-V4 makes inference faster and cheaper. The answer is **FP4 Quantization-Aware Training**.

Let's decode this.

- **FP4** stands for floating point with only 4 bits per number. Compared to FP8 or BF16, FP4 uses much less memory and bandwidth. It makes our life easier on the hardware side.
- **[Quantization-Aware Training (QAT)](https://outcomeschool.com/blog/how-does-model-quantization-work)** means the model is trained while simulating the lower-precision number format, so the weights adapt to the precision loss during training itself. Without QAT, we would squeeze the weights down only at deployment time, and the model would lose quality. With QAT, the model learns to live with low precision.

DeepSeek-V4 applies FP4 to two key places:

- **MoE expert weights**, which take up most of the GPU memory.
- The **Query-Key (QK) path of the CSA indexer**, where the lightning indexer computes scores in FP4.

There is one more clever detail here. FP8 (E4M3) has 2 more exponent bits than FP4 (E2M1), which gives it a much wider dynamic range. Because of this, the FP4 block scale factors can be fully absorbed into the FP8 format during dequantization. This means the FP4-to-FP8 dequantization is **lossless**, and the entire existing FP8 training pipeline can be reused without any modification.

The end result is a 2x speedup on the top-k selector while preserving a 99.7% recall of KV entries. There is no major quality loss.

## Pre-Training

Now that we have learned about the architecture and optimizer, it's time to learn about pre-training.

**Data.** The pre-training corpus has more than **32 trillion tokens**. It includes mathematical content, code, web pages, long documents, scientific papers, and multilingual data. The team puts a special emphasis on long-document curation since the model is built for long context.

**Sequence length scheduling.** Training does not start at one-million tokens directly. First, the model trains at a sequence length of 4K. Then, the length is extended to 16K. After that, to 64K. Finally, to 1M. Sparse attention is also turned on gradually. The model first warms up with dense attention for the first 1T tokens, and sparse attention is introduced at 64K and kept on for the rest of the training.

**Mitigating Training Instability.** Training trillion-parameter MoE models is hard. Loss spikes happen. But here is the catch - simple rollbacks do not prevent the next spike from happening. The DeepSeek team found two practical tricks that fix this:

- **Anticipatory Routing.** The MoE routing network at step `t` is computed using slightly older parameters `θ_{t-Δt}`, while the rest of the backbone uses the current parameters `θ_t`. This asymmetry breaks the feedback loop where bad routing causes outliers, which then cause worse routing.
- **SwiGLU Clamping.** The output of the SwiGLU activation is clamped to a fixed range. This prevents extreme values from appearing and destabilizing training.

With these two tricks in place, training stays stable all the way through.

## Post-Training: Specialist Training and On-Policy Distillation

Till now, we have learned about pre-training. Now, it's time to learn about post-training.

Post-training is where DeepSeek-V4 takes a different path from many other models. The pipeline has two stages. Let's decode each one.

### Stage 1: Specialist Training

For each target domain like mathematics, coding, agent use, instruction following, and etc., the DeepSeek team trains a separate **expert model**. Each expert model is built in two steps.

First, the base model goes through [Supervised Fine-Tuning (SFT)](https://outcomeschool.com/blog/how-does-fine-tuning-work) on high-quality, domain-specific data. This establishes the foundational capability for that domain. Then, [Reinforcement Learning](https://outcomeschool.com/blog/reinforcement-learning) is applied using **[GRPO (Group Relative Policy Optimization)](https://outcomeschool.com/blog/group-relative-policy-optimization-grpo)**, guided by domain-specific reward signals. This sharpens the model for the specific success criteria of that domain.

After this stage, the team has multiple specialist expert models - one per domain, each trained for varying reasoning efforts - each excelling in its own field.

This was all about Stage 1. Now, let's move to Stage 2.

### Stage 2: On-Policy Distillation (OPD)

Now, a natural question arises - how do we combine all these expert models into one final unified model?

The answer is **On-Policy Distillation (OPD)**.

In simple words:

**On-Policy Distillation = The student model generates its own outputs, and learns to match the probability distribution of the right teacher expert for each task.**

Let's understand what makes OPD different from [regular distillation](https://outcomeschool.com/blog/how-does-knowledge-distillation-work).

In regular distillation, the student learns from data that the teacher produced. But there is one catch - the student never sees the kind of outputs it actually produces at inference time. This creates a gap between training and real behavior.

In OPD, the student samples its own trajectories. This is the "on-policy" part. The student writes its own drafts, and the teacher corrects each token by providing the full vocabulary distribution it would have used. The student is pulled towards the teacher's distribution using **reverse KL loss**. Reverse KL is mode-seeking - it pushes the student to concentrate probability mass where the teacher's mass is concentrated, rather than smearing out across all teacher modes. This gives sharper, more decisive outputs.

Also, different teachers are weighted based on the task. For a math task, the math expert teaches more. For a coding task, the coding expert teaches more. This way, all the specialist knowledge gets merged into one single unified student.

This step replaces the traditional mixed RL stage that DeepSeek-V3.2 used. The team found that OPD gives more stable and faithful knowledge transfer than weight merging or mixed RL, which is why it became the core consolidation step in the DeepSeek-V4 post-training pipeline.

## Reasoning Modes

This was all about post-training. Now, let's move to how DeepSeek-V4 actually serves users at inference time.

DeepSeek-V4 supports three reasoning modes that the user can pick depending on how hard the task is. Let me tabulate the differences between them for your better understanding so that you can decide which one to use based on your use case.

| Reasoning Mode | When to Use | How it Works |
| --- | --- | --- |
| Non-think | Routine daily tasks, quick answers | No `<think>` block, direct response |
| Think High | Complex problem-solving, planning | `<think>` block with conscious reasoning |
| Think Max | Pushing reasoning to its limit | Long `<think>` block with a special "absolute maximum" instruction injected |

For **Think Max** mode, the injected system prompt essentially tells the model: *Reasoning effort is set to absolute maximum with no shortcuts permitted. Be very thorough, decompose the problem to its root cause, rigorously stress-test your logic against all edge cases and adversarial scenarios, and write out every intermediate step, considered alternative, and rejected hypothesis explicitly.* This instruction stretches the reasoning as far as it can go.

This way, the model can be cheap when the question is easy, and slow but powerful when the question is hard. We get to control the trade-off based on our use case.

## Putting It All Together

Now, let's put everything together to see how DeepSeek-V4 runs end to end.

In one sentence: a token enters the embedding layer, flows through many Transformer blocks (each one alternating CSA/HCA attention with a DeepSeekMoE feed-forward layer, both wrapped by mHC residual connections), and exits through the prediction head and MTP modules.

Here is the high-level architecture of one Transformer block in DeepSeek-V4:

```
                    Input Tokens
                         |
                     Embedding
                         |
        +----------------|----------------+
        |          Pre-Block Mixing       |
        |                |                |
        |             CSA / HCA           |   <- Hybrid Attention
        |                |                |
        |          Post-Block Mixing      |
        |                |                |
        |          Residual Mixing        |   <- mHC residuals
        |                |                |
        |          Pre-Block Mixing       |
        |                |                |
        |           DeepSeekMoE           |   <- Mixture of Experts FFN
        |                |                |
        |          Post-Block Mixing      |
        |                |                |
        |          Residual Mixing        |   <- mHC residuals
        +----------------|----------------+
                  (repeat for L layers)
                         |
                    Prediction Head
                         |
                    MTP Modules           <- Multi-Token Prediction
                         |
                       Output
```

At the top of the stack, a prediction head and **MTP (Multi-Token Prediction)** modules produce the output. MTP allows the model to predict more than one token at a time during training, which improves data efficiency, and at inference it can also serve as a built-in drafter for [Speculative Decoding](https://outcomeschool.com/blog/speculative-decoding). We have a detailed blog on [Medusa](https://outcomeschool.com/blog/decoding-medusa) that explains how extra prediction heads like these speed up generation without a separate draft model.

This is how DeepSeek-V4 runs end to end - combining strong capability with one-million-token efficiency.

## Quick Summary

Let's recap what we have decoded:

- **DeepSeek-V4** is a family of open MoE language models built for ultra-long context. Two variants: **V4-Pro (1.6T total, 49B active)** and **V4-Flash (284B total, 13B active)**, both natively supporting **1M tokens**.
- **Hybrid Attention** combines **CSA (Compressed Sparse Attention)** and **HCA (Heavily Compressed Attention)** in an interleaved manner. CSA compresses tokens into groups and then picks top-k. HCA compresses even more but keeps attention dense. A small sliding window keeps recent tokens uncompressed, and learnable attention sinks keep attention logits stable.
- **mHC (Manifold-Constrained Hyper-Connections)** widens the residual stream by `n_hc=4` and constrains the mixing matrix to the Birkhoff polytope (doubly stochastic matrices, rows and columns summing to 1), which bounds the spectral norm at 1 for stable deep training.
- **Muon Optimizer** orthogonalizes the gradient update matrix using Newton-Schulz iterations, normalizing all singular values close to 1 for balanced, faster convergence. AdamW is still used for embeddings and a few other modules.
- **FP4 Quantization-Aware Training** is applied to MoE expert weights and the CSA indexer, with a lossless FP4-to-FP8 dequantization that reuses the existing FP8 pipeline unchanged.
- **Pre-training** uses 32T+ tokens with a sequence length schedule that grows from 4K to 1M, plus **Anticipatory Routing** and **SwiGLU Clamping** to fix loss spikes.
- **Post-training** has two stages: **Specialist Training** (SFT + GRPO per domain) followed by **On-Policy Distillation (OPD)** that merges all specialists into one unified student model.
- **Three reasoning modes** - Non-think, Think High, Think Max - let the user trade off cost and depth.
- **Net result:** at 1M-token context, DeepSeek-V4-Pro uses only 27% of the FLOPs and 10% of the KV cache of DeepSeek-V3.2. DeepSeek-V4-Flash pushes this further to 10% FLOPs and 7% KV cache.

This is how the DeepSeek-V4 series ushers in a new era of million-length contexts for open large language models.

## Frequently Asked Questions

### Should we use DeepSeek-V4-Pro or DeepSeek-V4-Flash?

We should pick DeepSeek-V4-Pro when we need the larger, more capable model, and DeepSeek-V4-Flash when we need a smaller, faster, more cost-efficient model. Pro has 1.6T total and 49B activated parameters, while Flash has 284B total and 13B activated. Both support a context of one million tokens.

### How is DeepSeek-V4 different from DeepSeek-V3?

DeepSeek-V4 is DeepSeek-V3 plus Hybrid Compressed Attention, better residual connections, the Muon optimizer, and On-Policy Distillation. At a one-million-token context, DeepSeek-V4-Pro uses only 27% of the per-token compute and 10% of the KV cache size of DeepSeek-V3.2. It also replaces the mixed RL stage of DeepSeek-V3.2 with On-Policy Distillation.

### Does FP4 quantization reduce the quality of DeepSeek-V4?

Not in a major way, since there is no major quality loss. The model is trained with Quantization-Aware Training, so the weights adapt to the lower precision during training itself. FP4 gives a 2x speedup on the top-k selector while preserving a 99.7% recall of KV entries.

### Does DeepSeek-V4 use the Muon optimizer for every parameter?

No. Muon is used for most parameters, but AdamW is still used for the embedding module, the prediction head, all RMSNorm modules, and the static parts of mHC. This gives the best of both worlds. Muon brings faster convergence where it matters, and AdamW stays where it is already proven to work well.

### Why is on-policy distillation better than regular distillation?

On-policy distillation closes the gap between training and real behavior. In regular distillation, the student learns from data the teacher produced, so it never sees the kind of outputs it actually produces at inference time. In on-policy distillation, the student samples its own outputs, and the teacher corrects each token.
