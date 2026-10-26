---
title: How does Hybrid Search work?
module: 9
module_title: Vector Search and Retrieval-Augmented Generation (RAG)
lesson: '9.4'
source: https://outcomeschool.com/blog/how-does-hybrid-search-work
published: July 7, 2026
tags:
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 3713
reading_time: 19
status: full
---
# How does Hybrid Search work?

> **Module 9 · Lesson 9.4**  
> Source: [Outcome School](https://outcomeschool.com/blog/how-does-hybrid-search-work) · Published: July 7, 2026 · Reading time: ~19 min · Tags: `ai`, `system-design`

---

![How does Hybrid Search work?](../../assets/images/09-09-04-how-does-hybrid-search-work/how-does-hybrid-search-work.png)

Hybrid Search is a technique that combines keyword search and semantic search, and merges their results into one final ranked list. This way, we get exact word matches and meaning-based matches together.

In this blog, we will learn about how Hybrid Search works. We will also see why we need it, the two kinds of search it combines, how their results are merged together, and where it is used in real systems like RAG.

We will cover the following:

- What is keyword search?
- Why keyword search alone is not enough
- What is semantic search?
- Why semantic search alone is not enough
- What is Hybrid Search?
- How Hybrid Search runs both searches
- How the two result lists are combined
- Reciprocal Rank Fusion (RRF)
- Weighted score combination and normalization
- Hybrid Search in the real world

Let's get started.

### What is keyword search?

Before we talk about Hybrid Search, we must first understand what keyword search is.

The first way is keyword search.

**Keyword search finds documents that contain the same words as the query.**

In simple words, it looks for an exact word match. If the user types the word "refund", keyword search looks for documents that literally contain the word "refund".

Let's say our query is "refund policy". Keyword search scans every document and asks a simple question: does this document contain the words "refund" and "policy"? The documents that contain these words, especially many times, get pushed to the top.

The most popular method for keyword search is called **BM25**. Here, we just need to understand what it does in plain words.

BM25 gives each document a **score**, which is a number that tells us how well the document matches the query words. A higher score means a better match. BM25 looks at two simple things:

- How often the query words appear in the document. More appearances usually mean a better match.
- How rare the query word is across all documents. A rare word like "refund" matters more than a common word like "the".

So, BM25 reads the query words, counts how they appear in each document, and gives every document a score. Then it sorts the documents from the highest score to the lowest. This sorted list is called a **ranked list**.

Keyword search is also called **lexical search**. The word "lexical" simply means "relating to words". So lexical search is word-based search. Keep this word in mind, because we will use it later.

This is how keyword search works. It is fast, simple, and great at finding exact words.

### Why keyword search alone is not enough

Now, here is the catch with keyword search.

Keyword search only understands words, not meaning. It cannot tell that two different words mean the same thing.

Let's see the problem with an example. Suppose our document says "how to return your shoes", but the user types "how to send shoes back". A human knows these mean the same thing. But keyword search sees different words. The word "return" is not the same as "send back". So keyword search may rank the correct document very low, or miss it completely.

This problem is called the **synonym problem**. A synonym is a different word with the same meaning, like "car" and "automobile", or "doctor" and "physician". Keyword search treats them as totally unrelated, because the letters are different.

So, the issue with keyword search is that it is blind to meaning. Let's see how the next approach solves this issue.

### What is semantic search?

The second way is [semantic search](https://outcomeschool.com/blog/how-does-semantic-search-work).

**Semantic search finds documents that have the same meaning as the query, even if they use different words.**

The word "semantic" simply means "relating to meaning". So semantic search is meaning-based search.

In simple words, semantic search understands that "send shoes back" and "return your shoes" mean the same thing, and it brings up the right document even though the words are different.

Now, the question is, how does a computer understand meaning? The answer is something called an **[embedding](https://outcomeschool.com/blog/what-are-embeddings)**.

**An embedding is a list of numbers that represents the meaning of a piece of text.**

Let's understand this slowly, because it is the heart of semantic search. A special model called an embedding model reads a piece of text and turns it into a long list of numbers. This list of numbers is called a **vector**. The amazing part is this: texts that mean similar things get similar lists of numbers, and texts that mean different things get very different lists of numbers.

So, the sentence "return your shoes" and the sentence "send shoes back" will produce two lists of numbers that are very close to each other, because they mean almost the same thing.

We can picture it as below:

```
TEXT  ->  EMBEDDING MODEL  ->  VECTOR (a list of numbers)
"return your shoes"   ->   [ 0.91, 0.12, 0.77, ... ]
"send shoes back"     ->   [ 0.89, 0.15, 0.74, ... ]   <- very close to the one above
"order a pizza"       ->   [ 0.04, 0.88, 0.21, ... ]   <- far away, different meaning
```

Here, we can see that the first two texts mean almost the same thing, so their lists of numbers are very close. The third text means something completely different, so its list of numbers is far away.

So, to do semantic search, we first turn every document into a vector ahead of time. When the user types a query, we turn the query into a vector too. Then we look for the document vectors that are closest to the query vector. The closest vectors mean the most similar meaning. This is called **[vector search](https://outcomeschool.com/blog/how-does-a-vector-database-work)**, because we are searching using vectors. Finding these closest vectors quickly across a huge number of documents is a whole technique in itself - we have a detailed blog on [Approximate Nearest Neighbor (ANN) search](https://outcomeschool.com/blog/how-does-approximate-nearest-neighbor-ann-search-work) that explains how this works.

We can picture this closeness as points sitting in a space, like below:

```
            far away (different meaning)
                                          *  "order a pizza"
       *  "send shoes back"   (the query)
        \
         \  close by
          \
           *  "return your shoes"
                 *  "track my order"
                    (a bit farther)
```

Here, we can see that "return your shoes" sits very close to our query "send shoes back", because they mean almost the same thing. "Track my order" sits a bit farther, and "order a pizza" sits far away, because it means something completely different. Vector search simply picks the points that sit closest to the query.

Just like keyword search, vector search also gives each document a score and returns a ranked list. Here, the score is a measure of how close the document vector is to the query vector. A higher closeness score means a better match in meaning.

This is how semantic search works. It understands meaning, so it handles synonyms and rephrasing beautifully.

### Why semantic search alone is not enough

Now, semantic search sounds perfect. But it has its own catch.

Semantic search is great at meaning, but it can be weak at exact, precise terms.

Let's see why with an example. Suppose a user searches for a specific product code like "SKU-48217", or an exact error code like "ERR\_500", or a specific person's name, or a rare technical term. These are exact strings that must match exactly, not soft ideas about meaning.

A product code does not really have a "meaning". So semantic search may pull up documents that feel related but do not contain the exact code we asked for. It can quietly miss the one document that has the exact term.

So, here is the situation we are in:

- Keyword search is great at exact words and codes, but blind to meaning.
- Semantic search is great at meaning, but weak at exact codes and rare terms.

Each one is strong exactly where the other one is weak. So, here comes Hybrid Search to the rescue.

### What is Hybrid Search?

**Hybrid Search is a technique that combines keyword search and semantic search, and merges their results into one final ranked list.**

Let's decompose the term to make it clear.

> Hybrid Search = Keyword Search + Semantic Search

The word "hybrid" simply means a mix of two different things. So Hybrid Search is a mix of word-based search and meaning-based search.

In simple words, Hybrid Search runs both searches at the same time, and then combines what they found. This way, we get the exact-match power of keyword search and the meaning power of semantic search, together in one result.

Let's say we ask two helpers to find a document for us. One helper is very good at spotting exact words and codes. The other helper is very good at understanding what we actually mean. If we listen to only one of them, we lose what the other one is good at. So we ask both, and then we combine their answers. This is exactly what Hybrid Search does.

Let's connect it to what we learned. If the user searches for an exact code, keyword search catches it. If the user searches with different words for the same idea, semantic search catches it. Hybrid Search makes sure we do not lose either one.

So, Hybrid Search gives us the best of both worlds. Now, let's understand exactly how it works step by step.

### How Hybrid Search runs both searches

Hybrid Search starts by running two separate searches on the same query.

**Step 1:** The user types a query, for example "how to send shoes back".

**Step 2:** We run a lexical search using BM25. This is the keyword search. It returns a ranked list of documents, each with a BM25 score.

**Step 3:** At the same time, we run a vector search using embeddings. This is the semantic search. It turns the query into a vector, finds the closest document vectors, and returns its own ranked list of documents, each with a closeness score.

So, after this, we have two ranked lists. One list comes from keyword search, and one list comes from semantic search.

Let's see it as below:

```
                       Query: "how to send shoes back"
                                     |
                 +-------------------+-------------------+
                 |                                       |
          KEYWORD SEARCH                          SEMANTIC SEARCH
            (BM25)                                  (embeddings)
                 |                                       |
        ranked list A:                          ranked list B:
        1. Doc-7   (score 9.1)                  1. Doc-3   (score 0.95)
        2. Doc-2   (score 6.4)                  2. Doc-7   (score 0.88)
        3. Doc-9   (score 4.2)                  3. Doc-5   (score 0.81)
```

Here, we can see that both searches looked at the same query but returned different lists. Keyword search put Doc-7 first because it shares exact words. Semantic search put Doc-3 first because it is closest in meaning. Notice that Doc-7 appears in both lists, which is a strong hint that it is a very good match.

Now we have two lists. The next big question is: how do we combine them into one final list? Let's see.

### How the two result lists are combined

The step where we merge the two ranked lists into one final list is called **fusion**.

The word "fusion" simply means joining two things into one. So fusion means joining the keyword list and the semantic list into a single final ranking.

But, here is the catch. We cannot just add the two scores together directly. Look again at the example above. The BM25 score for Doc-7 was 9.1, while its semantic score was 0.88. These numbers live on completely different scales.

Let's understand this scale problem. BM25 scores can be any number, like 2, 6, or even 40, with no fixed top value. Semantic closeness scores usually sit between 0 and 1. So if we simply add them, the big BM25 numbers would crush the small semantic numbers. The keyword search would always win, and the semantic search would barely count. That is unfair, and it defeats the whole purpose of combining them.

So, we need a fair way to combine the two lists. There are two popular methods. The first one cleverly avoids the score problem altogether, and the second one fixes the scales first. Let's learn both.

### Reciprocal Rank Fusion (RRF)

The first and most popular method is called **Reciprocal Rank Fusion**, or **RRF**.

**RRF combines the two lists using the position of each document in each list, not its raw score.**

This is the clever trick. RRF ignores the messy raw scores completely. Instead, it only looks at the **rank**, which means the position of the document in the list. The document at the top is rank 1, the next is rank 2, and so on.

Why does this help? Because a position is just a position. Rank 1 means the same thing in both lists, whether the raw score was 9.1 or 0.88. So the scale problem disappears.

Let's understand the word "reciprocal". The reciprocal of a number is just 1 divided by that number. So the reciprocal of 2 is 1 divided by 2, which is 0.5. The reciprocal of 4 is 1 divided by 4, which is 0.25.

Here is the idea in plain words. For each document, RRF gives it points based on its rank in each list. A better rank, which means a smaller rank number, gives more points. We give points using the reciprocal of the rank. So:

- A document at rank 1 gets 1 divided by 1, which is the most points.
- A document at rank 2 gets 1 divided by 2, which is fewer points.
- A document at rank 3 gets 1 divided by 3, which is even fewer points.

Then, for each document, we add up the points it earned from both lists. The document with the most total points goes to the top of the final list.

Let's walk through our example. We will keep it simple just for the sake of understanding, as below:

```
Doc-7:  rank 1 in keyword list  ->  1/1 = 1.00
        rank 2 in semantic list ->  1/2 = 0.50
        total = 1.00 + 0.50 = 1.50
Doc-3:  not in keyword list     ->  0
        rank 1 in semantic list ->  1/1 = 1.00
        total = 0 + 1.00 = 1.00
Doc-2:  rank 2 in keyword list  ->  1/2 = 0.50
        not in semantic list    ->  0
        total = 0.50 + 0 = 0.50
```

Here, we can see that Doc-7 wins. It earned points from both lists, because it was near the top in both. Doc-3 was only strong in the semantic list, and Doc-2 was only strong in the keyword list. So Doc-7, which both searches agreed was good, rises to the top of the final list.

This is the beauty of RRF. A document that both searches like will naturally float to the top, because it collects points from both sides.

**Note:** In the real RRF formula, we add a small fixed number to the rank before dividing, to keep the top ranks from being too far ahead of the rest. We do not need that detail to understand the idea. The main point is that RRF uses ranks, not raw scores, so it avoids the scale problem completely.

So, RRF is simple, fair, and works very well in practice. This is why it is the most common fusion method in Hybrid Search. The same RRF is also used in [Multi-Query Retrieval](https://outcomeschool.com/blog/how-do-query-rewriting-and-multi-query-retrieval-work), where we search with several versions of the user's question and merge all the result lists into one.

### Weighted score combination and normalization

The second method is called **weighted score combination**.

**In weighted score combination, we use the actual scores from both searches, but we first fix their scales, and then we blend them using weights.**

We learned that the raw scores live on different scales, so we cannot add them directly. To solve this, we first do something called **normalization**.

**Normalization means rescaling all the scores so that they fall into the same range, usually between 0 and 1.**

In simple words, normalization is like converting two different units into one common unit, so we can compare them fairly.

After normalization, we apply a **weight** to each search. A weight is simply how much importance we give to each search. The weights let us tune the balance based on our use case.

Let's see the simple formula in plain words, as below:

```
final score = (weight_keyword  x  normalized keyword score)
            + (weight_semantic x  normalized semantic score)
```

Here, we can see that the final score for a document is a blend of its normalized keyword score and its normalized semantic score, each multiplied by how much we trust that search.

Let's say we set the keyword weight to 0.5 and the semantic weight to 0.5. That means we trust both searches equally. If our documents are full of exact codes and product names, we can raise the keyword weight, for example to 0.7, and lower the semantic weight to 0.3. If meaning matters more for our use case, we do the opposite.

So, the two steps for this method are simple. First, normalize the scores so they are on the same scale. Then, blend them using weights that match our use case.

Now, let me tabulate the differences between RRF and weighted score combination for your better understanding so that you can decide which one to use based on your use case.

| Point | Reciprocal Rank Fusion (RRF) | Weighted score combination |
| --- | --- | --- |
| What it uses | The rank (position) of each document | The actual normalized scores |
| Needs normalization | No, because ranks already share a scale | Yes, we must normalize first |
| Tuning control | Less control over balance | More control through weights |
| Ease of use | Very simple, works well by default | Needs more tuning to get right |

Here, we can see that RRF is the easy, reliable default, while weighted score combination gives us finer control when we are ready to tune.

### Hybrid Search in the real world

Now, let's see where Hybrid Search is used in real systems.

The biggest place where Hybrid Search shines is **[RAG](https://outcomeschool.com/blog/agentic-rag)**. RAG stands for **Retrieval-Augmented Generation**. In simple words, it is a system where we first fetch some relevant documents and then send them to a large language model along with the user's question, so the model can answer using real, up-to-date information.

The quality of a RAG system depends heavily on the fetching step, which is called retrieval. If we fetch the wrong documents, the model gives a wrong answer, no matter how smart the model is.

There are also techniques that sharpen this retrieval step further, like HyDE, which searches with a hypothetical answer instead of the raw question, and [Contextual Retrieval](https://outcomeschool.com/blog/how-does-contextual-retrieval-work), which adds a short note about the source document to every chunk before indexing. We have a detailed blog on [how HyDE works in RAG](https://outcomeschool.com/blog/how-does-hyde-work) that explains this step by step.

We can picture where Hybrid Search fits inside RAG, like below:

```
   User question
        |
        v
  +--------------+     fetched documents       +-----+
  | HYBRID       | ------------------------>   | LLM | --> Answer
  | SEARCH       |                             +-----+
  | (retrieval)  |                                ^
  +--------------+                                |
                                            User question
```

Here, we can see that the user question first goes into Hybrid Search, which fetches the most relevant documents. Those documents and the user question are then handed to the LLM together. The LLM reads both and produces the final answer. So if Hybrid Search fetches the right documents, the LLM has the right information to answer well.

This is exactly why Hybrid Search matters so much for RAG. The retrieval step must catch both exact terms and matching meaning. If a user asks about a specific error code, keyword search catches it. If a user asks the same thing in different words, semantic search catches it. Hybrid Search combines both, so the retrieval step rarely misses the right document. Better retrieval means better answers.

In many production RAG systems, one more step sits right after Hybrid Search - a reranker that reorders the fetched documents by true relevance before they reach the LLM. We have a detailed blog on [how a reranker works](https://outcomeschool.com/blog/how-does-a-reranker-work) that covers this in depth.

Retrieval does not always have to involve vectors either. A common setup narrows a huge collection down to a handful of documents with a cheap search like this one, and then lets the model read the structure of those few. We have a detailed blog on [Vectorless RAG](https://outcomeschool.com/blog/vectorless-rag) that explains how that second step works.

This is how Hybrid Search works. We run a keyword search with BM25 and a semantic search with embeddings, we get two ranked lists with their own scores, and then we fuse them into one final list, either with Reciprocal Rank Fusion using ranks, or with a weighted blend of normalized scores, so that we get the exact-match power of keywords and the meaning power of embeddings at the same time.

## Frequently Asked Questions

### Is Hybrid Search better than semantic search alone?

Yes, because it gives us the best of both worlds. Semantic search is great at meaning, but it can miss exact terms like a product code, an error code, or a rare technical term. Hybrid Search adds keyword search to catch those exact matches, so we get both exact words and matching meaning in one result.

### Can we simply add the BM25 score and the semantic score together?

No. The two scores live on completely different scales. BM25 scores can be any number with no fixed top value, while semantic closeness scores usually sit between 0 and 1. If we add them directly, the big BM25 numbers crush the small semantic numbers, and keyword search always wins.

### Should we use RRF or weighted score combination?

RRF is the easy, reliable default. It uses ranks instead of raw scores, so it needs no normalization and works well out of the box. Weighted score combination gives us finer control through weights, but we must normalize the scores first and spend more effort tuning it.

### How should we set the weights in weighted score combination?

We set the weights based on our use case. Equal weights, like 0.5 and 0.5, mean we trust both searches equally. If our documents are full of exact codes and product names, we raise the keyword weight, for example to 0.7. If meaning matters more, we raise the semantic weight instead.
