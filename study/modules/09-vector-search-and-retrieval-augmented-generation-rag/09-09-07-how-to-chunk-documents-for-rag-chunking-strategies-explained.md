---
title: How to Chunk Documents for RAG? Chunking Strategies Explained
module: 9
module_title: Vector Search and Retrieval-Augmented Generation (RAG)
lesson: '9.7'
source: https://outcomeschool.com/blog/chunking-strategies-for-rag
published: September 10, 2026
tags:
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 5961
reading_time: 30
status: full
---
# How to Chunk Documents for RAG? Chunking Strategies Explained

> **Module 9 · Lesson 9.7**  
> Source: [Outcome School](https://outcomeschool.com/blog/chunking-strategies-for-rag) · Published: September 10, 2026 · Reading time: ~30 min · Tags: `ai`, `system-design`

---

![Chunking Strategies for RAG](../../assets/images/09-09-07-how-to-chunk-documents-for-rag-chunking-strategies-explained/chunking-strategies-for-rag.png)

Chunking for RAG means cutting a big document into smaller pieces, called chunks, so that an AI system can find the right piece at the right time and answer our question correctly.

In this blog, we will learn about Chunking Strategies for RAG, the art of cutting a big document into smaller pieces so that an AI system can find the right piece at the right time. We will also see what RAG is, why chunking is needed at all, what happens when we chunk badly, the most useful chunking strategies one by one, how to pick the chunk size and the overlap, and where each strategy works well and where it fails.

We will cover the following:

- What is RAG?
- What is a chunk?
- Why do we need chunking?
- How retrieval actually works
- What happens when we chunk badly
- Fixed-size chunking
- Chunking by sentence
- Recursive chunking
- Document structure based chunking
- Semantic chunking
- Contextual chunking
- Small-to-big chunking
- Agentic chunking
- Chunk overlap
- How to choose the chunk size
- Comparison of all the strategies
- Common mistakes
- Conclusion

Let's get started.

## What is RAG?

Before jumping into chunking, we must know what RAG is.

**RAG = Retrieval + Augmented + Generation.**

Let's break the name into three plain words:

- **Retrieval** means finding.
- **Augmented** means adding something extra.
- **Generation** means writing the answer.

So, RAG is a system that first finds the useful information, then adds that information to our question, and then lets the AI model write the answer using it.

Let's say we have a company handbook of 500 pages. We ask the AI, "How many leave days do I get in my first year?"

The AI model has never read our handbook. It was trained on the public internet, and our handbook is a private document sitting on our laptop. So, the model has no way to know the answer.

Here comes RAG into the picture. RAG does three simple things:

- It searches our handbook and finds the small part that talks about leave days.
- It pastes that small part along with our question.
- It sends both to the AI model and asks it to answer using that part.

The model now has the right page in front of it, so it answers correctly, and that too without any retraining.

This is how RAG works. It is like giving an open-book exam to the model instead of asking it to remember everything.

Now, the question is, how does RAG search a 500-page handbook? It cannot send all 500 pages to the model every time. It is too big, too slow, and too costly. So, we cut the handbook into small pieces first.

Those small pieces are called chunks.

## What is a chunk?

**A chunk is a small piece of text that we cut out from a bigger document.**

In simple words, if the document is a long chocolate bar, a chunk is one square of it.

Let's say our handbook has this paragraph:

```text
Every employee gets 24 paid leave days in the first year.
Leave days do not carry forward to the next year.
Sick leave is counted separately and is limited to 12 days.
```

If we cut it into three pieces, one per sentence, we get three chunks. Each chunk is a small, self-contained note.

Later, when someone asks about sick leave, we do not need the whole handbook. We only need the third chunk.

This cutting is called **chunking**.

Now, we have understood the chunk. Now, let's learn why we need chunking at all.

## Why do we need chunking?

There are four solid reasons.

**Reason 1: The model has a limited context window.**

A model can only read a limited amount of text at once. This limit is called the [context window](https://outcomeschool.com/blog/context-engineering).

This limit is counted in **[tokens](https://outcomeschool.com/blog/tokenization-in-llms)**. A token is a small piece of text, roughly three-fourth of a word. So, 100 tokens is about 75 words. We will use this word many times in this blog, so it is good to remember it now.

Our 500-page handbook has millions of tokens, and it does not fit inside the window. So, we must send only the relevant part.

**Reason 2: Cost and speed.**

Even if a huge document fits, sending it every single time is slow and expensive. We pay for every token we send. Sending one paragraph is far cheaper than sending 500 pages.

**Reason 3: Accuracy.**

This is the most important reason. When we give the model a mountain of text, the useful line gets buried inside it. The model gets distracted and starts mixing up facts from two different pages. When we give it three short and relevant chunks, it answers cleanly.

Less and correct text always beats more and noisy text.

We have a detailed blog on [The Lost in the Middle Problem in LLMs](https://outcomeschool.com/blog/lost-in-the-middle-problem-in-llms) that explains this in depth.

**Reason 4: Search itself needs small pieces.**

The search step works by comparing meaning. A small chunk has one clear meaning. A giant chunk has fifty mixed meanings, so its meaning becomes blurry, and the search stops working well.

We will understand this fourth reason properly in the next section.

## How retrieval actually works

Before jumping into the strategies, we need to see how the searching happens. Once we understand this, every chunking strategy will make sense on its own.

The search inside RAG is not a keyword search. It is a **[meaning search](https://outcomeschool.com/blog/how-does-semantic-search-work)**.

Here is how it happens.

**Step 1: Every chunk is turned into a list of numbers.**

We pass each chunk through a small model called an [embedding model](https://outcomeschool.com/blog/what-are-embeddings). It reads the chunk and gives back a long list of numbers, something like `[0.12, -0.98, 0.45, ...]`.

This list of numbers is called an **embedding**. We can think of it as the address of the meaning of that chunk. Two chunks that talk about the same thing get two addresses that sit close to each other.

**Step 2: All these number lists are stored in a vector database.**

A [vector database](https://outcomeschool.com/blog/how-does-a-vector-database-work) is simply a storage that is very good at one job, finding the addresses that sit closest to a given address.

This whole one-time work of cutting the document, creating the embeddings, and storing them is called **indexing**. We do it once, before any user asks anything.

**Step 3: The user's question is also turned into numbers.**

When the user asks, "How many sick leave days do I get?", we pass this question through the same embedding model and get its address.

**Step 4: We pick the closest chunks.**

The vector database compares the question address with all the chunk addresses and returns the closest few, usually the top 3 or top 5. In a real system, one more step often sits right here. A reranker takes these closest few and reorders them by true relevance before they go to the model. We have a detailed blog on [how a Reranker works](https://outcomeschool.com/blog/how-does-a-reranker-work) that explains this step by step.

**Step 5: Those chunks go to the model.**

We paste those chunks along with the question and ask the model to answer.

Here, we can notice one very important thing. The whole system stands on one assumption, that **each chunk carries one clear meaning**. The moment a chunk carries a mix of ten unrelated ideas, its address becomes an average of ten things, and it stops being close to anything.

This is exactly why chunking strategy matters so much.

## What happens when we chunk badly

The best way to learn this is by taking an example.

Assume that we have this text in our handbook:

```text
Every employee gets 24 paid leave days in the first year. To apply,
open the HR portal and submit the request at least 7 days in advance.
```

Now, let's say we cut blindly after a fixed number of letters, and the cut lands in the middle:

**Chunk 1:**

```text
Every employee gets 24 paid leave days in the first year. To apply,
open the HR portal and submit the request at least
```

**Chunk 2:**

```text
7 days in advance.
```

Now, the user asks, "How early do I need to apply for leave?"

Chunk 2 has the actual answer, but it is just a floating fragment. It does not contain the words leave, apply, or request. Its meaning address is nowhere near the question. So, it is never retrieved.

Chunk 1 gets retrieved instead, and it stops right before the answer. The model reads it and either says it does not know, or worse, it guesses a number.

This is the core problem. **A bad chunk is not a small problem, it silently destroys the answer.**

So, our whole goal in chunking is simple, we must cut at places where a complete idea ends, not at random places.

Every strategy that we will learn now is just a smarter way of finding those places.

Now that we have understood the problem, it is time to learn the strategies one by one. We will start from the simplest one and keep improving. Do not worry, we will learn about each of them in detail.

## Fixed-size chunking

**Fixed-size chunking means we cut the document after every fixed number of characters or tokens, no matter what the text says.**

This is the simplest strategy. We decide a number, let's say 500 characters, and we cut after every 500 characters.

Let's see the code as below:

```python
def fixed_size_chunks(text, size=500):
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i + size])
    return chunks
```

Here, we are walking through the text 500 characters at a time and collecting each slice as one chunk.

**Advantage:**

- It is very simple and very fast.
- Every chunk has a predictable size, so nothing ever overflows the model limit.
- It works on any kind of text, even messy text with no structure.

But, here is the catch.

**Disadvantage:**

- It cuts in the middle of a word, a sentence, or an idea, exactly like the leave-application example we just saw.
- The retrieved chunk often reads like a broken fragment.

The issue with this approach is that the cut position is decided by counting, not by meaning. Let's see how the next approach solve this issue.

## Chunking by sentence

**Sentence-based chunking means we split the text into sentences first, and then group a few sentences together to form one chunk.**

So, instead of cutting after 500 characters, we cut only at a full stop. This one small change removes broken words and broken sentences completely.

Let's see the code as below:

```python
import re
def sentence_chunks(text, sentences_per_chunk=5):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        group = sentences[i:i + sentences_per_chunk]
        chunks.append(" ".join(group))
    return chunks
```

Here, we have first split the text wherever a full stop, a question mark, or an exclamation mark is followed by a space. Then we have grouped every 5 sentences into one chunk.

**Advantage:**

- No sentence is ever cut in half, so every chunk reads like proper language.
- It is still simple and fast.

**Disadvantage:**

- Chunk sizes become uneven, because some sentences are very long and some are very short.
- It still groups blindly. Sentence number 5 may be the last line of one topic and sentence number 6 may be the first line of a completely new topic, and this strategy happily puts them in the same chunk.

The issue with this approach is that it respects sentences but it does not respect paragraphs and sections. Let's see how the next approach solve this issue.

## Recursive chunking

**Recursive chunking means we try to cut at the biggest natural boundary first, and only if the piece is still too big, we go down to a smaller boundary.**

This is the most commonly used strategy in real projects, and the idea behind it is beautiful.

Every document already has natural boundaries, and they have a natural order of importance:

- A blank line between paragraphs is a strong boundary.
- A single new line is a weaker boundary.
- A full stop is weaker than that.
- A space is the weakest one.

So, the strategy works like this. First, we try to split the document at blank lines. If a resulting piece is still bigger than our chunk size, then we take that piece alone and split it at new lines. If it is still too big, we split it at full stops. If it is still too big, we split it at spaces.

We keep going down the list only when we are forced to. That is why it is called recursive.

Let's see the code as below:

```python
def recursive_chunks(text, size=500, separators=["\n\n", "\n", ". ", " "]):
    if len(text) <= size or not separators:
        return [text]
    separator = separators[0]
    parts = text.split(separator)
    chunks = []
    for part in parts:
        if len(part) <= size:
            chunks.append(part)
        else:
            # still too big, so try the next weaker separator
            chunks.extend(recursive_chunks(part, size, separators[1:]))
    return chunks
```

Here, we can see that we always start with the strongest separator `"\n\n"`, and we call the same function again with the remaining weaker separators only for the parts that are still too big.

**Note:** This code is kept short just for the sake of understanding. A real implementation also merges the tiny neighbouring pieces back together until they reach the chunk size, so that we do not end up with a lot of one-line chunks.

**Advantage:**

- Most chunks end up matching real paragraphs, so they carry a complete idea.
- It never blows past our size limit, because in the worst case it falls back to splitting at spaces.
- It works well on almost every kind of document, which is why it is the default choice in most RAG systems.

**Disadvantage:**

- It follows the shape of the text, not the meaning of the text. If the writer put two unrelated ideas in one paragraph, this strategy keeps them together.

The issue with this approach is that it treats every document as plain text and ignores the headings that the document already gives us. Let's see how the next approach solve this issue.

## Document structure based chunking

**Document structure based chunking means we use the headings, sections, and tables that already exist in the document, and we cut along those lines.**

Many of our documents are not plain text. A Markdown file has `#` and `##` headings. An HTML page has `<h1>` and `<h2>` tags. A PDF has chapters. A code file has functions and classes.

The writer already told us where one topic ends and the next begins. It would be a waste to ignore that.

Let's say we have this Markdown document:

```markdown
# Leave Policy
## Paid Leave
Every employee gets 24 paid leave days in the first year.
## Sick Leave
Sick leave is limited to 12 days and needs a doctor note after 3 days.
```

If we cut at every `##` heading, we get two clean chunks. One chunk is fully about paid leave, and the other chunk is fully about sick leave. Nothing is mixed.

There is one more trick here that makes a big difference. **We must carry the parent headings into each chunk.** So, the second chunk should be stored like this:

```text
Leave Policy > Sick Leave
Sick leave is limited to 12 days and needs a doctor note after 3 days.
```

Here, we have added the heading path at the top. Now the chunk knows which document and which section it belongs to, even when it is pulled out alone.

**Advantage:**

- The boundaries are decided by the person who wrote the document, so they are usually perfect.
- Adding the heading path gives every chunk a clear identity.

**Disadvantage:**

- It only works when the document actually has structure. A plain transcript of a meeting or a scanned page has no headings at all.
- Sections can be very uneven. One section may be two lines and another may be twenty pages, so we still need a size-based split inside the big sections.

In practice, we combine this with recursive chunking. First, we split by headings, and then we split the oversized sections recursively. This combination handles almost every real document well.

The issue with this approach is that it still depends on someone having written good headings. Let's see how the next approach solve this issue.

## Semantic chunking

The word semantic simply means related to meaning.

**Semantic chunking means we cut the document at the exact points where the topic changes, and we find those points by measuring meaning.**

Till now, every strategy was cutting based on shape, which means characters, sentences, paragraphs, or headings. Semantic chunking is the first strategy that cuts based on meaning.

Here is how it works.

**Step 1:** We split the document into sentences.

**Step 2:** We turn every sentence into its embedding, which is that list of numbers we learned about earlier.

**Step 3:** We walk from one sentence to the next and measure how similar the two meanings are. Measuring the similarity simply means checking how close the two addresses sit. Close addresses mean the same topic.

**Step 4:** When two neighbouring sentences are still talking about the same thing, the similarity is high, so we keep them together. When the similarity suddenly drops, it means the topic just changed, so we cut there.

Let's see it with an example:

```text
1. Every employee gets 24 paid leave days in the first year.
2. These days do not carry forward to the next year.
3. The office cafeteria is open from 8 AM to 6 PM.
4. It serves breakfast, lunch, and evening snacks.
```

Sentence 1 and sentence 2 are both about leave, so their similarity is high. Sentence 2 and sentence 3 are about two totally different things, so the similarity drops sharply. That drop is our cut point.

So, we get two chunks. One is about leave, and one is about the cafeteria. This is exactly what we wanted, and notice that no heading was needed.

**Advantage:**

- The boundaries follow the actual topics, so each chunk is genuinely about one thing.
- It works even on documents with no headings at all, like transcripts and chat logs.

**Disadvantage:**

- It is slow and costly, because we have to create an embedding for every single sentence before we can even start chunking.
- We have to tune the drop threshold. The threshold is the limit we set for deciding how big a drop counts as a topic change. If the threshold is too sensitive, we get hundreds of tiny chunks. If it is not sensitive enough, we get very few huge chunks.
- On a document that has one long flowing topic, it gives no clear cut points at all.

The issue with this approach is that even a perfectly cut chunk can still be useless on its own. Let's see why, and how the next approach solve this issue.

## Contextual chunking

Let's understand the problem first, because this problem is very easy to miss.

Assume that our chunking worked perfectly and we got this clean chunk:

```text
The limit was raised to 18 days from April, and the doctor note
requirement was removed.
```

Now, the user asks, "What is the current sick leave limit?"

This chunk has the exact answer, but read it once again carefully. It never says the words sick leave. It says "the limit". A human reading the full document knows which limit, because the heading two pages above said Sick Leave. But this chunk is stored alone in the database, with no memory of where it came from.

So, its meaning address is vague, and it never gets retrieved. **A chunk that loses its context loses its usefulness.**

So, here comes the contextual chunking to the rescue.

**Contextual chunking means we add a short line of context to the top of each chunk before we store it, so that the chunk can stand on its own.**

The fixed chunk looks like this:

```text
From the Employee Handbook, Leave Policy section, about sick leave:
The limit was raised to 18 days from April, and the doctor note
requirement was removed.
```

Now the chunk carries its own identity. The words sick leave are present, the section is present, and the source is present. The question now matches it easily.

There are two common ways to write this context line.

**The cheap way:** We build it from the metadata we already have. Metadata means the extra information we know about the chunk, like the file name and the heading path. This costs nothing and helps a lot.

**The costly way:** We send the chunk along with the full document to a language model and ask it to write one short line explaining what this chunk is about in the context of the document. This gives a better result, but we pay for one model call per chunk. This costly way is the idea behind [Contextual Retrieval](https://outcomeschool.com/blog/how-does-contextual-retrieval-work).

**Advantage:**

- Retrieval accuracy improves a lot, especially for chunks full of pronouns like "it", "this", and "the above".
- It works on top of any other strategy, so we never have to choose between them.

**Disadvantage:**

- The costly way needs one model call per chunk during indexing.
- The context line takes up some space inside every chunk.

**Note:** This is one of the highest value improvements we can do, and the cheap way costs us almost nothing. We must not skip it.

The issue with this approach is that we are still stuck between two needs. A small chunk searches well but answers poorly, and a big chunk answers well but searches poorly. Let's see how the next approach solve this issue.

## Small-to-big chunking

Let's understand the tug of war first.

- A small chunk has one sharp meaning, so the search finds it easily. But when it reaches the model, it is too thin. The model does not have enough surrounding information to answer well.
- A big chunk gives the model plenty of information to answer with. But its meaning is an average of many things, so the search struggles to find it.

We want both. We want to search with something small and answer with something big.

**Small-to-big chunking means we search using small chunks, but we send the bigger surrounding piece to the model.**

Here is how it works. We cut the document twice. First, we cut it into big parent chunks, let's say full sections. Then we cut each parent into small child chunks, let's say single sentences or short paragraphs. We store only the child embeddings in the vector database, and we keep a note on each child saying which parent it came from.

At query time, we search over the children. When a child matches, we throw away the child and send its parent to the model.

Let's see it with an example:

```text
Parent chunk: The full "Sick Leave" section, 12 sentences long.
Child chunks stored for search:
  - "Sick leave is limited to 12 days."      -> parent: Sick Leave
  - "A doctor note is needed after 3 days."  -> parent: Sick Leave
  - "The limit was raised to 18 days."       -> parent: Sick Leave
```

The user asks, "Do I need a doctor note for sick leave?"

The second child matches sharply, because that child is about nothing else. But instead of sending that one thin line, we send the whole Sick Leave section. Now the model can see the number of days, the doctor note rule, and the April update, all together, so it writes a complete answer.

This is how we get sharp search and rich answers at the same time.

**Advantage:**

- It gives us the best of both sides, precise retrieval and complete context.
- It removes the awkward hunt for one perfect chunk size, because we no longer need one size to do both jobs.

**Disadvantage:**

- We have to store and manage two levels of chunks, so the indexing pipeline becomes more complex.
- The final prompt becomes bigger, so the cost per question goes up.
- If several matching children belong to the same parent, we must remove the duplicates before sending, otherwise we send the same parent twice.

So, till now, every strategy was following a rule that we wrote by hand. Now, let's see the strategy where we stop writing the rule ourselves.

## Agentic chunking

**Agentic chunking means we hand the document to a language model and let the model itself decide where the cuts should be.**

In all the earlier strategies, we were the ones deciding the rule. In this one, we let the model read the document like a human editor would and mark the boundaries.

We give it an instruction like below:

```text
Read the document below. Split it into pieces where each piece
covers exactly one complete idea. Do not break a table or a list
in the middle. Give each piece a one-line title.
```

The model returns the pieces along with the titles, and we store those as our chunks.

**Advantage:**

- It handles the ugly cases that rules cannot handle, like a table split across two pages, a numbered list, or a legal clause that must never be broken.
- The one-line title it gives us works as free context for each chunk.

**Disadvantage:**

- It is the slowest and the most expensive option by a wide margin.
- It is not repeatable. Running it twice on the same document can give two different sets of chunks.
- It does not scale to millions of documents.

So, we must use this only for a small set of high-value and messy documents, like contracts, medical notes, or financial filings. For everything else, the earlier strategies are far more practical.

The same idea also shows up on the retrieval side, where an agent decides what to fetch and when. We have a detailed blog on [Agentic RAG](https://outcomeschool.com/blog/agentic-rag) that covers this end to end.

Now, we have understood all the strategies. Now, let's move to the two settings that we must get right no matter which strategy we pick.

## Chunk overlap

**Chunk overlap means we repeat the last few lines of one chunk at the start of the next chunk.**

Let's understand why we need it.

Even with a good strategy, a cut has to happen somewhere. And sometimes the answer sits right on top of that cut. Half of it is at the end of chunk 1 and half of it is at the start of chunk 2, so neither chunk can answer the question fully.

Overlap is the safety net for exactly this case.

Let's see it with an example. Without overlap:

```text
Chunk 1: ... Leave must be applied 7 days in advance.
Chunk 2: Emergency leave is an exception to this rule. ...
```

Here, chunk 2 says "this rule", but the rule itself is sitting in chunk 1. If only chunk 2 is retrieved, the model has no idea what rule is being talked about.

Now, with overlap:

```text
Chunk 1: ... Leave must be applied 7 days in advance.
Chunk 2: Leave must be applied 7 days in advance. Emergency leave
         is an exception to this rule. ...
```

Here, we have repeated the last sentence of chunk 1 at the start of chunk 2. Now chunk 2 is complete on its own. The problem is solved.

A common setting is an overlap of about 10 to 20 percent of the chunk size. So, for a chunk of 500 tokens, an overlap of 50 to 100 tokens works well.

**Note:** Overlap is not free. Every repeated line is stored again and embedded again, so our database grows. Too much overlap also means the same text gets retrieved multiple times, which wastes space in the prompt. So, we must keep the overlap small.

## How to choose the chunk size

This is the question everyone asks, and there is no single correct number. But there is a very reliable way to decide, and it comes from one simple idea.

**The chunk size must match the size of one complete answer in our data.**

Let's see what this means with three cases.

**Case 1: Short and factual answers.** A product catalogue, a FAQ page, or a list of definitions. Each answer is one or two lines. Here, small chunks of about 200 to 300 tokens work best, because each chunk holds exactly one fact and nothing extra.

**Case 2: Explanations and procedures.** A technical document, a policy handbook, or a tutorial. Each answer is a paragraph or two. Here, medium chunks of about 500 to 800 tokens work best. This is the safe default for most projects.

**Case 3: Long reasoning and narratives.** Research papers, legal contracts, or meeting transcripts. The answer needs a lot of surrounding argument to make sense. Here, larger chunks of about 1000 to 1500 tokens work better, and small-to-big chunking helps even more.

Here is the practical way to find our own number. We take about 20 real questions that our users would actually ask. We build the system with a chunk size of 500 and an overlap of 50, and we check for each question whether the correct chunk came back in the top results. Then we try 300 and 1000 and compare the same 20 questions. The number that wins is our number.

> Measure with real questions, not with guesses.

**Very important:** The embedding model also has a limit on how much text it can read. If our chunk is longer than that limit, the extra text is silently thrown away and never becomes part of the meaning address. So, we must always keep our chunk size within the limit of the embedding model we are using.

## Comparison of all the strategies

Let me tabulate the differences between all the chunking strategies for your better understanding so that you can decide which one to use based on your use case.

| Strategy | How it cuts | Cost | Quality | Best for |
| --- | --- | --- | --- | --- |
| Fixed-size | After N characters | Very low | Low | Quick prototypes, messy text |
| Sentence | At full stops | Very low | Low to medium | Short and clean text |
| Recursive | At paragraphs, then smaller | Low | Good | The default for most projects |
| Document structure | At headings and sections | Low | Very good | Markdown, HTML, PDFs with headings |
| Semantic | Where the topic changes | High | Very good | Transcripts and text with no headings |
| Contextual | Adds context to any chunk | Medium to high | Very good | Any document with pronouns and references |
| Small-to-big | Search small, send big | Medium | Very good | Long documents needing full context |
| Agentic | The model decides | Very high | Excellent | Small sets of critical messy documents |

Here, we can see that these strategies are not all competing with each other. Contextual chunking and small-to-big chunking sit on top of the others rather than replacing them.

So, a very strong and very practical setup looks like this.

First, we clean the document and split it by its headings. Then, we split the oversized sections recursively with a small overlap. After that, we add a short context line to every chunk. Finally, for the long sections, we search with the small children and send the parent to the model.

This combination is simple to build, cheap to run, and it covers almost every real case. We can always add semantic chunking or agentic chunking later for the few documents that need it, depending on our use case.

## Common mistakes

Most of the time, we do mistakes while doing the chunking. Let's see the most common ones so that we can avoid them.

**Mistake 1: Chunking the raw file directly.** A PDF converted carelessly gives us page numbers, headers, and footers repeated on every page. These get mixed into our chunks and pollute the meaning. We must clean the text before chunking.

**Mistake 2: Breaking tables and code blocks.** Half a table is worse than no table. We must keep tables, code blocks, and lists together as one unit, even when they cross our size limit.

**Mistake 3: Storing no metadata.** We must store the source file, the section, the page number, and the date along with every chunk. This lets us filter the search, and it lets us show the user where the answer came from.

**Mistake 4: Using one chunk size for every kind of document.** A FAQ page and a legal contract need very different sizes. We must chunk each type of document with settings that suit it.

**Mistake 5: Never measuring.** Many teams pick a chunk size once and never check it again. We must build a small set of test questions and measure, because that is the only honest way to know if our chunking is working.

**Mistake 6: Forgetting to re-index after a change.** The moment we change the chunk size, the overlap, or the embedding model, every stored embedding becomes stale. We must rebuild the whole index.

## Conclusion

Chunking looks like a small step in the middle of a RAG pipeline, but it decides everything that comes after it. If the right piece of text never gets retrieved, then no amount of clever prompting and no bigger model can save the answer.

The rule to remember is a simple one. **One chunk must hold one complete idea, and it must make sense when read completely alone.** Every strategy we learned is just a different way of reaching that same goal.

So, we must start with recursive chunking, respect the headings of the document, add a line of context to every chunk, keep a small overlap, and measure with real questions. This way we can use chunking to solve the retrieval problem in a very simple way.

There is also a line of thinking where we skip the cutting altogether and let the model walk the structure of the whole document instead. We have a detailed blog on [Vectorless RAG](https://outcomeschool.com/blog/vectorless-rag) that explains how retrieval works without any chunks and without a vector database.

Now we must have understood the chunking strategies for RAG.

## Frequently Asked Questions

### Which chunking strategy should we use by default for RAG?

Recursive chunking is the default choice for most RAG systems. A strong practical setup splits the document by its headings, splits oversized sections recursively with a small overlap, adds a short context line to every chunk, and uses small-to-big chunking for long sections. Semantic or agentic chunking can be added later for the few documents that need it.

### Do we still need chunking if the whole document fits in the context window?

Yes. Sending a huge document every single time is slow and expensive, because we pay for every token we send. Accuracy also drops, since the useful line gets buried and the model starts mixing up facts. Three short and relevant chunks give a cleaner answer.

### Can a chunk be longer than the embedding model's limit?

It should not be. If a chunk is longer than the limit of the embedding model, the extra text is silently thrown away. That text never becomes part of the meaning address of the chunk. So, we must always keep the chunk size within the limit of the embedding model we are using.

### Do we need to re-index after changing the chunk size?

Yes. The moment we change the chunk size, the overlap, or the embedding model, every stored embedding becomes stale. We must rebuild the whole index.

### Should we split tables and code blocks across chunks?

No. Half a table is worse than no table. We must keep tables, code blocks, and lists together as one unit, even when they cross our size limit.
