# Module 12: LLM Inference Engineering

[← Course index](../../README.md) · [HTML module page](../../html/modules/m12.html)

In this module, we will learn how to make LLMs faster and cheaper to run. We will start with what happens during inference, then learn the caching, batching, and speculation techniques, then quantization, and finally the serving engines that put it all together.

By the end of this module, we will understand TTFT, TPOT, and throughput, and know which optimization fixes which bottleneck.

## Module videos

- [LLM Inference Optimization](https://www.youtube.com/watch?v=jV2sCj4lHYk)
- [The First-Token Latency Problem in LLMs](https://www.youtube.com/watch?v=XD8DD4cEHu0)

## Lessons

| # | Lesson | Reading time | Source |
|---:|---|---:|---|
| 12.1 | [LLM Inference Optimization](12-12-01-llm-inference-optimization.md) | ~12 min | [Outcome School](https://outcomeschool.com/blog/llm-inference-optimization) |
| 12.2 | [Prefill vs Decode: LLM Inference Optimization](12-12-02-prefill-vs-decode-llm-inference-optimization.md) | ~34 min | [Outcome School](https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization) |
| 12.3 | [What is Prefill-Decode Disaggregation in LLM Inference?](12-12-03-what-is-prefill-decode-disaggregation-in-llm-inference.md) | ~21 min | [Outcome School](https://outcomeschool.com/blog/prefill-decode-disaggregation) |
| 12.4 | [KV Cache in LLMs](12-12-04-kv-cache-in-llms.md) | ~11 min | [Outcome School](https://outcomeschool.com/blog/kv-cache-in-llms) |
| 12.5 | [What is KV Cache Compression?](12-12-05-what-is-kv-cache-compression.md) | ~20 min | [Outcome School](https://outcomeschool.com/blog/kv-cache-compression) |
| 12.6 | [What is Paged Attention in LLMs and How Does It Work?](12-12-06-what-is-paged-attention-in-llms-and-how-does-it-work.md) | ~11 min | [Outcome School](https://outcomeschool.com/blog/paged-attention-in-llms) |
| 12.7 | [What is Continuous Batching in LLMs and How Does It Work?](12-12-07-what-is-continuous-batching-in-llms-and-how-does-it-work.md) | ~18 min | [Outcome School](https://outcomeschool.com/blog/continuous-batching-in-llms) |
| 12.8 | [What is Speculative Decoding and How Does It Make LLMs Faster?](12-12-08-what-is-speculative-decoding-and-how-does-it-make-llms-faster.md) | ~19 min | [Outcome School](https://outcomeschool.com/blog/speculative-decoding) |
| 12.9 | [What is N-gram Speculation in LLMs and How Does It Speed Up Generation?](12-12-09-what-is-n-gram-speculation-in-llms-and-how-does-it-speed-up-generation.md) | ~18 min | [Outcome School](https://outcomeschool.com/blog/n-gram-speculation-in-llms) |
| 12.10 | [What is Medusa? Multi-Head Speculative Decoding Explained](12-12-10-what-is-medusa-multi-head-speculative-decoding-explained.md) | ~10 min | [Outcome School](https://outcomeschool.com/blog/decoding-medusa) |
| 12.11 | [What is EAGLE? Feature-Level Speculative Decoding Explained](12-12-11-what-is-eagle-feature-level-speculative-decoding-explained.md) | ~8 min | [Outcome School](https://outcomeschool.com/blog/decoding-eagle) |
| 12.12 | [How does Model Quantization work?](12-12-12-how-does-model-quantization-work.md) | ~20 min | [Outcome School](https://outcomeschool.com/blog/how-does-model-quantization-work) |
| 12.13 | [How does GGUF work?](12-12-13-how-does-gguf-work.md) | ~19 min | [Outcome School](https://outcomeschool.com/blog/how-does-gguf-work) |
| 12.14 | [How does llama.cpp run LLMs on everyday hardware?](12-12-14-how-does-llama-cpp-run-llms-on-everyday-hardware.md) | ~18 min | [Outcome School](https://outcomeschool.com/blog/how-does-llama-cpp-run-llms-on-everyday-hardware) |
| 12.15 | [How does Ollama work?](12-12-15-how-does-ollama-work.md) | ~16 min | [Outcome School](https://outcomeschool.com/blog/how-does-ollama-work) |
| 12.16 | [How does vLLM work?](12-12-16-how-does-vllm-work.md) | ~21 min | [Outcome School](https://outcomeschool.com/blog/how-does-vllm-work) |
| 12.17 | [How does SGLang work?](12-12-17-how-does-sglang-work.md) | ~23 min | [Outcome School](https://outcomeschool.com/blog/how-does-sglang-work) |
| 12.18 | [How does TensorRT-LLM work?](12-12-18-how-does-tensorrt-llm-work.md) | ~45 min | [Outcome School](https://outcomeschool.com/blog/how-does-tensorrt-llm-work) |

---

*18 lessons · Fetched 2026-10-24. For personal offline study only; see [NOTICE.md](../../NOTICE.md).*
