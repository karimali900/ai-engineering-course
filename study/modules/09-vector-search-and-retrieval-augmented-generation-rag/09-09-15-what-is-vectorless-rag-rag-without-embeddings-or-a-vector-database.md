---
title: What is Vectorless RAG? RAG Without Embeddings or a Vector Database
module: 9
module_title: Vector Search and Retrieval-Augmented Generation (RAG)
lesson: '9.15'
source: https://outcomeschool.com/blog/vectorless-rag
published: September 10, 2026
tags:
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 3927
reading_time: 20
status: full
---
# What is Vectorless RAG? RAG Without Embeddings or a Vector Database

> **Module 9 · Lesson 9.15**  
> Source: [Outcome School](https://outcomeschool.com/blog/vectorless-rag) · Published: September 10, 2026 · Reading time: ~20 min · Tags: `ai`, `system-design`

---

![Vectorless RAG](../../assets/images/09-09-15-what-is-vectorless-rag-rag-without-embeddings-or-a-vector-database/vectorless-rag.png)

Vectorless RAG is a way of answering questions from our own documents without converting them into vectors and without any vector database. Instead, the LLM looks at the structure of the document, like a human reading a book, and decides which part to open.

In this blog, we will learn about Vectorless RAG, a way of answering questions from our own documents without converting those documents into numbers and without using any vector database. We will also see how the normal RAG works, why the vector part creates problems, how a Vectorless RAG system reads a document the way a human reads a book, how the tree structure and the search happen step by step, what the advantages and disadvantages are, and when to use which one.

We will cover the following:

- What is an LLM?
- What is RAG?
- How the normal Vector RAG works
- Problems with Vector RAG
- What is Vectorless RAG?
- How Vectorless RAG works
- An example of Vectorless RAG
- Other Vectorless approaches
- Advantages of Vectorless RAG
- Disadvantages of Vectorless RAG
- Vector RAG vs Vectorless RAG
- When to use which one

Let's get started.

## What is an LLM?

Before jumping into Vectorless RAG, we must know what an LLM is.

**LLM = Large Language Model.**

In simple words, an LLM is an AI Model that has read a huge amount of text and learned how language works. When we ask it something, it writes an answer one word at a time.

ChatGPT, Claude, and Gemini are all based on LLMs.

But there is a catch. An LLM only knows what it read during its training. It has never seen our office documents, our insurance policy, our company handbook, or the report we wrote last week.

So, if we ask an LLM a question about our own document, it cannot answer. It was never taught that.

We needed a solution for that, and RAG was introduced to solve this problem.

## What is RAG?

**RAG = Retrieval + Augmented + Generation.**

Let's break it down in simple words:

- **Retrieval**: find the useful part of our document.
- **Augmented**: add that part to the question.
- **Generation**: let the LLM write the answer using it.

So, RAG is a very simple idea. We do not teach the model anything new. We just hand it the right page at the right time.

Let's take an example.

Suppose we have a 300 page insurance policy. We ask, "Is dental treatment covered?"

Instead of sending all 300 pages to the LLM, we find the two pages that talk about dental treatment, and we send only those two pages along with our question.

The LLM reads those two pages and answers.

Think of it like an open book exam. The LLM is the student. Our document is the book. Retrieval is the act of finding the correct page.

Now, the following question arises. Why do we not simply hand over all the 300 pages every single time?

There are three reasons. First, an LLM can read only a limited amount of text at one time, and a large pile of documents will never fit. Second, we pay for every word we send, so sending the whole book for every small question becomes very costly. Third, and the most important one, when we bury the useful two pages inside 300 pages, the model gets distracted and the answer becomes worse.

We have a detailed blog on [The Lost in the Middle Problem in LLMs](https://outcomeschool.com/blog/lost-in-the-middle-problem-in-llms) that explains this third reason in depth.

So, we must send less text, and that less text must be the correct text.

Now, the question is, how do we find the correct page? This is exactly where the two approaches differ.

## How the normal Vector RAG works

Most RAG systems today use vectors. Let's understand this first, because Vectorless RAG only makes sense once we know what it is replacing.

Before that, we must know what a vector is.

A **vector** is just a long list of numbers, something like `[0.12, -0.88, 0.45, ...]`. There can be hundreds or thousands of numbers in that list.

There is a special model called an **[embedding model](https://outcomeschool.com/blog/what-are-embeddings)**. We give it a piece of text, and it gives back a vector. The important part is this: text with a similar meaning gets a similar list of numbers.

So, the sentence "I love dogs" and the sentence "I like puppies" will get two lists of numbers that are very close to each other. The sentence "The stock market crashed" will get a list of numbers that is far away from both.

Means, the meaning of a sentence has been turned into a position. Close numbers mean close meaning.

This way of searching by meaning instead of by exact words is called semantic search. We have a detailed blog on [How does Semantic Search work?](https://outcomeschool.com/blog/how-does-semantic-search-work) that covers this end to end.

Now, let's see how a Vector RAG system is built. It happens in two phases. Do not worry, we will learn about each of them in detail.

**Phase 1: Preparing the document.**

First, we take our 300 page document and cut it into small pieces. Each piece is usually a few hundred words. These pieces are called **[chunks](https://outcomeschool.com/blog/chunking-strategies-for-rag)**.

Then, we pass every chunk through the embedding model and get one vector for each chunk.

After that, we store all these vectors in a **[vector database](https://outcomeschool.com/blog/how-does-a-vector-database-work)**. A vector database is a special storage that is very fast at one job, which is finding the vectors that are closest to a given vector.

Now our document is ready for searching.

**Phase 2: Answering the question.**

First, the user asks a question.

Then, we pass the question through the same embedding model and get a vector for the question.

After that, we ask the vector database to find the chunks whose vectors are [closest to the question vector](https://outcomeschool.com/blog/how-does-approximate-nearest-neighbor-ann-search-work). Usually we ask for the closest 5 or 10 chunks. This number is called **top-k**.

Finally, we put those chunks and the question together and send them to the LLM, and the LLM writes the answer.

This is how Vector RAG works. It is a good approach, and it powers a huge number of products today.

But the following issues arise.

## Problems with Vector RAG

**Problem 1: Chunking breaks the meaning.**

We cut the document into pieces using a fixed size. The document does not care about our fixed size. A sentence can get cut in half. A table can get separated from its heading. A rule can get separated from its exception.

Let's say the policy says on one page, "Dental treatment is covered." And two pages later it says, "All treatments mentioned in Chapter 3 apply only after a waiting period of one year."

These two lines live in two different chunks. The system may pick the first chunk and miss the second one. The answer will be confidently wrong.

**Problem 2: Similar is not the same as correct.**

The vector database finds text that sounds similar to the question. Sounding similar is not the same as being the right answer.

If we ask, "Which policy does not cover dental treatment?", the word "not" is a tiny word. It barely moves the numbers. So, the system happily returns the chunks about policies that do cover dental treatment.

**Problem 3: There is no thinking during the search.**

The search is pure mathematics. It measures distance. It does not reason. It cannot say, "This question is about a rule and its exception, so I must look in two different chapters."

**Problem 4: We cannot explain the result.**

When a wrong chunk is picked, we cannot ask the vector database why. It returns numbers. Debugging becomes very hard.

**Problem 5: There is a whole system to maintain.**

We need an embedding model, a vector database, a chunking strategy, and a re-embedding job that runs every time a document changes. If we ever want to switch to a better embedding model, we must rebuild everything from the start.

**Problem 6: Special words and numbers suffer.**

Product codes, invoice numbers, medical terms, legal clause numbers, and tables do not carry much meaning for an embedding model. `Clause 14.2.b` and `Clause 14.3.b` look almost identical to it.

**Problem 7: The number of chunks is fixed.**

We decide the top-k value once, and it stays the same for every question. But one question may need a single line, and another question may need six full sections. A fixed number is either bringing too little or bringing too much noise.

So, here comes Vectorless RAG to the rescue.

## What is Vectorless RAG?

**Vectorless RAG = RAG without the vectors.**

**Vectorless RAG is a way of doing retrieval without converting our documents into vectors and without using any vector database. Instead of searching by number similarity, we let the LLM itself look at the structure of the document and decide which part to open, exactly the way a human finds an answer in a book.**

In simple words, we replace mathematics with reading, and that too without cutting our document into pieces.

Let's understand this with something that we all must have done at some point.

Suppose we buy a washing machine and we want to know about the warranty. We get a 200 page manual.

What do we do? We do not measure the similarity of anything. We open the table of contents at the front. We run our eyes down the chapter names. We see "Chapter 9: Warranty and Service". We jump to page 154. We read it. We answer.

That is it. That is the whole idea of Vectorless RAG.

We give the LLM the table of contents, and we let it choose the page.

**Note:** The word "Vectorless" only means that we are not using embedding vectors for the search. We are still using an LLM to read and to write the final answer.

## How Vectorless RAG works

Let's see how this happens step by step. It also has two phases.

**Phase 1: Preparing the document.**

So, here comes the **tree** into the picture. Instead of cutting the document into equal pieces, we build a tree out of it.

A tree here means the same thing as a table of contents. The book is at the top. Chapters come under the book. Sections come under the chapters. Sub-sections come under the sections.

For every node of this tree, we store three things:

- The title of that section, for example "3.4 Dental Treatment".
- A short summary of what that section says, written in one or two lines.
- The location of the real text, for example pages 41 to 43.

We do not store any numbers. We do not cut anything. The original document stays as it is, whole and untouched.

Building this tree is a one time job. If the document already has a table of contents, we can use it directly. If it does not have one, we let the LLM read section by section and write the titles and the summaries for us.

**Phase 2: Answering the question.**

**Step 1:** The user asks a question.

**Step 2:** We show the LLM only the top level of the tree, which is just the chapter names and their one line summaries. This is very small, maybe one page of text, even for a document of 300 pages. So, this step stays cheap and fast.

**Step 3:** We ask the LLM a simple question: "Based on these chapter names and summaries, which chapters can hold the answer?" The LLM picks one or more chapters and also tells us why it picked them.

**Step 4:** We open only the chosen chapters and show the LLM the sections inside them. The LLM picks again.

**Step 5:** We keep going down, level by level, until we reach the actual sections. This walking down the tree is called **tree search**.

**Step 6:** Now we pull the real, full text of those chosen sections. Nothing is cut in the middle, because we are taking complete sections.

**Step 7:** We send the question and that full text to the LLM, and it writes the final answer, along with the section number it used.

Here, we can notice one beautiful thing. At every step, a thinking model made the decision, and at every step it told us why. So, if the answer is wrong, we can open the trail and see exactly where it took the wrong turn.

**Note:** This is also called reasoning based retrieval, because the system reasons its way to the answer instead of measuring a distance between numbers.

## An example of Vectorless RAG

The best way to learn this is by taking an example.

Let's come back to our 300 page insurance policy. Our question is, "Is dental treatment covered in the first year?"

Assume that we have already built the tree of this policy, kept short here just for the sake of understanding, like below:

```text
Insurance Policy
|
|-- Chapter 1: Definitions
|-- Chapter 2: How to Buy the Policy
|-- Chapter 3: What is Covered
|     |-- 3.1 Hospital Stay
|     |-- 3.2 Surgery
|     |-- 3.3 Eye Care
|     |-- 3.4 Dental Treatment
|-- Chapter 4: What is Not Covered
|-- Chapter 5: Waiting Periods
|-- Chapter 6: How to Claim
```

Let's first see what a Vector RAG system does.

It looks for chunks that sound like "dental treatment covered first year". The word "dental" appears in Chapter 3 many times, so it returns five chunks from `3.4 Dental Treatment`. All five chunks talk about dental treatment being covered.

Chapter 5 says, "Dental treatment has a waiting period of 12 months." But that single line was sitting inside a long chunk about many different waiting periods, and it did not sound close enough to our question.

So, the LLM sees only the chunks that say yes, and it answers, "Yes, dental treatment is covered."

The answer is wrong.

Now, let's see what a Vectorless RAG system does.

The LLM sees the six chapter names. It thinks like this: "The user is asking two things. One, is dental treatment covered. Two, is it covered in the first year. The first part is in Chapter 3. The second part is about time, so it is in Chapter 5."

It picks Chapter 3 and Chapter 5.

Then it goes one level down inside Chapter 3 and picks `3.4 Dental Treatment`.

Then we pull the full text of `3.4` and the full text of Chapter 5, and we send both to the LLM.

Now the LLM has both halves of the truth in front of it, and it answers, "Dental treatment is covered, but not in the first year. There is a waiting period of 12 months, as per Chapter 5."

The answer is correct. Problem Solved!

Here, we can see the real difference. The vector system searched for words that sound alike. The vectorless system understood the question and went to look for the rule and its exception, the way a careful human would.

> In Vector RAG, we search with mathematics. In Vectorless RAG, we search with reading.

This way we can use Vectorless RAG to solve the interesting problem of finding an answer that is hiding in two different places at once.

## Other Vectorless approaches

The tree search is the most popular way, but it is not the only vectorless way. Let's see a few more.

**Keyword search.** This is the old and trusted way of matching the actual words, the same way we search inside a file. If the user asks for `Invoice INV-2024-8891`, keyword search will find that exact string every single time, while an embedding model may bring back a hundred similar looking invoice numbers.

**Filtering on structured data.** If our data lives in a normal database with columns like date, city, and amount, we do not need any search at all. We let the LLM write a query, we run it, and we give the rows back to the LLM. Numbers and dates are handled perfectly this way.

**Giving the full document.** Modern LLMs can read a very large amount of text in one go. If our document is small enough to fit, we can simply give the whole thing along with the question. There is no retrieval step at all. It is the simplest approach, and for a single contract or a single report, it works perfectly.

**Letting the model browse the files.** We can also give the LLM a set of tools, such as list the folders, open a file, and search inside a file. Then the LLM explores our files on its own, one step at a time, the way a developer explores a new codebase. This is often called [agentic search](https://outcomeschool.com/blog/agentic-rag).

All of these are vectorless. Not a single vector is created in any of them.

A coding agent works exactly this way inside our codebase. We have a detailed blog on [how Claude Code works](https://outcomeschool.com/blog/how-does-claude-code-work) that explains how it finds the right file without creating a single embedding.

This was all about the different vectorless approaches. Now, let's discuss the advantages and the disadvantages of Vectorless RAG.

## Advantages of Vectorless RAG

- **No chunking.** We always read complete sections, so a rule never gets separated from its exception.
- **No vector database and no embedding model.** There is one less system to build, to pay for, and to maintain.
- **Easy updates.** When a document changes, we update the summary of that one section. There is no re-embedding of anything.
- **We can see the reasoning.** At every step, the LLM tells us why it opened a particular chapter. Debugging becomes simple.
- **Special words work well.** Clause numbers, product codes, and medical terms are read as real words, not turned into a blur of numbers.
- **Better answers on long and structured documents.** Reports, policies, manuals, and legal papers already have a clean structure, and this approach uses that structure instead of throwing it away.
- **Real reasoning during the search.** The system can decide to look in two far apart chapters because the question needs both.

In short, it makes our life easy when the documents are long and the answers must be correct.

## Disadvantages of Vectorless RAG

- **It is slower.** Walking down the tree needs a few LLM calls, one for each level. A vector search finishes in milliseconds.
- **It costs more per question.** Every LLM call costs money. A vector search is close to free once the vectors are stored.
- **It needs structure.** If our data is ten million random support chat messages with no titles and no sections, there is no meaningful tree to build.
- **The quality depends on the summaries.** If a section summary is written poorly, the LLM may skip that section. The summary is doing the job that the vector used to do.
- **It does not scale to millions of documents on its own.** Searching inside one long document is easy. Choosing between five million documents needs some cheap first filter before the tree search can begin.

## Vector RAG vs Vectorless RAG

Now that we have learned about both of them, it's time to put them side by side.

Let me tabulate the differences between Vector RAG and Vectorless RAG for your better understanding so that you can decide which one to use based on your use case.

| Vector RAG | Vectorless RAG |
| --- | --- |
| Documents are converted into vectors. | Documents are kept as they are. |
| Needs an embedding model. | Does not need an embedding model. |
| Needs a vector database. | Does not need a vector database. |
| Documents are cut into fixed size chunks. | Documents are kept whole and read section by section. |
| Search happens by measuring distance between numbers. | Search happens by the LLM reading titles and summaries and choosing. |
| There is no reasoning during the search. | There is reasoning at every step of the search. |
| Very fast, in milliseconds. | Slower, because it needs a few LLM calls. |
| Very cheap for each question. | Costlier for each question. |
| Hard to explain why a chunk was picked. | Easy to explain, because the LLM gives its reason. |
| Scales very well to millions of documents. | Works best on long and well structured documents. |
| Updating a document needs re-embedding. | Updating a document needs only a summary update. |
| Struggles with exact codes, numbers, and negation. | Handles exact codes, numbers, and negation well. |

## When to use which one

We must use **Vector RAG** when we have a very large number of documents, when the questions are simple lookups, when speed matters a lot, and when the cost of each question must stay very low. A help center with a million short articles is a good example.

We must use **Vectorless RAG** when we have long documents that already have a clean structure, when a wrong answer is expensive, and when the questions need reasoning across different parts of the same document. Insurance policies, legal contracts, annual reports, medical guidelines, and technical manuals are good examples.

So, now we know where we can use the Vectorless RAG.

Many strong systems use both. They use a cheap vector search or a keyword search to narrow five million documents down to twenty, and then they use the tree search inside those twenty to find the exact section. This is called a [hybrid approach](https://outcomeschool.com/blog/how-does-hybrid-search-work), and we get the speed of one and the accuracy of the other.

Now we must have understood Vectorless RAG, why it exists, how it works, and where it fits.

## Frequently Asked Questions

### Does Vectorless RAG still use an LLM?

Yes. The word "Vectorless" only means that we do not use embedding vectors for the search. We still use an LLM to read the table of contents, pick the right chapters and sections, and write the final answer. In fact, the LLM does the job of finding the right part of the document.

### Can we use Vectorless RAG if our document has no table of contents?

Yes. If the document already has a table of contents, we can use it directly to build the tree. If it does not have one, we let the LLM read the document section by section and write the titles and short summaries for us. Building this tree is a one time job.

### Is Vectorless RAG the same as keyword search?

No. Keyword search is only one of the vectorless approaches. The most popular vectorless approach is tree search, where the LLM walks down the table of contents level by level. Keyword search instead matches the actual words, which makes it very good at finding exact strings like invoice numbers.

### Do we always need a retrieval step in RAG?

No. If our document is small enough to fit into what the LLM can read in one go, we can simply give the whole document along with the question. There is no retrieval step at all. It is the simplest approach, and it works perfectly for a single contract or a single report.

### Why is Vectorless RAG called reasoning based retrieval?

It is called reasoning based retrieval because the system reasons its way to the answer instead of measuring a distance between numbers. At every step, the LLM decides which part to open and tells us why. So, if the answer is wrong, we can open the trail and see exactly where it took the wrong turn.
