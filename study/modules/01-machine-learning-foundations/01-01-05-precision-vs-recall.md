---
title: Precision vs Recall
module: 1
module_title: Machine Learning Foundations
lesson: '1.5'
source: https://outcomeschool.com/blog/precision-vs-recall
published: August 1, 2026
tags:
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 1949
reading_time: 10
status: full
---
# Precision vs Recall

> **Module 1 · Lesson 1.5**  
> Source: [Outcome School](https://outcomeschool.com/blog/precision-vs-recall) · Published: August 1, 2026 · Reading time: ~10 min · Tags: `ai`, `machine-learning`

---

![Precision vs Recall](../../assets/images/01-01-05-precision-vs-recall/precision-vs-recall.png)

Precision tells us how many of the items we flagged were actually correct, whereas Recall tells us how many of all the real items we actually managed to catch.

In this blog, we will learn about Precision vs Recall, the two numbers we use to measure how good a system is at making yes-or-no decisions. We will also see how Precision and Recall differ from each other and when to use which one, what the four possible outcomes of any such decision are, why these two numbers pull against each other, and how the cost of a mistake decides which one we must care about more.

We will cover the following:

- The problem we are trying to solve
- The four possible outcomes
- What is Precision?
- What is Recall?
- Precision vs Recall
- When to use which one?
- A quick recap of the formulas
- Summary

Let's get started.

## The problem we are trying to solve

Before jumping into Precision and Recall, we must understand where they are used.

Let's say we have built a system that answers a simple yes-or-no question. For example, a spam filter that looks at an email and decides, "Is this email spam or not?"

A yes-or-no system like this is a classification model, and classification comes under supervised learning. We have a detailed blog on [Supervised vs Unsupervised Learning](https://outcomeschool.com/blog/supervised-vs-unsupervised-learning) that explains this in depth.

Now, our system will make some correct decisions and some wrong decisions. We need a way to measure how good our system really is. Just saying "it works fine" is not enough. We need proper numbers.

This is where Precision and Recall come into the picture. They are two numbers that tell us how good our system is, but they measure two different things.

The best way to learn this is by taking an example. So, for this whole blog, we will use one simple example: a spam filter that flags spam emails.

## The four possible outcomes

Before we understand Precision and Recall, we must first understand the four outcomes. Every decision our spam filter makes falls into one of four boxes.

Let's say an email comes in. There are two truths: the email is really spam, or it is really not spam. And there are two decisions: our filter flags it as spam, or it does not. When we mix these, we get four outcomes.

- **True Positive:** The email was really spam, and our filter correctly flagged it as spam. This is a correct catch.
- **False Positive:** The email was not spam, but our filter wrongly flagged it as spam. This is a false alarm. A real email got sent to the spam folder.
- **False Negative:** The email was really spam, but our filter missed it and let it into the inbox. This is a miss.
- **True Negative:** The email was not spam, and our filter correctly let it into the inbox. This is a correct pass.

Let's understand these four boxes with a simple table like below:

```
                         Really Spam         Really Not Spam
                   +---------------------+---------------------+
   Flagged as      |   True Positive     |   False Positive    |
   spam            |   (correct catch)   |   (false alarm)     |
                   +---------------------+---------------------+
   Not flagged     |   False Negative    |   True Negative     |
   as spam         |   (missed spam)     |   (correct pass)    |
                   +---------------------+---------------------+
```

Here, we can see all four outcomes clearly. The True Positive and the True Negative boxes are the correct decisions. The False Positive and the False Negative boxes are the mistakes.

Now that we know these four boxes, understanding Precision and Recall becomes very easy. Let's start with Precision.

## What is Precision?

**Precision answers this question: Out of all the emails we flagged as spam, how many were actually spam?**

In simple words, Precision checks how often our filter was correct when it raised an alarm. It looks only at the emails we flagged, and it asks how many of those were truly spam.

Let's say our filter flagged 10 emails as spam. Out of these 10, only 8 were really spam, and 2 were actually good emails. So, our Precision is 8 out of 10, which is 80%.

The formula is simple:

```
                       True Positive
   Precision = ------------------------------
               True Positive + False Positive
```

Here, we can see that Precision only cares about the emails we flagged. The bottom part of the formula is all the flagged emails (correct catches plus false alarms). The top part is only the correct catches.

So, high Precision means that when our filter says "this is spam", we can trust it. Very few good emails get wrongly flagged.

**When Precision is low:** It means our filter is flagging too many good emails as spam. This is annoying, because an important email can get lost in the spam folder.

## What is Recall?

Now that we have learned about Precision, it's time to learn about Recall.

**Recall answers this question: Out of all the emails that were really spam, how many did we actually catch?**

In simple words, Recall checks how many of the real spam emails our filter managed to find. It looks at all the true spam that exists, and it asks how much of it we caught.

Let's say there were 20 real spam emails in total. Our filter caught 8 of them and missed 12. So, our Recall is 8 out of 20, which is 40%.

The formula is simple:

```
                    True Positive
   Recall = ------------------------------
            True Positive + False Negative
```

Here, we can see that Recall cares about all the real spam. The bottom part of the formula is all the actual spam emails (the ones we caught plus the ones we missed). The top part is only the ones we caught.

So, high Recall means our filter catches most of the spam. Very little spam slips into the inbox.

**When Recall is low:** It means a lot of spam is getting past our filter and landing in the inbox. Our filter is missing too much.

## Precision vs Recall

Now, here is the most interesting part. Precision and Recall usually pull against each other. When we try to increase one, the other often goes down. It is like a tug of war.

Let's understand why.

Suppose we make our filter very strict, so it flags an email as spam only when it is 100% sure. Now it will rarely make a false alarm. So, our Precision goes up. But because it is so strict, it will also miss many spam emails that it was not fully sure about. So, our Recall goes down.

Now, suppose we make our filter very relaxed, so it flags an email as spam even on a small doubt. Now it will catch almost all the spam. So, our Recall goes up. But it will also wrongly flag many good emails. So, our Precision goes down.

We can picture this tug of war like below:

```
   Very strict filter                     Very relaxed filter
   Flags only when 100% sure              Flags on any small doubt
          |                                        |
          v                                        v
   Precision goes UP                       Recall goes UP
   Recall goes DOWN                        Precision goes DOWN
```

Here, we can clearly see the trade-off. We usually cannot get both very high at the same time. So, we must decide which one matters more for our problem.

Let me tabulate the differences between Precision and Recall for your better understanding.

| Point | Precision | Recall |
| --- | --- | --- |
| Main question | Of the ones we flagged, how many were correct? | Of all the real ones, how many did we catch? |
| Focus | Being correct when we raise an alarm | Not missing the real ones |
| Formula bottom | True Positive + False Positive | True Positive + False Negative |
| Low value means | Too many false alarms | Too many misses |
| We care about | Avoiding false alarms | Avoiding misses |

## When to use which one?

This is the real question. Whether we care more about Precision or more about Recall depends on the cost of the mistake. Let's understand with two examples.

**When Precision matters more:** Think about our spam filter. Here, wrongly flagging a good email as spam is very costly. An important message from our boss or bank can get lost in the spam folder. So, we want to be very sure before flagging. Here, we care more about Precision. A false alarm is worse than a small miss.

**When Recall matters more:** Now, think about a medical test that checks for a serious disease. Here, missing a sick patient is very dangerous. If we tell a sick person they are healthy, they will not get treatment, and that can cost a life. So, we want to catch every possible case, even if it means a few false alarms. Here, we care more about Recall. A miss is far worse than a false alarm.

So, the rule is simple:

- If a false alarm is costly, we care more about Precision.
- If a miss is costly, we care more about Recall.

The same two numbers are how we measure modern AI systems as well. A RAG pipeline, for example, is scored on Context Precision and Context Recall in exactly this way. We have a detailed blog on [LLM Evaluation](https://outcomeschool.com/blog/llm-evaluation) that covers this end to end.

**Note:** Sometimes we want a good balance of both. In that case, we use a single combined score called the F1 Score, which mixes Precision and Recall into one number. We can explore that in another blog.

## A quick recap of the formulas

Let's keep both formulas together so that we never forget them.

```
                       True Positive
   Precision = ------------------------------
               True Positive + False Positive
                    True Positive
   Recall = ------------------------------
            True Positive + False Negative
```

Here, we can notice one thing. Both formulas have True Positive on the top. The only difference is the bottom part. Precision adds False Positive, and Recall adds False Negative.

## Summary

Let's quickly recap what we have learned.

- Every yes-or-no decision falls into four boxes: True Positive, False Positive, False Negative, and True Negative.
- Precision asks: of all the ones we flagged, how many were correct?
- Recall asks: of all the real ones, how many did we catch?
- Precision and Recall usually pull against each other, like a tug of war.
- We care more about Precision when a false alarm is costly.
- We care more about Recall when a miss is costly.

This is how Precision and Recall help us measure our system in two different ways.

Now, we must have understood Precision vs Recall.

## Frequently Asked Questions

### Can a model have both high Precision and high Recall?

Usually not at the same time. Precision and Recall pull against each other like a tug of war. A very strict filter raises Precision but lowers Recall, while a very relaxed filter raises Recall but lowers Precision. So, we must decide which one matters more for our problem.

### What should we use when we want a balance of Precision and Recall?

We use the F1 Score. It is a single combined score that mixes Precision and Recall into one number. It is useful when we do not want to favor one over the other and need a good balance of both.

### Do Precision and Recall use True Negatives?

No. Neither formula includes True Negatives. Both formulas have True Positive on the top. The only difference is the bottom part, where Precision adds False Positive and Recall adds False Negative.

### Why does Recall matter more for a medical test?

Recall matters more because missing a sick patient is very dangerous. If we tell a sick person they are healthy, they will not get treatment. So, we want to catch every possible case, even if it means a few false alarms.

### Are Precision and Recall used to evaluate RAG pipelines?

Yes. The same two ideas are used to measure modern AI systems. A RAG pipeline, for example, is scored on Context Precision and Context Recall in exactly the same way.
