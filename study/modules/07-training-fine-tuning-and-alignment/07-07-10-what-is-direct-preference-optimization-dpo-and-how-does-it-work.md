---
title: What is Direct Preference Optimization (DPO) and How Does It Work?
module: 7
module_title: Training, Fine-Tuning, and Alignment
lesson: '7.10'
source: https://outcomeschool.com/blog/direct-preference-optimization-dpo
published: May 17, 2026
tags:
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 2708
reading_time: 14
status: full
---
# What is Direct Preference Optimization (DPO) and How Does It Work?

> **Module 7 · Lesson 7.10**  
> Source: [Outcome School](https://outcomeschool.com/blog/direct-preference-optimization-dpo) · Published: May 17, 2026 · Reading time: ~14 min · Tags: `llm`, `ai`, `machine-learning`

---

![Direct Preference Optimization (DPO)](../../assets/images/07-07-10-what-is-direct-preference-optimization-dpo-and-how-does-it-work/direct-preference-optimization-dpo.png)

Direct Preference Optimization (DPO) is a method to train a Large Language Model directly on human preference data, without using a separate reward model and without using reinforcement learning.

In this blog, we are going to learn about Direct Preference Optimization (DPO). We will also see how DPO works step-by-step and how it differs from RLHF (PPO).

We will cover the following:

- What is RLHF and why do we need it?
- The problem with RLHF.
- What is Direct Preference Optimization (DPO)?
- What is preference data?
- The key idea behind DPO.
- The DPO loss function in simple words.
- How DPO works step-by-step.
- DPO vs RLHF (PPO).
- Advantages of DPO.
- Disadvantages of DPO.

Let's get started.

Before jumping into DPO, we must know a few basic concepts. Do not worry, we will learn about each of them in detail.

### What is RLHF and Why Do We Need It?

**RLHF** stands for **[Reinforcement Learning from Human Feedback](https://outcomeschool.com/blog/reinforcement-learning-from-human-feedback-rlhf)**. It is a way of training a Large Language Model so that its responses match what humans actually prefer.

Let's say we have a Large Language Model that has already been trained on a huge amount of text. The model can generate responses to any question. But, here is the catch. The responses are not always helpful, safe, or in the tone that humans like.

Let's take an example. Suppose we ask the model: "How do I learn to code?" The model can give a very long, dry, and academic answer. But humans prefer a short, friendly, and step-by-step answer.

So, we need a way to teach the model what humans prefer. This is where RLHF comes into the picture.

In RLHF, humans look at different responses from the model and rank them. Then, a separate model called the **reward model** is trained on these rankings. After that, an algorithm like **[PPO (Proximal Policy Optimization)](https://outcomeschool.com/blog/proximal-policy-optimization-ppo)** is used to update the Language Model so that it generates higher-scoring responses. During this update, we also keep a frozen copy of the original Language Model. This frozen copy is called the **reference model**, and it acts as a safety anchor so that the new model does not drift too far from what it already knew.

This full recipe comes from OpenAI's InstructGPT paper, which itself built on the 2017 [Deep RL from Human Preferences](https://outcomeschool.com/blog/decoding-deep-rl-from-human-preferences) paper. We have a detailed blog on [Decoding InstructGPT](https://outcomeschool.com/blog/decoding-instructgpt) that covers that pipeline end to end.

This was about RLHF. Now, let's see the problem with this approach.

### The Problem with RLHF

RLHF works, but it is complex. Let's see why.

First, we need to train a separate reward model. This reward model is another neural network that we must train, save, and run during training.

Then, we need to run a [reinforcement learning](https://outcomeschool.com/blog/reinforcement-learning) algorithm like PPO. PPO is not easy to use. It needs careful tuning. The training can become unstable. The model can also start generating strange text if the reward model is not perfect.

On top of this, PPO also needs a **value model**, also called the **critic**. The value model predicts the expected reward at every step and helps PPO compute the advantage. The value model is almost the same size as the Language Model, so we are training two very large models at the same time. This makes the whole pipeline even more expensive.

So, the full RLHF pipeline has many moving parts: the base model, the reward model, the reference model, the value model, and the PPO algorithm. Each part can fail. Each part needs careful tuning. And that too, the whole process is slow and expensive.

For the sake of example, suppose we are trying to bake a cake. RLHF is like baking a cake using ten different machines, each with its own temperature setting. If any one machine fails, the whole cake is ruined. We need a simpler way.

What is the solution to this problem? Answer: **Direct Preference Optimization (DPO)**.

So, here comes DPO to the rescue.

### What is Direct Preference Optimization (DPO)?

**Direct Preference Optimization** is a method to train a Large Language Model directly on human preference data, without using a separate reward model and without using reinforcement learning.

Let's decompose the name:

**DPO = Direct + Preference + Optimization**

- **Direct** means we go straight to training the model on preferences. No reward model in between.
- **Preference** is the human choice between two responses, telling us which one is better.
- **Optimization** means making the model better.

So, DPO is a method that makes the Language Model better by directly using human preferences, without any extra steps.

In simple words, DPO replaces the whole complex RLHF pipeline with a single, simple training step. It is like baking the cake using just one oven. It makes our life easy.

### What is Preference Data?

Before we go deeper, we must understand what preference data is.

**Preference data** is a collection of examples, where each example has three parts:

- A **prompt**, i.e., the question or instruction.
- A **chosen response**, i.e., the response that humans preferred.
- A **rejected response**, i.e., the response that humans did not prefer.

Let's see an example.

```
Prompt: How do I learn to code?
Chosen response: Start with one language like Python. Build small projects every day. Slowly take on bigger challenges. Stay consistent.
Rejected response: Coding is a vast field with many languages, frameworks, paradigms, and tools that one must learn over years of dedicated study.
```

Here, we can see that humans preferred the chosen response because it is short, friendly, and gives clear steps. The rejected response is too academic and not very helpful.

This is the kind of data that DPO uses. We give DPO many such pairs, and DPO teaches the model to generate responses that look like the chosen ones and not like the rejected ones.

Now that we have understood preference data, it's time to learn about the key idea behind DPO.

### The Key Idea Behind DPO

The key idea behind DPO is very clever.

In RLHF, we first train a reward model. The reward model gives a score to any response. Then, we use this score to train the Language Model.

The authors of DPO noticed something important. They noticed that the Language Model itself can act as its own reward model. We do not need a separate reward model at all.

In simple words, the probabilities that the Language Model gives to different responses already tell us how much the model prefers each response. If we use these probabilities in a clever way, we can train the model directly on the preference data.

So, DPO removes the reward model from the picture. The model is its own reward model. The training becomes a single step.

Let's take an example. Imagine asking a chef to make better dishes. With RLHF, we first hire a food critic, train the critic to score dishes, and then ask the chef to cook based on the critic's scores. With DPO, we directly tell the chef: this dish is better, this one is worse, learn from these examples. There is no food critic in between. The chef learns directly from the comparison.

Now, let's see how this works for our Language Model. Suppose we have a Language Model. For a given prompt, it assigns a higher probability to the rejected response than to the chosen response. This means the model prefers the rejected response, which is wrong. DPO will update the model so that the probability of the chosen response goes up and the probability of the rejected response goes down. After training, the model assigns a higher probability to the chosen response. Means, the model now agrees with human preferences.

This way, DPO turns the complex reinforcement learning problem into a simple [supervised learning](https://outcomeschool.com/blog/supervised-vs-unsupervised-learning) problem. The problem is solved.

### The DPO Loss Function in Simple Words

The DPO loss function looks scary in math, but the idea is simple. Let's understand it in plain words.

The DPO loss is as below:

```
Loss = -log( sigmoid( beta * ( log_ratio_chosen - log_ratio_rejected ) ) )
```

Here, we have used the following:

- `log_ratio_chosen` is the log of the ratio of the new model's probability to the reference model's probability for the chosen response.
- `log_ratio_rejected` is the log of the ratio of the new model's probability to the reference model's probability for the rejected response.
- `beta` is a small number that controls how much we are allowed to move away from the reference model. A common value is 0.1.
- `sigmoid` is a function that squashes any number into a value between 0 and 1.
- The reference model is the original model before training. We keep a frozen copy of it.

In simple words, DPO says the following.

We want the new model to give a higher probability to the chosen response than to the rejected response. At the same time, we do not want the new model to move too far away from the reference model. The `beta` controls this balance.

If `beta` is small, the new model is allowed to change a lot. If `beta` is large, the new model is forced to stay close to the reference model.

**Note:** The reference model is the safety anchor. It plays a similar role to the reference model used in RLHF with PPO. The new model is not allowed to drift too far from it and forget what it already knows.

For the sake of understanding, let's see what this loss does in practice. If the new model already strongly prefers the chosen response over the rejected response, the value inside `sigmoid` becomes large, `sigmoid` becomes close to 1, and the loss becomes close to 0. Means, the model is doing the right thing, so there is nothing to learn. But if the new model prefers the rejected response over the chosen response, the value inside `sigmoid` becomes negative, `sigmoid` becomes small, and the loss becomes large. The model then updates itself to fix this.

This is how DPO trains the model. It is just one loss function, and we minimize it like any normal supervised learning task.

### How DPO Works Step-by-Step

Now, let's see how DPO works step-by-step.

**Step 1:** Start with a pretrained Language Model. This model has usually been [fine-tuned](https://outcomeschool.com/blog/how-does-fine-tuning-work) on instructions also. We also keep a frozen copy of this model. This frozen copy is called the **reference model**.

**Step 2:** Collect preference data. Each example has a prompt, a chosen response, and a rejected response.

**Step 3:** For each example, compute the probabilities of the chosen response and the rejected response. Compute these probabilities using both the new model and the reference model.

**Step 4:** Use the DPO loss function to compute the loss. The loss is high when the new model does not prefer the chosen response enough over the rejected response, compared to the reference model.

**Step 5:** Update the new model by minimizing the loss. This is the same as any normal training step using [gradient descent](https://outcomeschool.com/blog/math-behind-gradient-descent), just like how we train any other neural network.

**Step 6:** Repeat Steps 3 to 5 for many examples and many epochs.

Once we've done that, the model is trained to follow human preferences. No reward model. No reinforcement learning. Just one simple training loop.

That's the beauty of DPO. It takes a problem that used to need a full reinforcement learning setup and solves it with a single loss function.

This is how DPO improves the model in a very simple way.

### DPO vs RLHF (PPO)

Now that we have learned about DPO, it's time to compare it with the RLHF approach.

Let me tabulate the differences between DPO and RLHF (PPO) for your better understanding.

| Aspect | DPO | RLHF (PPO) |
| --- | --- | --- |
| Reward model | Not needed | Needed |
| Value model (critic) | Not needed | Needed |
| Algorithm | Supervised learning | Reinforcement learning |
| Training stability | Stable | Can be unstable |
| Implementation | Simple | Complex |
| Compute cost | Lower | Higher |
| Hyperparameter tuning | Easy | Hard |
| Memory usage | Lower | Higher |
| Performance | Competitive in many cases | Strong, but harder to achieve |

In simple words, DPO is simpler, faster, and more stable. RLHF can sometimes give better results, but it needs much more effort.

Based on our use case, if we want a simple and reliable way to train on preferences, DPO is the better choice. If we have the resources and need the absolute best performance on complex tasks, RLHF is still useful in certain settings.

Both methods have their place. But DPO has become very popular because of its simplicity.

### Advantages of DPO

- **No reward model.** We do not need to train a separate reward model. This saves time, compute, and memory.
- **No reinforcement learning.** DPO uses simple supervised learning. We do not need to deal with the complexity of PPO.
- **Stable training.** Since there is no reinforcement learning, the training is much more stable.
- **Simple to implement.** The DPO loss function can be implemented in a few lines of code.
- **Lower compute cost.** DPO needs less memory and less computation than RLHF.
- **Competitive performance.** In many cases, DPO matches or beats RLHF in terms of final model quality.

### Disadvantages of DPO

- **Needs paired data.** DPO needs preference pairs (chosen and rejected). Collecting this data still requires human effort.
- **Limited by data quality.** If the preference data is noisy, the model can learn the wrong preferences.
- **Hyperparameter sensitive.** The value of `beta` affects performance and must be tuned carefully.
- **Can overfit.** Since DPO is supervised learning, it can overfit to the preference data, especially with small datasets.
- **Less exploration.** DPO does not explore new responses like reinforcement learning does. It only learns from the data we give it.
- **Needs a good starting model.** DPO works best when the model has already been fine-tuned on instructions. If the starting model is weak, DPO cannot fully fix it.

### Conclusion

Now, we have understood Direct Preference Optimization.

DPO is a simple and powerful method to train Large Language Models on human preferences. It removes the need for a separate reward model and reinforcement learning. The Language Model itself acts as its own reward model. The training becomes a single supervised learning step.

DPO has made it much easier to align Language Models with human preferences. Hence, it is one of the most important developments in modern AI training. Many state-of-the-art open-source Language Models today use DPO as part of their training.

## Frequently Asked Questions

### Does DPO remove the need for human preference data?

No. DPO removes the reward model and reinforcement learning, but it still needs preference pairs. Each example has a prompt, a chosen response, and a rejected response. Collecting this data still requires human effort, and if the data is noisy, the model can learn the wrong preferences.

### Why does DPO need a reference model?

The reference model is the safety anchor. It is a frozen copy of the original model, and it stops the new model from drifting too far and forgetting what it already knows. DPO compares the new model's probabilities against the reference model's probabilities for both the chosen and rejected responses.

### What value of beta should we use in DPO?

A common value of `beta` is 0.1. If `beta` is small, the new model is allowed to change a lot. If `beta` is large, the new model is forced to stay close to the reference model. Since `beta` affects performance, it must be tuned carefully.

### Can we apply DPO to a base model that is not instruction-tuned?

We can, but DPO works best when the model has already been fine-tuned on instructions. If the starting model is weak, DPO cannot fully fix it. DPO only learns from the preference data we give it, and it does not explore new responses like reinforcement learning does.

### Is DPO used to train real language models?

Yes. Many state-of-the-art open-source Language Models today use DPO as part of their training. It became very popular because of its simplicity. It replaces the complex RLHF pipeline with a single loss function that we minimize like any normal supervised learning task.
