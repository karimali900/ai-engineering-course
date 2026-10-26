# Module 18: Prepare for AI Engineering Interviews

[← Course index](../../README.md) · [HTML module page](../../html/modules/m18.html)

## Contents

- [AI Engineering Key Concepts Glossary](#ai-engineering-key-concepts-glossary)
- [AI Engineering Course FAQs](#ai-engineering-course-faqs)
  - [What is the best way to learn AI Engineering?](#what-is-the-best-way-to-learn-ai-engineering)
  - [Is this AI Engineering Course free?](#is-this-ai-engineering-course-free)
  - [Do I need a Machine Learning background to start this AI Engineering Course?](#do-i-need-a-machine-learning-background-to-start-this-ai-engineering-course)
  - [How long does it take to complete this AI Engineering Course?](#how-long-does-it-take-to-complete-this-ai-engineering-course)
  - [What is the difference between an AI Engineer and a Machine Learning Engineer?](#what-is-the-difference-between-an-ai-engineer-and-a-machine-learning-engineer)
  - [What skills does an AI Engineer need?](#what-skills-does-an-ai-engineer-need)
  - [Does this AI Engineering Course cover AI Agents and Agentic AI?](#does-this-ai-engineering-course-cover-ai-agents-and-agentic-ai)
  - [Does this AI Engineering Course cover RAG?](#does-this-ai-engineering-course-cover-rag)
  - [Does this AI Engineering Course cover LLM Inference Optimization?](#does-this-ai-engineering-course-cover-llm-inference-optimization)
  - [Will this AI Engineering Course help me crack AI Engineer interviews?](#will-this-ai-engineering-course-help-me-crack-ai-engineer-interviews)
  - [Is this AI Engineering Course updated regularly?](#is-this-ai-engineering-course-updated-regularly)
  - [Who created this AI Engineering Course?](#who-created-this-ai-engineering-course)


Now that we have learned everything from Machine Learning foundations to AI Agents in production, it's time to prepare for the interviews.

- [AI Engineering Interview Questions and Answers](https://github.com/amitshekhariitbhu/ai-engineering-interview-questions)

## AI Engineering Key Concepts Glossary

Quick definitions of the most important AI Engineering terms, taken from the lessons of this AI Engineering Course. Click on any term to learn it in depth.

- **[Generative AI](https://outcomeschool.com/blog/what-is-generative-ai):** Generative AI is a type of artificial intelligence that can create new things, like text, images, audio, video, and code.
- **[Language Model](https://outcomeschool.com/blog/small-language-models-slms):** A Language Model is a neural network trained to predict the next token (i.e. the next small chunk of text) based on the previous tokens.
- **[LLM Architecture](https://outcomeschool.com/blog/evolution-of-llm-architecture):** An LLM Architecture is the blueprint of a large language model. It describes how the model reads text, how it remembers what it has read, and how it produces the next word.
- **[Tokenization](https://outcomeschool.com/blog/tokenization-in-llms):** The first step is to break the text into small pieces called tokens. Each token is then converted into a number. This process of breaking text into tokens is called tokenization.
- **[BPE (Byte Pair Encoding)](https://outcomeschool.com/blog/bpe-in-llms):** BPE (Byte Pair Encoding) is a tokenization algorithm that breaks text into pieces that are somewhere between characters and words.
- **[Embedding](https://outcomeschool.com/blog/what-are-embeddings):** An embedding is a list of numbers that represents the meaning of something, arranged so that things with similar meaning get similar numbers.
- **[Transformer](https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers):** A Transformer is the architecture behind most modern AI models that work with language.
- **[Self Attention](https://outcomeschool.com/blog/self-attention-in-transformers):** Self Attention is a mechanism that allows every token in a sequence to look at every other token in the same sequence, including itself, to understand the context.
- **[Multi-Head Attention](https://outcomeschool.com/blog/multi-head-attention-in-transformers):** Multi-Head Attention is a mechanism that runs many Self Attention operations in parallel, each with its own set of Q, K, and V projections, and then combines their outputs into a single richer representation.
- **[Grouped-Query Attention (GQA)](https://outcomeschool.com/blog/grouped-query-attention):** Grouped-Query Attention (GQA) is a strategy where heads are divided into groups, and all heads within a group share the same Key and Value, while each head still has its own Query.
- **[Gradient Descent](https://outcomeschool.com/blog/math-behind-gradient-descent):** Gradient Descent means going downward in the direction of the steepest slope.
- **[Backpropagation](https://outcomeschool.com/blog/math-behind-backpropagation):** Backpropagation is a method used to calculate how much each weight in a neural network contributed to the error, so that we can adjust those weights to reduce the error.
- **[Reinforcement Learning](https://outcomeschool.com/blog/reinforcement-learning):** Reinforcement Learning, often called RL, is a type of machine learning where an Agent learns to make a sequence of decisions by interacting with an Environment, with the goal of maximizing a Reward over time.
- **[Contrastive Learning](https://outcomeschool.com/blog/contrastive-learning):** Contrastive Learning is a way of teaching a model to learn good representations of data by comparing things. The model learns to pull similar things close to each other and push dissimilar things far apart in a representation space.
- **[Top-p Sampling](https://outcomeschool.com/blog/how-do-top-k-and-top-p-sampling-work):** Top-p Sampling is a decoding strategy in which we keep the smallest group of top tokens whose probabilities add up to at least p, throw away all the others, and then pick randomly from that group.
- **[Token Streaming](https://outcomeschool.com/blog/how-does-token-streaming-work):** Token streaming is a technique where the server sends the model's reply to us piece by piece, as each piece is produced, instead of waiting for the whole reply to be ready.
- **[Lost in the Middle](https://outcomeschool.com/blog/lost-in-the-middle-problem-in-llms):** The Lost in the Middle problem is the behaviour where an LLM pays strong attention to the information placed at the beginning and at the end of a long input, and pays very less attention to the information placed in the middle.
- **[Large Reasoning Model (LRM)](https://outcomeschool.com/blog/large-reasoning-models):** Large Reasoning Model = A Large Language Model that is trained to think first, and answer later.
- **[Diffusion Language Model](https://outcomeschool.com/blog/how-do-diffusion-language-models-dlms-work):** A Diffusion Language Model is a type of AI model that writes text by starting from a piece of pure gibberish and slowly cleaning it up into a clear, meaningful sentence.
- **[Fine-tuning](https://outcomeschool.com/blog/how-does-fine-tuning-work):** Fine-tuning is the process of taking a model that is already trained and training it a little more on our own specific data so that it becomes good at our specific task.
- **[LoRA](https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms):** LoRA is a way to fine-tune a large model without updating all of its weights. Instead of changing the original weight matrix, we keep it frozen and learn a tiny pair of extra matrices on the side.
- **[Knowledge Distillation](https://outcomeschool.com/blog/how-does-knowledge-distillation-work):** Knowledge Distillation is a technique where we train a small model to copy the behavior of a large model.
- **[Continual Learning](https://outcomeschool.com/blog/continual-learning-in-llms):** Continual Learning is the ability of a model to keep learning new information over time, without forgetting what it has already learned.
- **[RLHF](https://outcomeschool.com/blog/reinforcement-learning-from-human-feedback-rlhf):** RLHF (Reinforcement Learning from Human Feedback) is a training technique where we teach a Large Language Model (LLM) to produce responses that humans prefer, by collecting human preferences and converting them into a reward signal that guides further training.
- **[Chain-of-Thought (CoT) Prompting](https://outcomeschool.com/blog/how-does-chain-of-thought-prompting-work):** Chain-of-Thought (CoT) Prompting is a technique where we ask the model to write out its reasoning steps before giving the final answer.
- **[Tree of Thoughts](https://outcomeschool.com/blog/how-does-tree-of-thoughts-work):** Tree of Thoughts is a technique where the model explores many reasoning paths like the branches of a tree, judges each step, and drops or backtracks from the bad ones, instead of following a single straight chain of thought.
- **[Prompt Chaining](https://outcomeschool.com/blog/how-does-prompt-chaining-work):** Prompt Chaining is a way of breaking one big task into smaller prompts, where the output of one prompt becomes the input of the next prompt.
- **[Prompt Caching](https://outcomeschool.com/blog/how-does-prompt-caching-work):** Prompt Caching is a technique where the model saves the work it already did for a repeated part of a prompt, so that next time it can reuse that saved work instead of doing it all over again.
- **[Context Engineering](https://outcomeschool.com/blog/context-engineering):** Context Engineering is the practice of designing, organizing, and managing everything that goes into an LLM's context window so that the model can do its task reliably.
- **[Context Compaction](https://outcomeschool.com/blog/how-does-context-compaction-work):** Context compaction is the technique of shrinking the old conversation into a short summary, so the important facts stay while the box gets free space again.
- **[RAG (Retrieval-Augmented Generation)](https://outcomeschool.com/blog/how-does-hyde-work):** RAG stands for Retrieval-Augmented Generation. It is a way to make an AI model answer using our own documents instead of only using what it already knows.
- **[Chunk](https://outcomeschool.com/blog/chunking-strategies-for-rag):** A chunk is a small piece of text that we cut out from a bigger document.
- **[Hybrid Search](https://outcomeschool.com/blog/how-does-hybrid-search-work):** Hybrid Search is a technique that combines keyword search and semantic search, and merges their results into one final ranked list.
- **[Reranker](https://outcomeschool.com/blog/how-does-a-reranker-work):** A Reranker is a model that takes a list of documents and reorders them, putting the most relevant ones at the top for a given question.
- **[Semantic Caching](https://outcomeschool.com/blog/how-does-semantic-caching-work):** Semantic Caching is a cache that matches questions by their meaning instead of their exact words.
- **[Agentic RAG](https://outcomeschool.com/blog/agentic-rag):** Agentic RAG is a system where an AI Agent drives the retrieval process.
- **[AI Agent](https://outcomeschool.com/blog/ai-agent):** AI Agent = An LLM + Instructions + Tools + Memory + A loop that runs until the goal is achieved.
- **[Function Calling](https://outcomeschool.com/blog/how-does-function-calling-work-in-llms):** Function Calling is a way to let an LLM use external tools, APIs, and functions to get things done. It is also called tool calling, and both names mean the same thing.
- **[ReAct Agent](https://outcomeschool.com/blog/react-agent):** A ReAct Agent is an AI Agent built using the ReAct (Reasoning + Acting) pattern - the most common pattern for building AI Agents.
- **[MCP (Model Context Protocol)](https://outcomeschool.com/blog/what-is-mcp-model-context-protocol):** MCP, which stands for Model Context Protocol, is an open standard that defines one common way for AI applications to connect to outside tools and data.
- **[Agent Skill](https://outcomeschool.com/blog/what-are-agent-skills):** An Agent Skill is a folder of instructions, and optionally scripts and reference files, that an AI agent loads by itself only when the task actually needs it.
- **[OKF (Open Knowledge Format)](https://outcomeschool.com/blog/what-is-okf-open-knowledge-format):** OKF, which stands for Open Knowledge Format, is an open standard for writing down what an organization knows about its data and systems, as a folder of plain markdown files, so that any AI agent or any tool can read that knowledge without custom work.
- **[AI SubAgent](https://outcomeschool.com/blog/ai-subagents):** An AI SubAgent is a smaller, specialized agent that works under a main agent to handle a specific part of a larger task.
- **[AI Orchestration](https://outcomeschool.com/blog/ai-orchestration):** AI Orchestration is the process of coordinating multiple AI components, such as LLMs, tools, data sources, and agents, to work together to finish a complex task.
- **[Loop Engineering](https://outcomeschool.com/blog/what-is-loop-engineering):** Loop Engineering is the practice of designing the repeating cycle that an AI agent runs, so that the agent keeps making real progress on a task and stops at the right moment with the right result.
- **[Graph Engineering](https://outcomeschool.com/blog/what-is-graph-engineering):** Graph Engineering is the practice of designing an AI system as a graph, where every step of the work is a node and every path from one step to another step is an edge.
- **[LangChain](https://outcomeschool.com/blog/how-does-langchain-work):** LangChain is a framework that helps us build applications powered by Large Language Models.
- **[LangGraph](https://outcomeschool.com/blog/how-does-langgraph-work):** LangGraph is a framework that helps us build applications powered by an LLM, where the work is organized as a graph of steps.
- **[Claude Code](https://outcomeschool.com/blog/how-does-claude-code-work):** Claude Code is a coding agent from Anthropic that runs in the terminal. We give it a task in plain English, and it completes the task by reading our code, editing files, running commands, and checking its own work.
- **[Prefill](https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization):** Prefill is the phase where the model reads and processes your entire input prompt in one single pass and produces the very first output token.
- **[KV Cache Compression](https://outcomeschool.com/blog/kv-cache-compression):** KV Cache Compression is the set of techniques that make the KV Cache smaller while keeping the quality of the model output almost the same.
- **[Paged Attention](https://outcomeschool.com/blog/paged-attention-in-llms):** Paged Attention is a technique that manages KV Cache memory more efficiently by breaking it into small, fixed-size blocks called pages.
- **[Continuous Batching](https://outcomeschool.com/blog/continuous-batching-in-llms):** Continuous Batching is a way of running batches where the server does not wait for the whole batch to finish. The moment any request in the batch finishes, the server immediately replaces it with a new request that is waiting in the queue.
- **[Speculative Decoding](https://outcomeschool.com/blog/n-gram-speculation-in-llms):** Speculative Decoding is a technique where we first guess the next few tokens quickly, and then ask the big model to verify all those guesses in one single run.
- **[Model Quantization](https://outcomeschool.com/blog/how-does-model-quantization-work):** Model Quantization is the process of storing and computing a model's numbers at lower precision, so the model takes less memory and runs faster.
- **[GGUF](https://outcomeschool.com/blog/how-does-gguf-work):** GGUF is a single file format that stores everything needed to run a large language model for local inference, all in one self-contained file.
- **[Ollama](https://outcomeschool.com/blog/how-does-ollama-work):** Ollama is an open-source tool that makes it easy to download, run, and manage LLMs on our own computer.
- **[vLLM](https://outcomeschool.com/blog/how-does-vllm-work):** vLLM is a high-throughput engine for serving LLMs. It is built to serve as many requests as possible on a GPU by managing the KV cache memory very efficiently.
- **[LLM Evaluation](https://outcomeschool.com/blog/llm-evaluation):** LLM Evaluation is the process of measuring how well a Large Language Model performs on the tasks we expect it to do.
- **[LLM as a Judge](https://outcomeschool.com/blog/llm-as-a-judge):** LLM as a Judge is a technique where we use a large language model to evaluate the output of another large language model.
- **[AI Agent Observability](https://outcomeschool.com/blog/ai-agent-observability):** AI Agent Observability is the practice of recording and understanding everything an AI Agent does internally, step by step, so that we can see why it behaved the way it did.
- **[LLM Guardrails](https://outcomeschool.com/blog/how-do-llm-guardrails-work):** LLM guardrails are safety checks that sit around an LLM to control what goes in and what comes out.
- **[Prompt Injection](https://outcomeschool.com/blog/prompt-injection-in-llms):** Prompt Injection is an attack where someone slips their own instructions into the text that an AI application sends to the model, so that the model follows the attacker's instructions instead of the developer's instructions.
- **[Diffusion Model](https://outcomeschool.com/blog/diffusion-models):** A Diffusion Model is a type of AI model that learns to create new data, such as images, by starting from pure random noise and slowly cleaning it up step by step until a clear image appears.
- **[Variational Autoencoder (VAE)](https://outcomeschool.com/blog/variational-autoencoders):** A Variational Autoencoder, also called a VAE, is a special type of Autoencoder that learns a smooth and organized latent space, so that we can pick any random point from it and generate brand new, meaningful data.
- **[LPU](https://outcomeschool.com/blog/how-does-an-lpu-work):** An LPU is a chip that is built for one single job, running a large language model that is already trained, and producing text as fast as possible.
- **[LLM Routing](https://outcomeschool.com/blog/llm-routing):** LLM Routing is the practice of choosing the right LLM for each user query, instead of sending every query to the same LLM.
- **[Voice AI Agent](https://outcomeschool.com/blog/design-a-real-time-voice-ai-agent):** A Voice AI Agent is a software program that we can talk to using our voice, and it talks back to us, just like a phone call with a human, but the one on the other side is an AI.
- **[World Model](https://outcomeschool.com/blog/how-do-world-models-work):** A World Model is an AI that learns an approximate internal copy of how an environment behaves, so that it can predict what happens next, given the current state and an action.
- **[Recursive Self-Improvement](https://outcomeschool.com/blog/what-is-recursive-self-improvement-rsi):** Recursive Self-Improvement is a process in which an AI system improves its own abilities, and then the improved version improves itself further, and this cycle keeps repeating.

## AI Engineering Course FAQs

### What is the best way to learn AI Engineering?

The best way to learn AI Engineering is to follow a structured path in the right order: Machine Learning foundations, then Deep Learning, then the Transformer architecture, then LLMs, then fine-tuning, RAG, AI Agents, LLM Inference, Evaluation, and AI System Design. This AI Engineering Course follows exactly this order, and every lesson has a detailed blog that explains one concept in simple words.

### Is this AI Engineering Course free?

Yes. This AI Engineering Course is completely free. Every lesson is a free blog. No sign-up. No paywall.

### Do I need a Machine Learning background to start this AI Engineering Course?

No. This AI Engineering Course starts from the very basics of Machine Learning. We only need basic programming knowledge, preferably Python, and high-school level math. Everything else is explained inside the lessons.

### How long does it take to complete this AI Engineering Course?

It depends on our pace. If we read one or two lessons every day and make notes, we can complete the full AI Engineering Course in around 3 to 4 months. The most important thing is to understand every concept deeply, not to finish fast.

### What is the difference between an AI Engineer and a Machine Learning Engineer?

A Machine Learning Engineer mostly focuses on training, tuning, and deploying models. An AI Engineer mostly focuses on building real products and systems on top of models, especially LLMs, using techniques like prompt engineering, context engineering, RAG, AI Agents, fine-tuning, and LLM inference optimization. The two roles overlap a lot, and this AI Engineering Course covers the foundations of both.

### What skills does an AI Engineer need?

An AI Engineer needs to understand how LLMs work from the inside (Transformers, attention, tokenization), how to adapt them (prompting, context engineering, fine-tuning, LoRA), how to give them knowledge (RAG, vector search), how to make them take actions (AI Agents, function calling, MCP), how to run them fast and cheap (LLM inference, KV cache, quantization, vLLM), how to measure them (evaluation, observability), and how to keep them safe (guardrails, prompt injection defense). All of these are covered in this AI Engineering Course.

### Does this AI Engineering Course cover AI Agents and Agentic AI?

Yes. Module 10 and Module 11 of this AI Engineering Course cover AI Agents in depth: the agent loop, function calling, ReAct, Plan-and-Execute, Reflection, agent memory, MCP, Agent Skills, multi-agent systems, SubAgents, orchestration, computer-use agents, browser agents, harness engineering, loop engineering, graph engineering, LangChain, LangGraph, Claude Code, and Cursor.

### Does this AI Engineering Course cover RAG?

Yes. Module 9 of this AI Engineering Course covers RAG from the basics to the advanced: vector databases, ANN search, semantic search, hybrid search, rerankers, ColBERT, chunking strategies, Contextual Retrieval, HyDE, query rewriting, multi-query retrieval, embedding cache, semantic caching, Agentic RAG, GraphRAG, and Vectorless RAG.

### Does this AI Engineering Course cover LLM Inference Optimization?

Yes. Module 12 of this AI Engineering Course covers LLM Inference Engineering: prefill vs decode, prefill-decode disaggregation, KV cache, KV cache compression, paged attention, continuous batching, speculative decoding, Medusa, EAGLE, quantization, GGUF, llama.cpp, Ollama, vLLM, SGLang, and TensorRT-LLM.

### Will this AI Engineering Course help me crack AI Engineer interviews?

Yes. This AI Engineering Course covers the concepts that are asked in AI Engineer, Gen AI Engineer, LLM Engineer, and Machine Learning Engineer interviews. After completing the course, use [AI Engineering Interview Questions and Answers](https://github.com/amitshekhariitbhu/ai-engineering-interview-questions) to practice.

### Is this AI Engineering Course updated regularly?

Yes. AI is moving very fast, and so is this course. We keep adding new lessons, new blogs, and new videos.

### Who created this AI Engineering Course?

This AI Engineering Course is prepared and maintained by Amit Shekhar, Founder of [Outcome School](https://outcomeschool.com). He has taught and mentored many developers, and their efforts landed them high-paying tech jobs, helped many tech companies in solving their unique problems, and created many open-source libraries being used by top companies.

---

*Fetched 2026-10-24. For personal offline study only; see [NOTICE.md](../../NOTICE.md).*
