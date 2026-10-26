---
title: What is Agentic RAG? How It Works and When to Use It
module: 9
module_title: Vector Search and Retrieval-Augmented Generation (RAG)
lesson: '9.13'
source: https://outcomeschool.com/blog/agentic-rag
published: May 1, 2026
tags:
- ai-agent
- llm
- ai
- machine-learning
videos:
- title: Agentic RAG Explained
  url: https://www.youtube.com/watch?v=6nSegpuWJVw
fetched: '2026-10-24'
words: 2788
reading_time: 14
status: full
---
# What is Agentic RAG? How It Works and When to Use It

> **Module 9 · Lesson 9.13**  
> Source: [Outcome School](https://outcomeschool.com/blog/agentic-rag) · Published: May 1, 2026 · Reading time: ~14 min · Tags: `ai-agent`, `llm`, `ai`, `machine-learning`
> Video: [Agentic RAG Explained](https://www.youtube.com/watch?v=6nSegpuWJVw)

---

![Agentic RAG](../../assets/images/09-09-13-what-is-agentic-rag-how-it-works-and-when-to-use-it/agentic-rag.png)

Agentic RAG is a type of RAG where an AI Agent decides how to search for information, step by step, instead of doing just one fixed search before answering.

In this blog, we will learn about Agentic RAG - what it is, why standard RAG falls short, the agentic RAG loop, the three building blocks, the common patterns, when to use it, and the limitations to keep in mind.

A hard question often needs more than one search. Some of those searches need different sources. Some depend on what the previous search found. Standard RAG cannot do any of this. Agentic RAG can.

**Agentic RAG = Agentic + RAG**

We will cover the following in this blog:

- The Big Picture
- A Quick Recap of RAG
- A Quick Recap of AI Agent
- Why Standard RAG Falls Short
- What is Agentic RAG?
- The Agentic RAG Loop
- The Three Building Blocks
- A Walkthrough with a Real Example
- Common Patterns of Agentic RAG
- Standard RAG vs Agentic RAG
- When to Use Agentic RAG
- Limitations of Agentic RAG
- Quick Summary

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

The best way to think about this is with a real-world analogy. Suppose we want to find an answer in a big library.

**Standard RAG is like a librarian who fetches one book.** We hand over the question. The librarian picks the book that matches the words best, gives it to us, and the LLM reads it to write the answer. One shot. Done.

**Agentic RAG is like a researcher.** The researcher reads the question, thinks about where to look, picks a section, reads it, and decides whether the answer is in there. If not, the researcher goes back, picks a different shelf, runs a follow-up search, and keeps going until the answer is found.

The librarian flow is fast but cannot adapt to the question. The researcher flow is slower but can handle questions that need many steps.

This is exactly the difference between Standard RAG and Agentic RAG. Agentic RAG turns the one-shot retrieval into a loop driven by an [AI Agent](https://outcomeschool.com/blog/ai-agent) that keeps working until it can answer well.

In simple words:

**Agentic RAG = RAG + an AI Agent that controls the retrieval steps.**

## A Quick Recap of RAG

Before jumping into Agentic RAG, we must quickly recall what RAG is.

**RAG** stands for **Retrieval-Augmented Generation**. The flow is simple:

- The user asks a question.
- We convert the question into an [embedding](https://outcomeschool.com/blog/what-are-embeddings).
- We search a [vector database](https://outcomeschool.com/blog/how-does-a-vector-database-work) and pull the top relevant [chunks](https://outcomeschool.com/blog/chunking-strategies-for-rag).
- We pass those chunks plus the question to the LLM.
- The LLM generates the final answer.

One clever twist on the second step is [HyDE](https://outcomeschool.com/blog/how-does-hyde-work), where instead of embedding the raw question, we first ask the model to write a hypothetical answer and search with that - a trick that often retrieves better chunks.

We can see this flow as below:

```
User Question
     |
     v
+------------------+
|     Embed        |
|   the question   |
+------------------+
     |
     v
+------------------+
|  Vector Search   |
|  (top-k chunks)  |
+------------------+
     |
     v
+------------------+
|       LLM        |
|  (generate)      |
+------------------+
     |
     v
  Final Answer
```

Here, we can see that the flow is a straight line. There are no decisions in the middle. Retrieve once. Generate once. Return. This is the librarian flow.

In a production RAG system, a Reranker often sits between retrieval and the LLM to reorder those top chunks by true relevance. We have a detailed blog on [how a Reranker works](https://outcomeschool.com/blog/how-does-a-reranker-work) that covers this step end to end.

## A Quick Recap of AI Agent

Now, let's recall what an AI Agent is.

An [AI Agent](https://outcomeschool.com/blog/ai-agent) is a system that uses an LLM as its brain and runs in a loop. The LLM plans the next step, recommends a tool, observes the result, and decides what to do next. It is not a one-shot prompt. It is a thinking loop with access to tools. This is the researcher in our analogy.

## Why Standard RAG Falls Short

Standard RAG works for simple questions. But the moment the question gets harder, it breaks down. The reason is simple. Our librarian only knows how to match words. The librarian cannot think, cannot ask follow-up questions, and cannot decide where to look.

Let's see the problems this causes.

**Problem 1: Multi-hop questions.**

Suppose the user asks:

> "What was the Q4 revenue of the company that acquired Acme in 2023?"

To answer this, we first need to find out which company acquired Acme in 2023. Only after that, we can retrieve the Q4 revenue of that company. One single retrieval cannot do this. The librarian sees the long question and tries to find one matching book. There is no such book.

**Problem 2: Ambiguous queries.**

The user asks: "What about the new policy?"

The retrieval system has no idea which policy. Standard RAG will pull random chunks and the answer will be wrong. The librarian does not stop to ask "which policy?". The librarian just matches words and hands over a book.

**Problem 3: Multiple data sources.**

Some questions need a SQL database. Some need a vector store. Some need a live web search. Standard RAG hits one source. It cannot pick the right one. Our librarian only knows one library. If the answer lives in a database, on the web, or in a graph of relationships, the librarian cannot reach it.

**Problem 4: Bad retrieval quality.**

Sometimes the top retrieved chunks are not relevant. Standard RAG does not know this. It just passes whatever it found to the LLM. The LLM then makes up the answer. The librarian hands over whatever matched the words best, without checking if the book actually has the answer.

Do you see the problem? Standard RAG is rigid. It cannot adapt.

So, here comes **Agentic RAG** to the rescue. We replace the librarian with a researcher.

## What is Agentic RAG?

**Agentic RAG is a system where an AI Agent drives the retrieval process.** Instead of one fixed retrieve-then-generate step, the agent decides every step in a loop.

The agent decides:

- Does this question even need retrieval?
- Which tool or data source should we use?
- What should the search query look like?
- Are the retrieved chunks good enough to answer?
- Should we retrieve again with a better query?
- Should we combine results from multiple sources?
- When can we stop and write the final answer?

This is a big shift. The retrieval is no longer a fixed pipeline. It is a decision made by the agent at every step. The librarian has been replaced by the researcher.

## The Agentic RAG Loop

Let's see the loop.

```
User Question
     |
     v
+------------------+
|    AI Agent      |
|   (the LLM)      |
+------------------+
     |
     | thinks: "Do I need to retrieve?
     |          Which tool? What query?"
     v
+------------------+
|  Retrieval Tool  |
|  (vector / SQL / |
|   web / graph)   |
+------------------+
     |
     | returns chunks
     v
+------------------+
|    AI Agent      |
|   evaluates:     |
|  "Good enough?"  |
+------------------+
     |
     +--- No  --> retrieve again with a new query
     |
     +--- Yes --> generate the final answer
```

Here, we can see that the agent is in control. It loops until it has enough information.

## The Three Building Blocks

Agentic RAG has three building blocks. Let's decode each one.

**1. The Agent (The Brain)**

This is the researcher's mind. It is an LLM that does the thinking. It reads the question, plans the next step, recommends the tool, and evaluates the result.

**2. The Tools (The Hands)**

These are the resources our researcher can reach for. A real researcher uses different sources for different questions. The agent has the same options:

- **[Vector search](https://outcomeschool.com/blog/how-does-approximate-nearest-neighbor-ann-search-work):** for finding text by meaning over documents
- **Keyword search:** for exact term matches
- **SQL query:** for structured data in a database
- **Web search:** for fresh information on the internet
- **Knowledge graph query:** for relationships between entities

The agent recommends the right tool based on the question, just like a researcher walks to the right shelf.

**3. The Loop (The Workflow)**

This is the back-and-forth between the researcher's mind and the resources. The runtime that ties the agent and the tools together. It calls the agent, runs the tool the agent recommended, feeds the result back to the agent, and repeats.

Across the loop, the runtime keeps track of every past step - the actions the agent took and the results it saw. This running record is called the **scratchpad** or [**agent memory**](https://outcomeschool.com/blog/ai-agent-memory). The agent reads this record on every step so it knows what it has already tried and what it has already learned.

**Note:** The LLM inside the agent does not call the tool itself. The LLM only outputs text - the name of the tool to use and the arguments. The runtime around the LLM is what actually calls the tool and feeds the result back. This distinction is important.

## A Walkthrough with a Real Example

The best way to learn this is by taking an example.

Let's say the user asks:

> "What was the Q4 revenue of the company that acquired Acme in 2023?"

Here is how Agentic RAG handles it. Watch the agent act like a researcher.

**Step 1:** The agent reads the question. It thinks: "This is a multi-hop question. I first need to find who acquired Acme in 2023."

**Step 2:** The agent recommends the **web search** tool with the query: `company that acquired Acme in 2023`.

**Step 3:** The web search returns: "Globex acquired Acme in 2023."

**Step 4:** The agent updates its plan. Now it needs Globex's Q4 2023 revenue.

**Step 5:** The agent recommends the **vector search** tool over the internal financial reports with the query: `Globex Q4 2023 revenue`.

**Step 6:** The vector search returns chunks from Globex's Q4 financial report.

**Step 7:** The agent evaluates the chunks: "Yes, these chunks contain the revenue number. I have enough."

**Step 8:** The agent generates the final answer using the gathered information.

**Note:** In practice, the web search returns several noisy snippets. The agent reads them and pulls out the answer. We have shown a clean answer above just for the sake of understanding.

Sometimes, the agent combines results from two sources in a single step. For example, it pulls a definition from a vector store and fresh news from a web search before answering.

Standard RAG could not do this. It would have made one retrieval with the original question and failed. Agentic RAG broke the question into two steps, used two different tools, and answered correctly. The researcher did the job that the librarian could not.

Problem solved. This is the power of Agentic RAG.

The same reasoning can also replace the vector search itself. We have a detailed blog on [Vectorless RAG](https://outcomeschool.com/blog/vectorless-rag) that explains how an LLM walks the structure of a document instead of matching vectors.

## Common Patterns of Agentic RAG

Agentic RAG is a general idea. Over time, a few specific patterns have become popular. Let's quickly look at three of them.

**ReAct-style RAG.** The agent follows a ["think, act, observe" loop](https://outcomeschool.com/blog/ai-agent-loop). It thinks about what to do, takes an action like a retrieval, observes the result, and repeats. Our walkthrough above is a ReAct-style flow. We have a detailed blog on [ReAct Agent](https://outcomeschool.com/blog/react-agent) that explains this pattern in depth.

**Self-RAG.** The agent grades its own retrievals on two things - **relevance** (are the chunks about the question?) and **support** (do the chunks actually back up the answer?). If not, the agent skips or trusts them less before generating. Self-RAG is about quality control on what the agent fetches.

**Corrective RAG (also called CRAG).** The agent recommends a fallback source when the main retrieval is bad. For example, if the vector search returns nothing useful, the agent falls back to a live web search. CRAG is about robustness when the main source fails.

All three share the same core idea. The agent decides what happens at every step. They differ in what they focus on - reasoning style, quality control, or robustness.

## Standard RAG vs Agentic RAG

Let me tabulate the differences between Standard RAG and Agentic RAG for your better understanding so that you can decide which one to use based on your use case.

| Aspect | Standard RAG | Agentic RAG |
| --- | --- | --- |
| Flow | Fixed pipeline | Dynamic loop |
| Number of retrievals | One | Many, as needed |
| Tools used | One (usually vector search) | Many (vector, SQL, web, and etc.) |
| Query rewriting | No | Yes |
| Quality check on retrieved chunks | No | Yes |
| Multi-hop questions | Cannot handle | Can handle |
| Latency | Low | Higher |
| Cost | Low | Higher |
| Complexity to build | Simple | More complex |

## When to Use Agentic RAG

Use Agentic RAG when:

- The user asks **multi-hop questions** that need information from more than one search.
- The data lives in **multiple sources** (vector DB, SQL, web, files).
- The questions are **ambiguous** and need [rewriting](https://outcomeschool.com/blog/how-do-query-rewriting-and-multi-query-retrieval-work) before retrieval.
- The **quality of retrieval matters more than latency**, like in research, legal, or medical use cases.
- The system needs to **decide if retrieval is even needed**. For greetings or small talk, no retrieval is needed.

Use Standard RAG when:

- The questions are simple and direct.
- The data lives in one place.
- Latency and cost matter more than depth.

## Limitations of Agentic RAG

A researcher takes more time and costs more than a librarian. The same is true for Agentic RAG. It is powerful, but it has trade-offs.

- **Higher latency.** Each loop step is one or more LLM calls. The user waits longer.
- **Higher cost.** Each loop step is one LLM call, and the tool results are fed back into the next prompt. More steps mean more tokens, which means a higher API bill.
- **Harder to debug.** The agent's decisions are not fixed. The same question can take different paths on different runs.
- **Can loop too long.** Without a stopping rule, the agent can keep retrying and never stop. Common stopping rules are: the LLM signals it is done, the agent's confidence in the answer is high enough, or a max step count is hit.
- **More moving parts.** We need to design tools, prompts, [evaluation steps](https://outcomeschool.com/blog/ai-agent-evaluation), and stopping rules. A simple system becomes a complex one.

We must keep these trade-offs in mind while designing the system.

## Quick Summary

Let's recap what we have learned:

- **Standard RAG** is a fixed pipeline: retrieve once, generate once.
- **Agentic RAG** is a loop where an AI Agent drives every step of retrieval.
- The agent decides when to retrieve, what to retrieve, from where, and whether to retrieve again.
- It has three parts: the **agent**, the **tools**, and the **loop**, with a **scratchpad** that tracks the past steps.
- Common patterns are **ReAct-style RAG**, **Self-RAG**, and **Corrective RAG (CRAG)**.
- It shines on **multi-hop questions, multiple data sources, and ambiguous queries**.
- The trade-offs are **higher latency, higher cost, and more complexity**.

Standard RAG is the librarian who fetches one book. Agentic RAG is the researcher who keeps digging until the answer is found. We use Agentic RAG when Standard RAG is not enough.

## Frequently Asked Questions

### Is Agentic RAG always better than standard RAG?

No. Agentic RAG is not always the better choice. It has higher latency, higher cost, and more complexity to build. When the questions are simple and direct, the data lives in one place, and latency and cost matter more than depth, standard RAG is the better fit.

### Does the LLM in Agentic RAG call the search tools itself?

No. The LLM only outputs text, which is the name of the tool to use and its arguments. The runtime around the LLM actually calls the tool and feeds the result back to the agent. This distinction is important when we design the system.

### How does an Agentic RAG agent know when to stop searching?

The agent stops when a stopping rule is met. Common stopping rules are that the LLM signals it is done, the agent's confidence in the answer is high enough, or a max step count is hit. Without a stopping rule, the agent can keep retrying and never stop.

### Does every question need retrieval in Agentic RAG?

No. The agent first decides whether the question even needs retrieval. For greetings or small talk, no retrieval is needed, so the agent can answer directly. This is one of the reasons to use Agentic RAG over a fixed pipeline that always searches.

### What is the difference between Self-RAG and Corrective RAG?

Self-RAG is about quality control, and Corrective RAG is about robustness. In Self-RAG, the agent grades its own retrievals on relevance and support before generating. In Corrective RAG, the agent falls back to another source, like a live web search, when the main retrieval is bad.
