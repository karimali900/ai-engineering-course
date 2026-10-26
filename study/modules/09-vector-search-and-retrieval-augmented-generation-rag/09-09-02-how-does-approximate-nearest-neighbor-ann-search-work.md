---
title: How does Approximate Nearest Neighbor (ANN) search work?
module: 9
module_title: Vector Search and Retrieval-Augmented Generation (RAG)
lesson: '9.2'
source: https://outcomeschool.com/blog/how-does-approximate-nearest-neighbor-ann-search-work
published: June 29, 2026
tags:
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 4079
reading_time: 20
status: full
---
# How does Approximate Nearest Neighbor (ANN) search work?

> **Module 9 · Lesson 9.2**  
> Source: [Outcome School](https://outcomeschool.com/blog/how-does-approximate-nearest-neighbor-ann-search-work) · Published: June 29, 2026 · Reading time: ~20 min · Tags: `ai`, `system-design`

---

![How does Approximate Nearest Neighbor (ANN) search work?](../../assets/images/09-09-02-how-does-approximate-nearest-neighbor-ann-search-work/how-does-approximate-nearest-neighbor-ann-search-work.png)

Approximate Nearest Neighbor (ANN) Search finds an item that is very close to the true most similar one, but much faster, by using clever shortcuts and allowing a tiny chance of not being perfectly exact.

In this blog, we will learn about Approximate Nearest Neighbor (ANN) Search, the idea that lets apps find "similar" things in a huge collection in the blink of an eye. It powers search engines, recommendation systems, face matching, and the memory behind modern AI chatbots. We will also see why the naive approach fails, how trees, hashing, clustering, and graphs make the search fast, and where ANN search is used in the real world.

We will cover the following:

- What is Nearest Neighbor Search?
- How do we turn things into numbers (vectors)?
- How do we measure "closeness"?
- The naive approach and why it fails
- What is Approximate Nearest Neighbor (ANN) Search?
- The trade-off: speed vs accuracy
- Approach 1: Trees (KD-Tree)
- Approach 2: Hashing (LSH)
- Approach 3: Clustering (IVF)
- Approach 4: Graphs (HNSW)
- A simple code example
- Where ANN Search is used
- Picking the right method

Let's get started.

### What is Nearest Neighbor Search?

**Nearest Neighbor Search means finding the item in a collection that is the most similar to a given item.**

A **neighbor** is something that lives close to us. The **nearest** neighbor is the one that lives closest of all.

Let's say we walk into a music app and play one song. The app then says, "Here are songs similar to this one." To do that, the app looked at its whole library and found the songs that are closest in style to the one we played. That is nearest neighbor search.

Here are some everyday examples of the same idea:

- We upload a photo, and the app finds similar-looking photos.
- We type a question, and a search engine finds the most relevant answers.
- We watch one video, and the app suggests the next similar video.

So, nearest neighbor search is simply "find me the most similar thing". Now, the question is: how does a computer measure how similar two things are? For that, we first need numbers.

### How do we turn things into numbers (vectors)?

A computer does not understand a song, a photo, or a sentence directly. It only understands numbers. So, the first step is to turn every item into a list of numbers.

This list of numbers is called a **vector**.

> Vector = a list of numbers that describes an item

In simple words, a vector is like a fingerprint made of numbers. Each item gets its own fingerprint.

Let's say we describe a person using just two numbers: their age and their height. Then a person becomes a vector of two numbers, like below:

```
   Person A  ->  [ 25, 170 ]
   Person B  ->  [ 27, 172 ]
   Person C  ->  [ 60, 165 ]
```

Here, we can see that each person is now a list of two numbers. Person A and Person B have similar numbers, so they are similar. Person C has a very different age, so Person C is far from the other two.

Real items like photos and sentences are not described by just two numbers. They are described by hundreds or even thousands of numbers. A special kind of model, called an **[embedding model](https://outcomeschool.com/blog/what-are-embeddings)**, reads an item and produces this vector for us. We do not need to know how it works right now. We just need to know that it turns any item into a vector, and similar items get similar vectors. We have a detailed blog on [Contrastive Learning](https://outcomeschool.com/blog/contrastive-learning) that explains how models learn to give similar items similar vectors.

So, every song, photo, and sentence becomes a point in space described by numbers. Now, let's learn how to measure the distance between two such points.

### How do we measure "closeness"?

Once everything is a vector, "similar" becomes "close", and "different" becomes "far". So, we need a way to measure the distance between two vectors.

The most common way is **Euclidean distance**. This is just the straight-line distance between two points, the same distance we measure with a ruler.

Let's take two simple vectors with two numbers each:

```
   A = [ 1, 2 ]
   B = [ 4, 6 ]
```

We find the difference in each number, square it, add them, and take the square root:

- difference in first number: 4 - 1 = 3
- difference in second number: 6 - 2 = 4
- distance = square root of (3 squared + 4 squared) = square root of (9 + 16) = square root of 25 = 5

So, the distance between A and B is 5. A smaller distance means the two items are more similar.

We can picture these two points on a simple grid like below:

```
   6 -|                 B (4,6)
   5 -|                /
   4 -|               /
   3 -|              /  distance = 5
   2 -|   A (1,2)---/
   1 -|
   0 -+----------------------
       0  1  2  3  4  5  6
```

Here, we can see two points A and B on a grid. The straight line connecting them is the Euclidean distance, and its length is 5. The closer two points sit, the shorter this line, and the more similar the items are.

**Note:** There is another popular measure called **cosine similarity**, which looks at the angle between two vectors instead of the gap between them. It is widely used for text. For now, we just need the core idea: there is a number that tells us how close two vectors are.

So, now finding the nearest neighbor means finding the vector with the smallest distance to our query. Let's see the simplest way to do that.

### The naive approach and why it fails

The most obvious way to find the nearest neighbor is to check every single item.

We take our query vector, measure its distance to every vector in the collection, and keep the one with the smallest distance. This is called the **brute-force** approach, and it is also called **exact** search because it always gives the perfect answer.

Let's see this approach like below:

```
   query  ----compare---->  item 1   (distance = 12)
   query  ----compare---->  item 2   (distance = 3)   <- closest so far
   query  ----compare---->  item 3   (distance = 9)
   query  ----compare---->  item 4   (distance = 7)
   ...
   query  ----compare---->  item N   (distance = 5)
```

Here, we can see that we compare the query against every single item, one by one, and pick the smallest distance. For a small collection, this works perfectly.

But, here is the catch. Real collections are huge.

Let's say we have one billion vectors, and each vector has 1000 numbers. To answer one query, we must do one billion distance calculations, and each calculation touches 1000 numbers. That is a thousand billion operations for a single search. And large apps handle thousands of searches every second.

So, the brute-force approach is too slow. It does not scale. We need something much faster.

So, here comes Approximate Nearest Neighbor Search to the rescue.

### What is Approximate Nearest Neighbor (ANN) Search?

**Approximate Nearest Neighbor Search means finding a neighbor that is very close to the true nearest one, but much faster, by allowing a tiny chance of not being perfectly exact.**

In simple words, instead of checking every item, we use clever shortcuts that look at only a small part of the collection and still find an answer that is almost always correct.

Let's decompose the term:

> Approximate Nearest Neighbor = Approximate + Nearest Neighbor

**Approximate** means "very close to correct, but not guaranteed to be perfect". **Nearest Neighbor** is the most similar item, which we already learned.

The best way to understand this is by taking an example. Suppose we are in a giant library and we want a book on cooking. The brute-force way is to read the title of every single book in the building. That is perfect but extremely slow.

The smart way is to walk straight to the "Food and Cooking" section and look only there. We may not find the single best cookbook in the entire building, but we will almost certainly find an excellent one, and we will find it in seconds.

That is exactly what ANN does. It organizes the data in advance so that, at search time, it can jump to the right neighborhood and ignore everything else.

So, ANN trades a tiny bit of accuracy for a massive gain in speed. For almost every real app, this trade is more than worth it.

### The trade-off: speed vs accuracy

Before we learn the methods, we must understand the one idea that connects all of them: the trade-off between speed and accuracy.

In ANN, we measure quality using a number called **[recall](https://outcomeschool.com/blog/precision-vs-recall)**.

**Recall is the percentage of times the approximate answer matches the true nearest neighbor.**

A recall of 100 percent means the approximate answer is always perfect. A recall of 95 percent means it is correct 95 times out of 100, and slightly off the other 5 times. In practice, being slightly off usually means returning the second or third closest item instead of the very closest, which is perfectly fine for most apps.

We can picture the trade-off like below:

```
   brute-force        ANN (tuned for          ANN (tuned for
   (exact)            high accuracy)           high speed)
   recall: 100%       recall: ~99%             recall: ~90%
   speed:  slow       speed:  fast             speed:  very fast
```

Here, we can see the whole picture. As we push for more speed, recall drops a little. As we push for more accuracy, speed drops a little. Every ANN method gives us a knob to balance these two, and we tune it based on our use case.

Now, let's learn the main approaches that make ANN fast. We will build them up one by one.

### Approach 1: Trees (KD-Tree)

The first idea is to split the space into smaller and smaller regions, so we only search the region our query falls into.

A popular method here is the **KD-Tree**. The "KD" stands for "K-Dimensional", which simply means it works with vectors that have many numbers.

In simple words, a KD-Tree keeps cutting the space in half, again and again. Each cut sends us down one branch and lets us ignore the other branch.

Let's say all our points are spread on a flat board. First, we draw a vertical line that splits the points into left and right. Then, inside each side, we draw a horizontal line that splits them into top and bottom. We keep doing this, building a tree of cuts.

We can picture the tree like below:

```
                    [ all points ]
               split by a vertical line
                 /                  \
        left region              right region
        /         \              /          \
   sub-region   sub-region   sub-region   sub-region
```

Here, we can see that the whole space is cut into a tree of regions. When a query arrives, we follow the cuts down to the small region where it belongs, and we only compare against the few points in that region. We skip the rest of the tree.

**The issue with this approach is that it works well only when each vector has few numbers.** When vectors have hundreds of numbers, the cuts stop being helpful, and we end up checking almost everything anyway. This problem of high-dimensional data is famously called the **curse of dimensionality**.

So, trees are great for low-dimensional data but weak for the large, high-dimensional vectors used in modern AI. Let's see how the next approach solves this issue.

### Approach 2: Hashing (LSH)

The next idea is to use a smart shortcut called **hashing**.

Normally, hashing turns an item into a short code, and very different items get very different codes. But for ANN, we use a special twist called **Locality Sensitive Hashing**, or **LSH**.

**Locality Sensitive Hashing is a method that gives similar items the same code on purpose, so they land in the same bucket.**

In simple words, LSH groups similar vectors into the same "bucket". At search time, we look only inside the query's bucket instead of the whole collection.

Let's say we sort thousands of marbles into a few boxes, and we make sure that marbles of similar color always go into the same box. Later, to find marbles similar to a red one, we open only the red box. We ignore all the other boxes.

We can picture LSH like below:

```
   all vectors  ---LSH--->   Bucket 1: [ v3, v9, v14 ]
                             Bucket 2: [ v1, v7 ]
                             Bucket 3: [ v2, v5, v8, v11 ]   <- query lands here
   query  ---LSH--->  Bucket 3, so compare only with v2, v5, v8, v11
```

Here, we can see that LSH first drops every vector into a bucket. When a query arrives, we run the same hashing on it, find its bucket, and compare only with the few vectors in that bucket. We skip every other bucket.

**The advantage** is that this is very fast and uses simple, fixed rules. **The disadvantage** is that the accuracy can be uneven. Sometimes a true neighbor lands in a different bucket and we miss it. To fix this, we use several hash tables at once, which uses more memory.

So, LSH is fast and simple, but to get high accuracy it needs extra memory. Let's see how the next approach handles this.

### Approach 3: Clustering (IVF)

The next idea is to group nearby vectors into clusters in advance, and then search only the clusters closest to our query.

This method is called **IVF**, which stands for **Inverted File Index**. The name sounds heavy, but the idea is simple.

In simple words, we divide all the vectors into groups, where each group has a representative center point, and at search time we only open the few groups whose centers are nearest to the query.

The best way to learn this is by taking an example. Suppose we sort all the people in a country by which city they live in. Each city has a center. To find people near a given location, we first find the nearest city or two, and then look only at the people in those cities. We do not scan the whole country.

This happens in two phases.

**Step 1: Build the clusters (done once, in advance).** We group all the vectors into clusters. Each cluster gets a center point that represents it. This grouping step is often done using a method called **k-means**, which simply finds natural groups in the data.

**Step 2: Search (done for every query).** When a query arrives, we first compare it only with the cluster centers, which are very few. We pick the nearest few clusters. Then we compare the query only with the vectors inside those chosen clusters.

We can picture IVF like below:

```
   Cluster A (center cA): [ v1, v4, v8 ]
   Cluster B (center cB): [ v2, v6 ]
   Cluster C (center cC): [ v3, v5, v7, v9 ]
   Step 1: query vs centers ->  cA, cB, cC   (pick nearest: cC)
   Step 2: query vs members of C only -> v3, v5, v7, v9
```

Here, we can see that we first compare the query against a handful of cluster centers, not the whole collection. Then we open only the nearest cluster and compare against the vectors inside it. Everything else is skipped.

There is a knob here called `nprobe`, which decides how many clusters we open. If we open more clusters, we get higher accuracy but slower speed. If we open fewer clusters, we get more speed but lower accuracy. We tune `nprobe` based on our use case.

So, IVF gives us a clean balance and scales to billions of vectors. But we can have an even smarter approach than this too.

### Approach 4: Graphs (HNSW)

The most popular ANN method today is based on graphs. It is called **HNSW**, which stands for **Hierarchical Navigable Small World**.

The name is long, so let's decompose it.

A **graph** is just a set of points connected by links. Here, each vector is a point, and we connect each vector to its nearby vectors with links. To find a neighbor, we hop from point to point along the links, always moving closer to the query. This is the "Navigable" part.

The **Hierarchical** part means we build several layers of this graph, stacked on top of each other. The top layer is sparse and has only a few points with long links. Each lower layer is denser. We start our search at the top, take big jumps to get close fast, and then drop into the lower, denser layers to fine-tune the answer.

The best way to understand this is by taking an example. Think of how we travel between two cities. First, we take a highway to cover most of the distance quickly, which is the top layer. Then, we take main roads, which is the middle layer. Finally, we take small local streets to reach the exact house, which is the bottom layer.

We can picture the layers like below:

```
   Top layer (few points, long jumps)
      A -------------------- F
       \                    /
        \                  /
   Middle layer (more points)
      A ---- C ---- D ---- F
       \    /  \   /  \   /
   Bottom layer (all points, short hops)
      A - B - C - D - E - F - G   <- final answer found here
```

Here, we can see the journey. We enter at the top layer and take large jumps to get into the right area quickly. Then we move down layer by layer, taking smaller and smaller hops, until we reach the closest point in the dense bottom layer. We never touch the points that are far away.

This greedy hopping is extremely fast and gives very high accuracy. This is why HNSW is the default choice in most modern [vector databases](https://outcomeschool.com/blog/how-does-a-vector-database-work).

**The advantage** is excellent speed and accuracy together. **The disadvantage** is that the graph uses more memory and takes longer to build than the other methods. But for most apps, the search speed matters most, so HNSW wins.

So, now we have learned the four main families of ANN: trees, hashing, clustering, and graphs.

### A simple code example

Now, let's see ANN in action using a popular open-source library called FAISS, which is built for fast vector search. We will use the IVF method we just learned. Let's see the code as below:

```python
import faiss
import numpy as np
# Suppose we have 100000 vectors, each with 128 numbers
dimension = 128
data = np.random.random((100000, dimension)).astype("float32")
# Build an IVF index with 100 clusters
quantizer = faiss.IndexFlatL2(dimension)
index = faiss.IndexIVFFlat(quantizer, dimension, 100)
# Step 1: learn the clusters from the data
index.train(data)
# Step 2: add all the vectors into the index
index.add(data)
# Open 10 nearest clusters per query (the nprobe knob)
index.nprobe = 10
# Search: find the 5 nearest neighbors of one query vector
query = np.random.random((1, dimension)).astype("float32")
distances, neighbors = index.search(query, 5)
print(neighbors)
```

Here, we have built an ANN search system, and let me explain each part.

- `data` is our collection of 100000 vectors, each with 128 numbers.
- `IndexIVFFlat(quantizer, dimension, 100)` creates an IVF index that splits the data into 100 clusters.
- `index.train(data)` is Step 1. It learns the cluster centers from the data.
- `index.add(data)` is Step 2. It places every vector into its nearest cluster.
- `index.nprobe = 10` is the knob. It tells the search to open the 10 nearest clusters per query. A higher value gives more accuracy but less speed.
- `index.search(query, 5)` finds the 5 nearest neighbors of the query, returning their distances and positions.

So, in just a few lines, we have built a fast search over 100000 vectors without comparing against every single one. It works perfectly.

### Where ANN Search is used

Now, let's discuss where ANN Search is used in the real world. We use it far more often than we realize.

- **[Semantic search](https://outcomeschool.com/blog/how-does-semantic-search-work):** When a search bar understands the meaning of our words, not just exact keywords, ANN finds the closest matching documents.
- **Recommendation systems:** When an app suggests the next song, video, or product, ANN finds items similar to what we already liked.
- **Image search:** When we search by an image and get visually similar images, ANN is matching the [picture vectors](https://outcomeschool.com/blog/how-do-image-embeddings-work).
- **Face recognition:** When a phone or a photo app groups the same person together, ANN matches face vectors.
- **RAG for AI chatbots:** Modern AI assistants use a technique called **Retrieval Augmented Generation**, which means the model first fetches relevant facts from a large knowledge store before answering. ANN is the engine that fetches those relevant facts quickly. This is why ANN sits at the heart of vector databases like FAISS and Qdrant.
- **Semantic caching:** When an AI app reuses a past answer for a new question that means the same thing, ANN finds the closest saved question so the app can skip calling the model again. This is [how Semantic Caching works](https://outcomeschool.com/blog/how-does-semantic-caching-work).
- **Detecting duplicates:** When a platform finds near-duplicate articles, photos, or products, ANN spots the close matches.

So, now we know where we can use ANN Search.

In a search or RAG pipeline, ANN usually fetches a rough shortlist of candidates, and then a reranker reorders that shortlist so the most relevant items rise to the top. We have a detailed blog on [how a Reranker works](https://outcomeschool.com/blog/how-does-a-reranker-work) that explains this step by step.

On the RAG side, there is also an approach that skips this whole numeric search. We have a detailed blog on [Vectorless RAG](https://outcomeschool.com/blog/vectorless-rag) that explains how a model reaches the right section by reading the structure of a document instead of measuring distances.

### Picking the right method

Now, let me tabulate the differences between the main ANN methods for your better understanding so that you can decide which one to use based on your use case.

| Method | Core idea | Strength | Weakness |
| --- | --- | --- | --- |
| KD-Tree | Split space into regions | Simple, exact for few numbers | Fails for many numbers |
| LSH | Group similar items into buckets | Fast and simple | Needs extra memory for accuracy |
| IVF | Cluster and search nearest clusters | Scales to billions, balanced | Needs tuning of clusters |
| HNSW | Hop through a layered graph | Best speed and accuracy together | Uses more memory to build |

For very large data where we want the best speed and accuracy and have enough memory, HNSW is usually the top choice. For huge data where we must save memory, IVF is excellent. For simple, low-dimensional data, a tree can be enough.

This was all about Approximate Nearest Neighbor Search.

ANN turns the slow task of comparing against everything into a fast task of looking only at the right neighborhood. We first turn items into vectors, then measure closeness as distance, and finally use a clever structure like a tree, hash buckets, clusters, or a graph to skip almost all the work. We give up a tiny bit of perfect accuracy and gain enormous speed, and that is exactly the trade that makes modern search, recommendations, and AI assistants feel instant.

## Frequently Asked Questions

### Does ANN search always return the exact nearest neighbor?

No. ANN search does not guarantee the exact nearest neighbor. It allows a tiny chance of not being perfectly exact. When it is off, it usually returns the second or third closest item instead of the very closest, which is perfectly fine for most apps.

### Why not just use brute-force search instead of ANN?

Brute-force search is exact, but it is too slow for large collections. With one billion vectors of 1000 numbers each, one query needs a thousand billion operations. Large apps handle thousands of searches every second, so brute-force does not scale, and ANN looks at only a small part of the collection instead.

### Which ANN method should we use, HNSW or IVF?

HNSW is usually the top choice when we want the best speed and accuracy together and have enough memory. IVF is excellent for huge data where we must save memory. HNSW uses more memory and takes longer to build, while IVF scales to billions of vectors but needs tuning of clusters.

### Why does a KD-Tree not work well for AI embeddings?

A KD-Tree works well only when each vector has few numbers. Modern AI vectors have hundreds of numbers, and at that size the cuts stop being helpful, so we end up checking almost everything anyway. This problem is called the curse of dimensionality.

### What does the nprobe setting control in IVF?

The `nprobe` setting decides how many clusters we open for each query. Opening more clusters gives higher accuracy but slower speed. Opening fewer clusters gives more speed but lower accuracy. We tune it based on our use case.
