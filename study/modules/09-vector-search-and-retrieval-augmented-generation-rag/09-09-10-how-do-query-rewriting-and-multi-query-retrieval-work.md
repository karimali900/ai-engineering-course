---
title: How do Query Rewriting and Multi-Query Retrieval work?
module: 9
module_title: Vector Search and Retrieval-Augmented Generation (RAG)
lesson: '9.10'
source: https://outcomeschool.com/blog/how-do-query-rewriting-and-multi-query-retrieval-work
published: October 8, 2026
tags:
- llm
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 2779
reading_time: 14
status: full
---
# How do Query Rewriting and Multi-Query Retrieval work?

> **Module 9 · Lesson 9.10**  
> Source: [Outcome School](https://outcomeschool.com/blog/how-do-query-rewriting-and-multi-query-retrieval-work) · Published: October 8, 2026 · Reading time: ~14 min · Tags: `llm`, `ai`, `system-design`

---

![How do Query Rewriting and Multi-Query Retrieval work?](../../assets/images/09-09-10-how-do-query-rewriting-and-multi-query-retrieval-work/how-do-query-rewriting-and-multi-query-retrieval-work.png)

Query Rewriting and Multi-Query Retrieval are two ways of improving the search step of an AI system. Query Rewriting uses an LLM to turn the user's messy question into one clear search query, and Multi-Query Retrieval uses an LLM to turn the question into several different search queries, searches with all of them, and merges the results.

In this blog, we will learn about how Query Rewriting and Multi-Query Retrieval work. We will also see why the user's raw question is often a bad search query, how Query Rewriting fixes vague, follow-up, and badly worded questions, how Multi-Query Retrieval searches from many angles, how the results from many searches are merged using Reciprocal Rank Fusion, how they differ from each other, and when to use which one.

We will cover the following:

- The problem: the user's question is not a good search query
- What is Query Rewriting?
- How does Query Rewriting work?
- Types of Query Rewriting
- Query Rewriting in code
- The problem that Query Rewriting does not solve
- What is Multi-Query Retrieval?
- How does Multi-Query Retrieval work?
- How do we merge the results? Reciprocal Rank Fusion
- Multi-Query Retrieval in code
- Query Rewriting vs Multi-Query Retrieval
- Where they work well and where they fail

Let's get started.

## The problem: the user's question is not a good search query

Query Rewriting and Multi-Query Retrieval are used in the retrieval step of **RAG** (Retrieval-Augmented Generation), where we search our documents, pick the pieces of text called **[chunks](https://outcomeschool.com/blog/chunking-strategies-for-rag)** that are most related to the question, and give them to an LLM before it answers.

The flow looks like below:

```text
User question -> Retriever -> Top chunks -> LLM -> Answer
```

**If retrieval brings the wrong chunks, the LLM often gives a wrong answer.**

And retrieval depends completely on the text we search with. That text is called the **search query**.

In a simple RAG system, we search with the user's question exactly as they typed it. But real users do not type perfect search queries.

Let's see a few real situations:

- **Follow-up questions:** The user first asks, "What is the refund policy of the Pro plan?". Then they ask, "And what about the Basic one?". If we search with "And what about the Basic one?", the retriever has no idea that we are talking about refunds.
- **Vague questions:** "My thing is not working after the update." Which thing? Which update?
- **Different words:** The user asks, "How do I get my money back?", but our documents say "refund process". A keyword search does not match them.
- **Extra noise:** "Hi, hope you are well, quick question, my manager asked me, how many leaves do we get in a year?". Most of these words are not useful for search.
- **Many questions in one:** "Compare the battery life and price of phone A and phone B." This needs information from several different places.

In all these cases, the retriever brings poor chunks, and the LLM gives a poor answer.

So, here comes Query Rewriting to the rescue.

## What is Query Rewriting?

**Query Rewriting is a step where an LLM rewrites the user's question into a clear, complete, and search-friendly query before we search.**

It is like going to a big library and asking the librarian, "I want that book about the boy wizard". The librarian does not search for "boy wizard". The librarian searches for "Harry Potter". The librarian rewrote our query.

The flow now looks like below:

```text
User question -> LLM rewrites -> Clear query -> Retriever -> Top chunks -> LLM -> Answer
```

The answer is still written using the user's original question. Only the search uses the rewritten query.

## How does Query Rewriting work?

The best way to learn this is by taking an example.

**Step 1:** The user is chatting with a support bot.

```text
User: What is the refund policy of the Pro plan?
Bot:  You can get a full refund within 30 days.
User: And what about the Basic one?
```

**Step 2:** Before searching, we send the chat history and the latest question to an LLM with an instruction like below:

```text
Given the conversation and the latest question, rewrite the latest
question as a standalone search query that contains all the needed
details. Return only the query.
```

**Step 3:** The LLM returns:

```text
Refund policy of the Basic plan
```

**Step 4:** We search with "Refund policy of the Basic plan". Now, the retriever finds the right chunk about Basic plan refunds.

**Step 5:** We give that chunk and the user's question to the LLM, and it answers correctly.

## Types of Query Rewriting

Query Rewriting is one idea, but it is used in a few different ways, depending upon our use case:

- **Standalone rewriting:** Turns a follow-up question into a complete question, using the chat history. Like the refund example above. This is the most common type in chat applications.
- **Clarifying and cleaning:** Removes noise, fixes spelling, and keeps only the important words. "Hi, quick question, how many leaves do we get in a year?" becomes "Annual leave policy number of days".
- **Expanding:** Adds words that the documents are likely to use. "How do I get my money back?" becomes "refund process, return money, get refund".
- **Step-back rewriting:** Turns a very specific question into a more general one, so that we find the background information. "Why did my order #4521 get delayed in Mumbai?" becomes "Reasons for order delivery delays".

All of them follow the same pattern: an LLM changes the query, and then we search. A close cousin of these is [HyDE](https://outcomeschool.com/blog/how-does-hyde-work), where the LLM writes a hypothetical answer instead of a query, and we search with that answer.

## Query Rewriting in code

Now, let's see the code for a simple Query Rewriting step. Here, `call_llm` sends a prompt to an LLM and returns its text, and `retriever.search` searches our chunks. We are hiding their details for the sake of understanding.

```python
def rewrite_query(chat_history, question):
    prompt = f"""Given the conversation and the latest question, rewrite the
latest question as a standalone search query. Return only the query.
Conversation:
{chat_history}Latest question: {question}"""
    return call_llm(prompt).strip()
def answer(chat_history, question):
    search_query = rewrite_query(chat_history, question)
    chunks = retriever.search(search_query, top_k=5)
    return call_llm(f"Context:\n{chunks}\n\nQuestion: {question}\nAnswer:")
```

Here, we have:

- `rewrite_query` builds a prompt with the chat history and the latest question, and asks the LLM for one clean search query.
- In `answer`, we first rewrite the question, then search with the rewritten query.
- Finally, we give the found chunks and the original question to the LLM to write the answer.

Here, we can notice that the user never sees the rewritten query. It is used only for searching.

## The problem that Query Rewriting does not solve

Query Rewriting gives us one better query. But one query, however good, looks at the question from only one angle.

Let's say the user asks, "Is the new phone good for gaming?". The useful information can be in many places:

- A chunk about the processor.
- A chunk about the screen refresh rate.
- A chunk about heating and battery during long use.

A single query like "new phone gaming performance" can find the first chunk but miss the others, because they use very different words.

Also, if the LLM rewrites the query in a slightly wrong way, we have no backup. One bad rewrite means bad retrieval.

So, the question is: what if we search from many angles at the same time?

Here comes Multi-Query Retrieval into the picture.

## What is Multi-Query Retrieval?

**Multi-Query Retrieval is a method where an LLM creates several different versions of the user's question, we search with each version separately, and then we merge all the results into one list.**

It is like looking for a lost key at home. If we only look in the bedroom, we can miss it. If three family members look in the bedroom, the kitchen, and the car at the same time, the chance of finding the key is much higher.

## How does Multi-Query Retrieval work?

Let's take the same gaming example.

**Step 1:** The user asks, "Is the new phone good for gaming?".

**Step 2:** We ask the LLM to create, let say, 3 different search queries for the same question:

```text
Query 1: new phone processor and graphics performance
Query 2: new phone display refresh rate and touch response
Query 3: new phone heating and battery life during heavy use
```

**Step 3:** We search with each query separately. Each search returns its own top chunks.

```text
Query 1 -> [processor chunk, benchmark chunk, ...]
Query 2 -> [display chunk, touch chunk, ...]
Query 3 -> [battery chunk, heating chunk, ...]
```

**Step 4:** We merge all the results into one list and remove the duplicates, because the same chunk can come from more than one query.

**Step 5:** We give the merged chunks and the original question to the LLM, and it writes a complete answer covering speed, display, and battery.

The flow looks like below:

```text
                     /--> Query 1 -> Retriever -> results 1 \
User question -> LLM ---> Query 2 -> Retriever -> results 2 --> Merge -> LLM -> Answer
                     \--> Query 3 -> Retriever -> results 3 /
```

**Note:** Many systems also keep the user's original question as one of the queries, so that we never lose what a plain search would have found.

Similarly, Multi-Query Retrieval solves the "many questions in one" problem that we saw earlier. For "Compare the battery life and price of phone A and phone B", the LLM can split it into smaller questions like "phone A battery life", "phone A price", "phone B battery life", and "phone B price". Splitting a big question into smaller questions like this is called **query decomposition**.

## How do we merge the results? Reciprocal Rank Fusion

Now, the next big question is: how do we merge the lists?

The simplest way is to take all the chunks from all the lists, remove the duplicates, and keep them. This is called taking the **union**. It works, but it does not tell us which chunks are the most important.

A better way is **Reciprocal Rank Fusion**, or **RRF**. When Multi-Query Retrieval is combined with RRF, it is often called **RAG-Fusion**.

**RRF gives each chunk a score based on its position in each list, and adds these scores across all the lists.**

The formula is as below:

**RRF score of a chunk = sum over all lists of 1 / (k + rank)**

Here, `rank` is the position of the chunk in that list (1 for the top), and `k` is a constant, commonly 60.

Here, "reciprocal" just means "1 divided by". A chunk at the top of a list gets a bigger score than a chunk at the bottom. A chunk that appears in many lists collects score from each of them.

Let's see an example with 3 queries and their top 3 chunks:

```text
Query 1 -> [D2, D5, D1]
Query 2 -> [D5, D3, D2]
Query 3 -> [D5, D2, D4]
```

Now, we calculate with `k = 60`:

```text
D5: 1/(60+2) + 1/(60+1) + 1/(60+1) = 0.0161 + 0.0164 + 0.0164 = 0.0489
D2: 1/(60+1) + 1/(60+3) + 1/(60+2) = 0.0164 + 0.0159 + 0.0161 = 0.0484
D3: 1/(60+2)                        = 0.0161
D1: 1/(60+3)                        = 0.0159
D4: 1/(60+3)                        = 0.0159
```

The final order is D5, D2, D3, and then D1 and D4 with the same score.

Here, we can see that D5 wins because it was near the top of all three lists. D2 is a close second. D3, D1, and D4 appeared in only one list each, so they come later.

RRF only needs the positions, not the raw scores. So, it works even when the lists come from different kinds of search. This is also why RRF is the most common way to merge keyword search and semantic search results in [Hybrid Search](https://outcomeschool.com/blog/how-does-hybrid-search-work).

## Multi-Query Retrieval in code

Now, let's see the code for Multi-Query Retrieval with RRF. We can write the code as below:

```python
def generate_queries(question, n=3):
    prompt = f"""Write {n} different search queries for the question below.
Each query must look at the question from a different angle.
Return one query per line.
Question: {question}"""
    lines = call_llm(prompt).strip().split("\n")
    return [question] + [line.strip() for line in lines if line.strip()]
def rrf_merge(result_lists, k=60):
    scores = {}
    for results in result_lists:
        for rank, chunk_id in enumerate(results, start=1):
            scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)
def multi_query_search(question, top_k=5):
    queries = generate_queries(question)
    result_lists = [retriever.search(q, top_k=top_k) for q in queries]
    return rrf_merge(result_lists)[:top_k]
```

Here, we have:

- `generate_queries` asks the LLM for `n` different queries, one per line, and also keeps the original question in the list.
- `retriever.search` returns a list of chunk ids for each query, best first.
- `rrf_merge` goes through every list, gives each chunk `1 / (k + rank)`, and adds the scores. Then, it sorts the chunks by the total score. Duplicates are handled automatically, because the same chunk id simply collects more score.
- `multi_query_search` connects everything and returns the best `top_k` chunks.

## Query Rewriting vs Multi-Query Retrieval

Let me tabulate the differences between Query Rewriting and Multi-Query Retrieval for your better understanding.

| Point | Query Rewriting | Multi-Query Retrieval |
| --- | --- | --- |
| Output of the LLM step | One better query | Several different queries |
| Number of searches | One | One per query |
| Main strength | Fixes follow-ups, vague, and noisy questions | Finds information spread across different places |
| Safety against a bad rewrite | No backup | Other queries act as backup |
| Merging step needed | No | Yes, union or RRF |
| Speed and cost | Fast, one extra LLM call | Slower, one extra LLM call plus many searches |
| Best for | Chat applications with follow-up questions | Broad or multi-part questions |

**Note:** We can use both together. First, rewrite the follow-up question into a standalone question. Then, create multiple queries from that clean question.

In [Agentic RAG](https://outcomeschool.com/blog/agentic-rag), an agent goes one step further and decides on its own when to rewrite the query and when to search again.

## Where they work well and where they fail

**Advantages:**

- Both improve retrieval without changing our documents or our retriever.
- Query Rewriting makes follow-up questions in a chat work correctly.
- Multi-Query Retrieval finds more of the useful chunks, which is called better **[recall](https://outcomeschool.com/blog/precision-vs-recall)**.
- Both work with any retriever: keyword search, [vector search](https://outcomeschool.com/blog/how-does-a-vector-database-work), or both.

**Disadvantages:**

- Both add an extra LLM call before search, which adds time and cost.
- The LLM can change the meaning while rewriting. For example, it can drop an important detail like a version number. We must test our rewriting prompt carefully.
- Multi-Query Retrieval can bring in chunks that are only loosely related, which adds noise to the prompt. A [reranker](https://outcomeschool.com/blog/how-does-a-reranker-work) after the merge step can reorder the chunks by true relevance, so that only the best ones reach the LLM.
- For simple, clear questions, they add cost without much benefit.

Query Rewriting and Multi-Query Retrieval improve the question side of the search. We can also improve the chunk side by adding a short note to every chunk about where it comes from in the document. We have a detailed blog on [how Contextual Retrieval works](https://outcomeschool.com/blog/how-does-contextual-retrieval-work) that explains this end to end.

Now, we must have understood how Query Rewriting and Multi-Query Retrieval work, how they differ, and when to use which one.

## Frequently Asked Questions

### Does the user see the rewritten query?

No. The user never sees the rewritten query. It is used only for searching. The final answer is still written using the user's original question, together with the chunks that the rewritten query found.

### Can we use Query Rewriting and Multi-Query Retrieval together?

Yes. We can use both together. First, we rewrite the follow-up question into a standalone question using the chat history. Then, we create multiple queries from that clean question, search with each of them, and merge the results.

### Why keep the original question as one of the queries in Multi-Query Retrieval?

Many systems keep the user's original question as one of the queries so that we never lose what a plain search would have found. The other queries also act as a backup against one bad rewrite.

### What value of k is used in Reciprocal Rank Fusion?

The constant k is commonly set to 60. Each chunk gets 1 / (k + rank) from every list it appears in, and these scores are added. A chunk near the top of many lists collects the highest total score.
