---
title: LLM Inference Optimization
module: 12
module_title: LLM Inference Engineering
lesson: '12.1'
source: https://outcomeschool.com/blog/llm-inference-optimization
published: June 14, 2026
tags:
- llm
- ai
- system-design
videos:
- title: LLM Inference Optimization
  url: https://www.youtube.com/watch?v=jV2sCj4lHYk
fetched: '2026-10-24'
words: 2469
reading_time: 12
status: full
---
# LLM Inference Optimization

> **Module 12 · Lesson 12.1**  
> Source: [Outcome School](https://outcomeschool.com/blog/llm-inference-optimization) · Published: June 14, 2026 · Reading time: ~12 min · Tags: `llm`, `ai`, `system-design`
> Video: [LLM Inference Optimization](https://www.youtube.com/watch?v=jV2sCj4lHYk)

---

![LLM Inference Optimization](../../assets/images/12-12-01-llm-inference-optimization/llm-inference-optimization.png)

LLM Inference Optimization is the set of techniques that make a Large Language Model generate its answers faster and serve more users at a lower cost.

Techniques like KV Cache, Paged Attention, Flash Attention, Speculative Decoding, and Continuous Batching are what make LLMs fast and scalable in production. Let’s learn all of these techniques one by one.

## KV Cache in LLMs

In this blog, we will learn about **KV Cache** - where **K** stands for **Key** and **V** stands for **Value** - and why it is used in Large Language Models (LLMs) to speed up text generation.

We will start with how LLMs generate text one token at a time, understand the role of Key, Value, and Query inside the model, see the problem of repeated computation through an example, and then walk through how KV Cache solves this problem by storing and reusing past results.

**Read here:** [KV Cache in LLMs](https://outcomeschool.com/blog/kv-cache-in-llms)

---

## KV Cache Compression

In this blog, we will learn about **KV Cache Compression**, the set of techniques that shrink the memory an AI model uses to remember the conversation while it is writing its reply.

We will cover the following:

- What is an LLM and how it writes text
- What is Attention
- What is the KV Cache
- Why the KV Cache becomes huge
- What is KV Cache Compression
- Approach 1: Quantization
- Approach 2: Token Eviction
- Approach 3: Sharing Keys and Values across Heads
- Approach 4: Low-Rank Compression
- Comparison of the approaches
- When to use which one

**Read here:** [KV Cache Compression](https://outcomeschool.com/blog/kv-cache-compression)

---

## Paged Attention in LLMs

In this blog, we will learn about **Paged Attention**, a technique that solves the memory waste problem of KV Cache, allowing LLMs to serve many more users at the same time.

We will start with a quick recap of KV Cache, understand the memory problem it creates, see how traditional memory allocation wastes space through an example, and then walk through how Paged Attention solves this problem by borrowing an idea from how computers manage memory.

**Read here:** [Paged Attention in LLMs](https://outcomeschool.com/blog/paged-attention-in-llms)

---

## Decoding Flash Attention in LLMs

In this blog, we will learn about **Flash Attention** by decoding it piece by piece - understanding why standard attention is slow, what makes Flash Attention fast, how it uses GPU memory cleverly, and why it is used in almost every modern Large Language Model (LLM).

We will cover the following:

- A quick recap of standard attention
- Why standard attention is slow
- How GPU memory actually works (HBM vs SRAM)
- The core idea behind Flash Attention
- Tiling: breaking the work into small blocks
- Online softmax: computing softmax without the full matrix
- Recomputation in the backward pass
- Flash Attention 2
- Flash Attention 3
- Advantages and impact of Flash Attention

**Read here:** [Decoding Flash Attention in LLMs](https://outcomeschool.com/blog/decoding-flash-attention)

---

## Grouped Query Attention

In this blog, we will learn about **Grouped-Query Attention (GQA)** and how it differs from **Multi-Head Attention (MHA)**.

Today, we will cover the following topics:

- Quick Recap: Multi-Head Attention (MHA)
- The Problem with Multi-Head Attention
- What is Multi-Query Attention (MQA)?
- What is Grouped-Query Attention (GQA)?
- How Grouped-Query Attention Works
- GQA is a Generalization of MHA and MQA
- GQA vs MHA vs MQA
- Real-World Use Cases
- A Note on Terminology
- Uptraining: Converting MHA to GQA
- Quick Summary

**Read here:** [Grouped Query Attention](https://outcomeschool.com/blog/grouped-query-attention)

---

## Speculative Decoding

In this blog, we will learn about **Speculative Decoding** - what it is, why LLM generation is slow without it, how a small draft model and a big target model work together to produce tokens faster, the rejection sampling math that guarantees no quality loss, real numbers showing the 2× to 3× speedup, where it is used in production, and the trade-offs to watch out for.

We will cover the following:

- What problem does Speculative Decoding solve?
- The Big Picture
- Why is LLM generation slow?
- The core idea behind Speculative Decoding
- Step-by-step walkthrough
- The verification step
- Real numbers and speedup
- Where it is used
- Trade-offs
- Quick Summary

**Read here:** [Speculative Decoding](https://outcomeschool.com/blog/speculative-decoding)

---

## Decoding Medusa

In this blog, we will learn about **Medusa**, a simple way to make a language model generate text 2 to 3 times faster by giving it several extra heads that guess multiple future tokens at once.

We will cover the following:

- What is Medusa
- Why text generation is slow
- A quick recap of speculative decoding
- The problem with needing a draft model
- The big idea: many heads on one model
- How tree attention checks many guesses at once
- The math behind the speedup with small numbers
- The results
- How Medusa lives on today
- Quick Summary

**Read here:** [Decoding Medusa](https://outcomeschool.com/blog/decoding-medusa)

---

## Decoding EAGLE

In this blog, we will learn about **EAGLE**, a state-of-the-art way to speed up language model generation by drafting tokens at the feature level instead of the token level.

We will cover the following:

- What is EAGLE
- A quick recap of speculative decoding
- The problem with token-level drafting
- The big idea: draft at the feature level
- Resolving the uncertainty by feeding back the token
- The math behind the speedup with small numbers
- EAGLE-2 and dynamic draft trees
- How EAGLE lives on today
- Quick Summary

**Read here:** [Decoding EAGLE](https://outcomeschool.com/blog/decoding-eagle)

---

## N-gram Speculation in LLMs

In this blog, we will learn about **N-gram Speculation in LLMs**, a simple trick that makes a language model write its answer faster by guessing the next few words from the text it has already seen.

We will cover the following:

- How an LLM generates text
- Why generating text is slow
- What is Speculative Decoding
- The cost of a draft model
- What is an N-gram
- What is N-gram Speculation
- N-gram Speculation step by step
- Why the output stays exactly the same
- Where it works well and where it fails
- N-gram Speculation vs Draft Model Speculative Decoding

**Read here:** [N-gram Speculation in LLMs](https://outcomeschool.com/blog/n-gram-speculation-in-llms)

---

## Continuous Batching in LLMs

In this blog, we will learn about **Continuous Batching**, a technique that lets LLM servers handle many more users at the same time by keeping the GPU busy at every single step of generation.

We will cover the following:

- Quick Recap: How an LLM Generates Tokens
- Why Batching Matters for LLMs
- The Old Way: Static Batching
- The Problem with Static Batching
- What is Continuous Batching?
- The Ride-Share Analogy
- How Continuous Batching Works Step by Step
- A Numeric Example
- Real Numbers and Speedup
- Benefits of Continuous Batching
- A Few Important Notes
- Quick Summary

**Read here:** [Continuous Batching in LLMs](https://outcomeschool.com/blog/continuous-batching-in-llms)

---

## Prompt Caching

In this blog, we will learn about how Prompt Caching works. We will also see why we need it, how it actually works inside a large language model, and where it is used in real systems like AI assistants and agents.

We will cover the following:

- What is a prompt
- A quick recap of how an LLM reads a prompt
- What is Prompt Caching
- Why we need Prompt Caching
- The core idea behind Prompt Caching
- The exact-prefix rule
- Cache write vs cache read and TTL
- What we should put in the cache
- The benefits of Prompt Caching
- Prompt Caching in the real world

**Read here:** [How does Prompt Caching work?](https://outcomeschool.com/blog/how-does-prompt-caching-work)

---

## Prefill vs Decode: LLM Inference Optimization

In this blog, we will learn about Prefill vs Decode, the two phases of LLM inference, and how understanding them helps us optimize the speed of an LLM. We will also see how the prefill and decode phases work, how the KV cache connects them, how they differ and when to use which one based on our use case, and how we optimize each phase to make an LLM faster.

We will cover the following:

- The two phases: Prefill and Decode
- Prefill explained in simple words
- Decode explained in simple words
- A diagram of the two phases and the KV cache flow
- The KV cache as the bridge between the two phases
- A step-by-step walkthrough of a few decode steps
- Prefill vs Decode comparison table
- Why this split matters: compute-bound vs memory-bound
- The key metrics: TTFT, TPOT, throughput, and end-to-end latency
- Optimization techniques mapped to each phase

**Read here:** [Prefill vs Decode: LLM Inference Optimization](https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization)

---

## Prefill-Decode Disaggregation

In this blog, we will learn about **Prefill-Decode Disaggregation**, a way of running a large language model where the reading of the prompt and the writing of the answer happen on separate machines.

We will cover the following:

- How an LLM answers a request
- What is the KV Cache?
- Prefill is compute-heavy, Decode is memory-heavy
- The problem when both run on the same GPU
- TTFT vs TPOT
- The naive approaches and their issues
- What is Prefill-Decode Disaggregation?
- How Prefill-Decode Disaggregation works
- Walkthrough of one request
- Advantages of Prefill-Decode Disaggregation
- Disadvantages of Prefill-Decode Disaggregation
- Where it works well and where it is overkill
- Co-located vs Disaggregated serving

**Read here:** [Prefill-Decode Disaggregation](https://outcomeschool.com/blog/prefill-decode-disaggregation)

---

## How does vLLM work?

In this blog, we will learn about how vLLM works. We will also see why we need it, how it manages memory so cleverly, and where it is used in the real world to serve large language models to many users at once.

We will cover the following:

- What is serving an LLM
- A quick recap of prefill, decode, and the KV cache
- The problem: the KV cache eats GPU memory
- Why naive serving wastes memory
- What is vLLM
- PagedAttention, the core idea
- How PagedAttention shares memory
- Continuous batching
- The OpenAI-compatible API server
- The benefits of vLLM
- vLLM in the real world

**Read here:** [How does vLLM work?](https://outcomeschool.com/blog/how-does-vllm-work)

---

## How does SGLang work?

In this blog, we will learn about how SGLang works. We will also see what problem it solves, how it makes serving large language models faster, and the clever ideas that make it special.

We will cover the following:

- What is SGLang
- RadixAttention: the heart of SGLang
- How RadixAttention reuses past work
- The frontend language of SGLang
- Continuous batching in SGLang
- Structured output and faster decoding
- More powerful features of SGLang
- How SGLang compares to vLLM

**Read here:** [How does SGLang work?](https://outcomeschool.com/blog/how-does-sglang-work)

---

## How does TensorRT-LLM work?

In this blog, we will learn about how TensorRT-LLM works, NVIDIA's own engine that squeezes the highest possible speed out of an NVIDIA GPU when it runs a large language model.

We will cover the following:

- What is inference
- What is a GPU and what is a kernel
- The problem: the GPU spends its time on the wrong things
- What is TensorRT-LLM
- The big idea: prepare the model ahead of time
- The build step: from a model to an engine
- Kernel fusion
- Quantization
- Custom attention kernels
- The paged KV cache
- In-flight batching
- CUDA graphs
- Speculative decoding
- Running one model across many GPUs
- How we actually serve the model
- The PyTorch backend, the newer and easier path
- The full journey of one request
- TensorRT-LLM vs vLLM
- Where it works well and where it fails

**Read here:** [How does TensorRT-LLM work?](https://outcomeschool.com/blog/how-does-tensorrt-llm-work)

---

## How does Ollama work?

In this blog, we will learn about how Ollama works, the free tool that lets us download and run LLMs on our own computer with one simple command. We will also see why model files must be shrunk before they fit on a laptop, how Ollama's client and server talk to each other, and how models are loaded onto the CPU and GPU.

We will cover the following:

- What does running an LLM locally mean?
- What is Ollama?
- The big problem: models are huge
- Quantization and the GGUF file format
- The architecture: client and server
- What happens when we run a model?
- How models are downloaded and stored
- How the model runs on CPU and GPU
- What is a Modelfile?
- Using Ollama from code through its API
- Where it works well and where it fails

**Read here:** [How does Ollama work?](https://outcomeschool.com/blog/how-does-ollama-work)

---

## How do CUDA Kernels work?

In this blog, we will learn about how CUDA Kernels work, the small programs that run on a GPU and do the heavy lifting behind almost every modern AI model.

We will cover the following:

- Why do we need a GPU?
- What is CUDA?
- What is a CUDA Kernel?
- Threads, Blocks, and Grids
- Host and Device
- Writing our first CUDA Kernel
- How a thread finds its own work
- What happens inside the GPU when a kernel runs
- Memory in CUDA
- Why CUDA Kernels matter for AI
- Where CUDA Kernels work well and where they fail

**Read here:** [How do CUDA Kernels work?](https://outcomeschool.com/blog/how-do-cuda-kernels-work)

---

## How does an LPU work?

In this blog, we will learn about how an **LPU** works, the chip that was built for one single job, running a large language model that is already trained and producing text as fast as possible.

We will cover the following:

- What is an LPU
- How an LLM writes text, one token at a time
- The real bottleneck is memory, not math
- Why a GPU struggles here
- Keeping the model on the chip
- Removing all the guesswork with a compiler
- A network that never waits
- What happens when we send a prompt
- Where an LPU works well and where it does not
- LPU vs GPU

**Read here:** [How does an LPU work?](https://outcomeschool.com/blog/how-does-an-lpu-work)

---

## Frequently Asked Questions

### Does Speculative Decoding reduce the quality of the output?

No. In Speculative Decoding, a small draft model and a big target model work together to produce tokens faster. The rejection sampling math guarantees no quality loss. It gives a speedup of around 2 to 3 times.

### Can we speed up generation without a separate draft model?

Yes. Medusa gives the model several extra heads that guess multiple future tokens at once, so it does not need a draft model. N-gram Speculation guesses the next few words from the text the model has already seen.

### What is the difference between the prefill and decode phases?

Prefill and decode are the two phases of LLM inference. Prefill reads the prompt and is compute-heavy, while decode writes the answer and is memory-heavy. The KV cache acts as the bridge between the two phases. Prefill-Decode Disaggregation goes one step further and runs these two phases on separate machines.

### Which techniques help an LLM server handle more users at the same time?

Paged Attention and Continuous Batching both help here. Paged Attention solves the memory waste problem of the KV Cache, allowing LLMs to serve many more users at the same time. Continuous Batching keeps the GPU busy at every single step of generation, so the server can handle many more users.
