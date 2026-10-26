---
title: How do Top-k and Top-p Sampling work?
module: 4
module_title: How LLMs Generate Text
lesson: '4.2'
source: https://outcomeschool.com/blog/how-do-top-k-and-top-p-sampling-work
published: September 19, 2026
tags:
- llm
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 3580
reading_time: 18
status: full
---
# How do Top-k and Top-p Sampling work?

> **Module 4 · Lesson 4.2**  
> Source: [Outcome School](https://outcomeschool.com/blog/how-do-top-k-and-top-p-sampling-work) · Published: September 19, 2026 · Reading time: ~18 min · Tags: `llm`, `ai`, `system-design`

---

![How do Top-k and Top-p Sampling work?](../../assets/images/04-04-02-how-do-top-k-and-top-p-sampling-work/how-do-top-k-and-top-p-sampling-work.png)

Top-k Sampling keeps only the k most likely tokens and picks randomly from them, whereas Top-p Sampling keeps the smallest group of top tokens whose probabilities add up to at least p, and picks randomly from that group.

In this blog, we will learn about how Top-k and Top-p Sampling work, the two most common ways an LLM decides which word to write next when it is replying to us. We will also see how an LLM picks one token at a time, why always picking the best token gives boring text, why picking from every token gives silly text, how Top-k keeps a fixed number of tokens, how Top-p keeps tokens based on their total probability, how both of them work with temperature, and when to use which one.

We will cover the following:

- How an LLM picks the next token
- The problem with always picking the best token
- The problem with picking from every token
- What is Top-k Sampling?
- Step-by-step example of Top-k Sampling
- The problem with Top-k Sampling
- What is Top-p Sampling?
- Step-by-step example of Top-p Sampling
- Top-k vs Top-p Sampling
- How Top-k and Top-p work with Temperature
- When to use which one

Let's get started.

## How an LLM picks the next token

Before jumping into Top-k and Top-p Sampling, we must know how an LLM writes text.

An LLM does not write a full sentence in one go. It writes one token at a time.

A **[token](https://outcomeschool.com/blog/tokenization-in-llms)** is a small piece of text. It can be a full word like "cat", a part of a word like "ing", or even a comma. For the sake of understanding, we can think of a token as a word.

Let's say we give the LLM the text "The cat sat on the". Now, the LLM has to decide the next token.

Inside the LLM, there is a list of every token it knows. This list is called the **vocabulary**. It is huge, it contains tens of thousands of tokens.

For every token in the vocabulary, the LLM gives a score. A higher score means the LLM thinks that token is a better fit as the next token. These raw scores are called **logits**.

Then, the LLM converts these scores into probabilities using a function called **softmax**. Do not worry, we do not need to go deep into softmax here. In simple words, softmax takes all the scores and turns them into percentages that add up to 100%. A probability is just the chance of that token being the next one. 40% means 40 chances out of 100.

We have a detailed blog on [Cross-Entropy Loss](https://outcomeschool.com/blog/math-behind-cross-entropy-loss) that explains logits and softmax step by step.

So, for "The cat sat on the", the LLM gives probabilities like below:

| Token | Probability |
| --- | --- |
| mat | 40% |
| floor | 25% |
| sofa | 15% |
| bed | 10% |
| roof | 5% |
| every other token | 5% in total |

Here, we can see that "mat" has the highest probability, and thousands of other tokens together share the remaining 5%.

**Note:** We are showing only a few tokens in the table just for the sake of understanding. In a real LLM, this table has one row for every token in the vocabulary.

Now, the LLM has to pick one token from this list. This picking step is called **sampling**. The rule we follow while picking is called the **decoding strategy**.

Once a token is picked, it is added to the text, and the whole process repeats for the next token. This continues till the reply is complete. This way of writing, one token at a time, is called autoregressive generation, and we have a detailed blog on [Autoregressive Models](https://outcomeschool.com/blog/autoregressive-models) that explains it in depth.

So, Top-k and Top-p Sampling are all about one question: from this list of probabilities, which token do we pick?

Let's see the simple approaches first, and then we will see why we need Top-k and Top-p.

## The problem with always picking the best token

The simplest approach is to always pick the token with the highest probability. This is called **Greedy Decoding**.

In our example, it will always pick "mat".

**Advantage:** It is simple and fast.

**Disadvantage:** The text becomes boring and repetitive. Ask the same question twice, and we get the exact same answer. Many times, the LLM gets stuck in a loop like "I think that I think that I think that".

And, the most likely token at every step does not always give the most natural sentence overall. We humans do not always use the most common word. A little variety makes the text feel natural.

The issue with this approach is that there is no variety at all. Let's see how the next approach solve this issue.

## The problem with picking from every token

The opposite approach is to pick randomly from every token in the vocabulary based on its probability. This is called **Pure Sampling**.

Picking randomly based on probability is like a lottery. Suppose we have a box with 100 tickets. "mat" gets 40 tickets, "floor" gets 25 tickets, "sofa" gets 15 tickets, "bed" gets 10 tickets, "roof" gets 5 tickets, and the remaining 5 tickets are shared by every other token. We close our eyes and pick one ticket. The token written on that ticket is our next token.

Means, "mat" gets picked 40% of the time, "floor" gets picked 25% of the time, and so on.

**Advantage:** The text has variety. Every reply is different.

**Disadvantage:** Remember that thousands of other tokens together share 5%. Each one of them has a very tiny probability. But there are so many of them that together, one of them gets picked 5% of the time.

So, the LLM writes "The cat sat on the banana" or "The cat sat on the democracy". This looks silly.

And, this is not a one-time problem. The LLM writes hundreds of tokens in a reply. If even one silly token gets picked, the LLM builds the rest of the sentence on top of that silly token, and the whole reply goes off track.

The issue with this approach is that we let the LLM pick from the bad tokens at the bottom of the list. We need a way to keep the variety but cut off the bad tokens.

So, here comes the Top-k Sampling to the rescue.

## What is Top-k Sampling?

**Top-k Sampling is a decoding strategy in which we keep only the k tokens with the highest probability, throw away all the others, and then pick randomly from those k tokens.**

Top-k = Top + k

- Top: the tokens with the highest probability
- k: how many of them we keep

In simple words, we cut the list down to a fixed size k, and we run our lottery only on that short list.

Let's say we go to a restaurant and ask the waiter to pick a dish for us. A greedy waiter always picks the number one dish, every single time. A pure sampling waiter picks from the whole menu, even the dishes that nobody orders. Top-k is like a waiter who looks only at the 3 most popular dishes and picks one of them. The dishes that nobody orders are never picked.

Here, k is a number that we choose. It is a setting, not something the LLM learns. Common values are between 10 and 50.

## Step-by-step example of Top-k Sampling

The best way to learn this is by taking an example.

Let's take our example "The cat sat on the" with k = 3.

**Step 1: Sort the tokens by probability, from highest to lowest.**

| Token | Probability |
| --- | --- |
| mat | 40% |
| floor | 25% |
| sofa | 15% |
| bed | 10% |
| roof | 5% |
| every other token | 5% in total |

**Step 2: Keep only the top k tokens.**

With k = 3, we keep "mat", "floor", and "sofa". Everything else is thrown away.

| Token | Probability |
| --- | --- |
| mat | 40% |
| floor | 25% |
| sofa | 15% |

**Step 3: Re-scale the probabilities so that they add up to 100% again.**

Now, the three tokens add up to only 80%. So, we take each one as a share of that 80%. This is called **renormalization**.

| Token | New Probability |
| --- | --- |
| mat | 40 / 80 = 50% |
| floor | 25 / 80 = 31.25% |
| sofa | 15 / 80 = 18.75% |

**Step 4: Pick one token randomly based on the new probabilities.**

So, "mat" gets picked half of the time, "floor" gets picked around one-third of the time, and "sofa" gets picked around one-fifth of the time.

"banana" and "democracy" can never be picked. Problem Solved!

Let's see the code for Top-k Sampling, as below:

```python
import torch
def top_k_sampling(logits, k):
    # keep only the k highest scores
    top_values, top_indices = torch.topk(logits, k)
    # convert the kept scores into probabilities
    probs = torch.softmax(top_values, dim=-1)
    # pick one token randomly based on the probabilities
    chosen = torch.multinomial(probs, num_samples=1)
    return top_indices[chosen]
```

Here, we have:

- `torch.topk` gives us the k highest scores and their positions in the vocabulary.
- `torch.softmax` converts those k scores into probabilities that add up to 100%. This does the renormalization for us.
- `torch.multinomial` runs the lottery and picks one token based on the probabilities.
- Finally, we return the position of the chosen token in the vocabulary.

**Note:** Here, we apply softmax only on the k kept scores instead of all the scores. This gives exactly the same result as applying softmax on all the scores and then re-scaling the top k. So, we get the renormalization for free.

This is how Top-k Sampling works.

## The problem with Top-k Sampling

Top-k Sampling works well in our example. But, here is the catch.

The value of k is fixed. It does not change based on the situation. And, the situation changes at every token.

Let's see two very different situations.

**Situation 1: The next token is obvious.**

Let's say the text is "The capital of France is". The LLM is very sure here.

| Token | Probability |
| --- | --- |
| Paris | 95% |
| the | 2% |
| a | 1% |
| located | 1% |
| every other token | 1% in total |

With k = 3, we keep "Paris", "the", and "a". But, "the" and "a" are weak choices here. We are forcing weak tokens into the list just because k says we need three. So, once in a while, the LLM writes "The capital of France is the", which is a poor start.

**Situation 2: The next token has many good options.**

Let's say the text is "My favourite colour is". Many answers are equally good.

| Token | Probability |
| --- | --- |
| blue | 12% |
| red | 11% |
| green | 11% |
| black | 10% |
| purple | 10% |
| yellow | 9% |
| white | 9% |
| pink | 8% |
| every other token | 20% in total |

With k = 3, we keep only "blue", "red", and "green". But, "black", "purple", and "yellow" are just as good. We are cutting off good tokens just because k says we can keep only three. So, the LLM never says "black", "purple", or "yellow", and its answers feel limited.

So, the same k = 3 is too many in Situation 1 and too few in Situation 2.

The issue with this approach is that a fixed number k cannot adapt to how confident the LLM is. Let's see how the next approach solve this issue.

Here comes the Top-p Sampling into the picture.

## What is Top-p Sampling?

**Top-p Sampling is a decoding strategy in which we keep the smallest group of top tokens whose probabilities add up to at least p, throw away all the others, and then pick randomly from that group.**

Top-p = Top + p

- Top: the tokens with the highest probability
- p: the total probability we want to cover

In simple words, instead of saying "keep 3 tokens", we say "keep enough tokens to cover 90% of the probability".

Top-p Sampling is also called **Nucleus Sampling**. Nucleus means the core or the center of something. The small group of tokens that we keep is the core of the list, hence the name. It was introduced in 2019 in a research paper named "The Curious Case of Neural Text Degeneration".

Let's go back to our restaurant. Top-p is like a waiter who looks at the dishes that together make up 90% of all the orders. On a day when almost everyone orders one dish, that is just one dish. On a day when the orders are spread out, that is many dishes. The waiter adapts to the day.

Here, p is a number between 0 and 1 that we choose. Common values are between 0.9 and 0.95.

The size of the group is not fixed anymore. It becomes small when the LLM is sure and big when the LLM is unsure. This is the key difference from Top-k.

## Step-by-step example of Top-p Sampling

Let's take our example "The cat sat on the" with p = 0.9, which means 90%.

**Step 1: Sort the tokens by probability, from highest to lowest.**

| Token | Probability |
| --- | --- |
| mat | 40% |
| floor | 25% |
| sofa | 15% |
| bed | 10% |
| roof | 5% |
| every other token | 5% in total |

**Step 2: Add the probabilities from the top, one by one, till the total reaches p.**

| Token | Probability | Running Total |
| --- | --- | --- |
| mat | 40% | 40% |
| floor | 25% | 65% |
| sofa | 15% | 80% |
| bed | 10% | 90% |

The total reaches 90% at "bed". So, we stop here.

**Step 3: Keep the tokens up to that point and throw away all the others.**

We keep "mat", "floor", "sofa", and "bed". "roof" and every other token is thrown away.

**Step 4: Re-scale the probabilities so that they add up to 100% again.**

The four tokens add up to 90%. So, we take each one as a share of that 90%.

| Token | New Probability |
| --- | --- |
| mat | 40 / 90 = 44.4% |
| floor | 25 / 90 = 27.8% |
| sofa | 15 / 90 = 16.7% |
| bed | 10 / 90 = 11.1% |

**Step 5: Pick one token randomly based on the new probabilities.**

This is how Top-p Sampling works.

Now, let's see how the same p = 0.9 handles the two situations where Top-k struggled.

**Situation 1: "The capital of France is"**

| Token | Probability | Running Total |
| --- | --- | --- |
| Paris | 95% | 95% |

"Paris" alone crosses 90%. So, we keep only "Paris". The weak tokens "the" and "a" are thrown away. The group has just one token.

**Situation 2: "My favourite colour is"**

| Token | Probability | Running Total |
| --- | --- | --- |
| blue | 12% | 12% |
| red | 11% | 23% |
| green | 11% | 34% |
| black | 10% | 44% |
| purple | 10% | 54% |
| yellow | 9% | 63% |
| white | 9% | 72% |
| pink | 8% | 80% |

These eight tokens reach only 80%. So, we keep going into the tokens below "pink" till the total reaches 90%. The group has many tokens. All the good colours stay in the list.

So, the same p = 0.9 gave one token in Situation 1 and many tokens in Situation 2. The group size adapted itself to how confident the LLM was. All problems got solved.

Let's see the code for Top-p Sampling, as below:

```python
import torch
def top_p_sampling(logits, p):
    # convert all the scores into probabilities
    probs = torch.softmax(logits, dim=-1)
    # sort from highest to lowest
    sorted_probs, sorted_indices = torch.sort(probs, descending=True)
    # running total of the probabilities
    cumulative = torch.cumsum(sorted_probs, dim=-1)
    # running total before this token
    before = cumulative - sorted_probs
    # if the total before this token already reached p, we do not need it
    sorted_probs[before >= p] = 0.0
    # re-scale so that the kept probabilities add up to 1
    sorted_probs = sorted_probs / sorted_probs.sum()
    # pick one token randomly based on the probabilities
    chosen = torch.multinomial(sorted_probs, num_samples=1)
    return sorted_indices[chosen]
```

Here, we have:

- `torch.softmax` converts all the scores into probabilities.
- `torch.sort` puts the probabilities in order from highest to lowest.
- `torch.cumsum` gives the running total, just like the "Running Total" column in our table.
- `before` is the running total without the current token. If that total has already reached p, then the current token is not needed, so we set its probability to zero. This keeps the token which makes the total reach p and removes everything after it.
- We divide by the sum to re-scale the kept probabilities. This is the renormalization.
- `torch.multinomial` runs the lottery and picks one token.
- Finally, we return the position of the chosen token in the vocabulary.

This was all about Top-p Sampling. Now, let's compare both of them.

## Top-k vs Top-p Sampling

Let me tabulate the differences between Top-k and Top-p Sampling for your better understanding so that you can decide which one to use based on your use case.

|  | Top-k Sampling | Top-p Sampling |
| --- | --- | --- |
| What we fix | The number of tokens to keep | The total probability to cover |
| Size of the kept group | Always exactly k | Changes at every token |
| When the LLM is very sure | Still keeps k tokens, some of them weak | Keeps very few tokens, sometimes just one |
| When the LLM is unsure | Still keeps only k tokens, cuts off good ones | Keeps many tokens |
| Other name | No other name | Nucleus Sampling |
| Common values | 10 to 50 | 0.9 to 0.95 |
| Work needed | Less, only find the top k | More, sort everything and keep a running total |

## How Top-k and Top-p work with Temperature

Many of you must be knowing about **[Temperature](https://outcomeschool.com/blog/how-does-temperature-control-llm-output)**. Temperature is another setting that controls how random the output of an LLM is.

Temperature divides all the scores by the temperature value before they are converted into probabilities. A low temperature like 0.2 makes the top token even more likely, so the probabilities become sharp. Means, one token stands out clearly. A high temperature like 1.5 brings all the tokens closer to each other, so the probabilities become flat. Means, many tokens look almost equally likely.

Top-k and Top-p do not change the shape of the probabilities. They only cut the list.

So, they do different jobs:

- Temperature decides how sharp or how flat the probabilities are.
- Top-k and Top-p decide how many tokens stay in the list.

Now, the question is: can we use all three together? Yes, we can. Inside the LLM, they are usually applied in the below order:

Scores -> Temperature -> Top-k -> Top-p -> Convert to probabilities -> Pick one token

First, temperature reshapes the scores. Then, Top-k cuts the list to k tokens. Then, Top-p cuts it further if needed. Finally, we run the lottery on whatever is left. Many tools set k = 50 and p = 0.95 by default.

When we call an LLM API, we pass these as settings named `top_k`, `top_p`, and `temperature` along with our prompt. We do not have to write the sampling code ourselves. The code we saw above is what runs behind these settings.

**Note:** If we set k to a very large number or p to 1.0, then that filter does nothing, and we get Pure Sampling back. If we set k = 1 or p very close to 0, then only the top token survives, and we get Greedy Decoding back. So, Greedy Decoding and Pure Sampling are just the two ends of the same idea. Top-k and Top-p let us pick any point in between.

## When to use which one

- For tasks where the answer must be correct, like answering a factual question, writing code, or summarizing a document, we want less randomness. Use a small k like 10, or a p like 0.9, along with a low temperature. The LLM must not take chances here.
- For creative tasks, like writing a story or a poem, we want more variety. Use a larger k like 50, or a p like 0.95, along with a slightly higher temperature.
- When we are not sure, Top-p is the safer default because it adapts itself at every token. This is why almost every LLM API exposes Top-p as a setting, while Top-k is not always available.

Now we must have understood how Top-k and Top-p Sampling work.

## Frequently Asked Questions

### Can we use Top-k and Top-p together?

Yes. Inside the LLM, they are usually applied in order: temperature reshapes the scores, Top-k cuts the list to k tokens, and then Top-p cuts it further if needed. Finally, one token is picked from whatever is left. Many tools set k = 50 and p = 0.95 by default.

### What happens if we set top\_p to 1.0?

The Top-p filter does nothing, and we get Pure Sampling back. The same happens when we set k to a very large number. On the other side, if we set k = 1 or p very close to 0, only the top token survives, and we get Greedy Decoding back.

### Is Top-p better than Top-k?

Top-p is the safer default when we are not sure, because it adapts itself at every token. It keeps very few tokens when the LLM is sure and many tokens when the LLM is unsure. This is why almost every LLM API exposes Top-p as a setting, while Top-k is not always available. Top-k does need less work, since it only finds the top k.

### Is Top-p the same as temperature?

No. Temperature decides how sharp or how flat the probabilities are by dividing the scores before they become probabilities. Top-k and Top-p do not change the shape of the probabilities. They only decide how many tokens stay in the list.

### Do we need to write Top-k or Top-p code when we use an LLM API?

No. When we call an LLM API, we pass settings named `top_k`, `top_p`, and `temperature` along with our prompt. The sampling code runs behind these settings, so we do not have to write it ourselves.
