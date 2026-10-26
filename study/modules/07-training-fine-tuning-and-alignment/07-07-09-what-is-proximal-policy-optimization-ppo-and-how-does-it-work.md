---
title: What is Proximal Policy Optimization (PPO) and How Does It Work?
module: 7
module_title: Training, Fine-Tuning, and Alignment
lesson: '7.9'
source: https://outcomeschool.com/blog/proximal-policy-optimization-ppo
published: May 16, 2026
tags:
- llm
- ai
- machine-learning
videos: []
fetched: '2026-10-24'
words: 2431
reading_time: 12
status: full
---
# What is Proximal Policy Optimization (PPO) and How Does It Work?

> **Module 7 · Lesson 7.9**  
> Source: [Outcome School](https://outcomeschool.com/blog/proximal-policy-optimization-ppo) · Published: May 16, 2026 · Reading time: ~12 min · Tags: `llm`, `ai`, `machine-learning`

---

![Proximal Policy Optimization (PPO)](../../assets/images/07-07-09-what-is-proximal-policy-optimization-ppo-and-how-does-it-work/proximal-policy-optimization-ppo.png)

Proximal Policy Optimization (PPO) is a reinforcement learning algorithm that improves the policy in small, safe steps, so that the new policy stays close to the old one. It is used to train Large Language Models with RLHF.

In this blog, we are going to learn about Proximal Policy Optimization (PPO). We will also see how PPO works step-by-step and how it is used in training Large Language Models with RLHF.

We will cover the following:

- What is Reinforcement Learning?
- What is a Policy?
- The problem with simple policy updates.
- What is Proximal Policy Optimization (PPO)?
- The key idea behind PPO: Clipping.
- The PPO objective function in simple words.
- How PPO works step-by-step.
- PPO in Large Language Models (RLHF).
- Advantages of PPO.
- Disadvantages of PPO.

Let's get started.

Before jumping into PPO, we must know a few basic concepts of [reinforcement learning](https://outcomeschool.com/blog/reinforcement-learning). Do not worry, we will learn about each of them in detail.

### What is Reinforcement Learning?

**Reinforcement Learning** is a way of teaching a model by giving it rewards for good actions and penalties for bad actions. The model learns by trial and error, and that too without being explicitly programmed.

Let's say we are teaching a dog a new trick. When the dog does the trick correctly, we give it a treat. When the dog does it wrong, we do not give a treat. Over time, the dog learns which actions lead to treats. This is exactly how reinforcement learning works.

In simple words, the model tries different actions, sees the rewards, and slowly learns which actions are better.

This was about Reinforcement Learning. Now, let's move to the next concept.

### What is a Policy?

A **policy** is the strategy that the model follows to decide what action to take in a given situation.

For the sake of understanding, let's take an example. Suppose we have a robot in a room. The room has many doors. The policy tells the robot which door to open in which situation. If the policy is good, the robot picks the right door. If the policy is bad, the robot picks the wrong door.

So, the goal of reinforcement learning is to find the best policy. The best policy gives the highest total reward over time.

Now that we have learned about a policy, it's time to learn about the problem we face while improving it.

### The Problem with Simple Policy Updates

Now, the question is: how do we improve the policy?

The simple idea is to update the policy in the direction that gives more reward. This is called **policy gradient**. We compute how the policy should change to get a higher reward, and then we apply that change.

But, here is the catch.

If we update the policy too much in one step, the new policy becomes very different from the old policy. The model suddenly behaves in a strange way. The training becomes unstable. Sometimes the model gets worse and never recovers.

If we update the policy too little, the training becomes very slow. The model takes forever to learn.

For the sake of understanding, let's take an example. Suppose we are learning to ride a bicycle. If we turn the handle too much, we fall. If we turn the handle too little, we cannot steer. We need to turn the handle by just the right amount. This is the same problem in policy updates.

So, we need a balance. We need to update the policy enough to make progress, but not so much that the training breaks.

What is the solution to this problem? Answer: **Proximal Policy Optimization (PPO)**.

So, here comes PPO to the rescue.

### What is Proximal Policy Optimization (PPO)?

**Proximal Policy Optimization** is a reinforcement learning algorithm that improves the policy in small, safe steps. It makes sure that the new policy stays close to the old policy.

Let's decompose the name:

**PPO = Proximal + Policy + Optimization**

- **Proximal** means close or nearby.
- **Policy** is the strategy the model follows.
- **Optimization** means making it better.

So, PPO is an algorithm that makes the policy better while keeping the new policy close to the old policy.

In simple words, PPO improves the model step by step, and each step is small and safe.

### The Key Idea Behind PPO: Clipping

The key idea behind PPO is **clipping**.

In simple words, clipping means cutting off the extreme values. If a value tries to go too high or too low, we cut it down to a safe range.

Let's say we have an old policy and a new policy. We measure how much the new policy differs from the old policy by computing a **ratio**.

- If the ratio is 1, the new policy is the same as the old policy.
- If the ratio is greater than 1, the new policy is more likely to take this action.
- If the ratio is less than 1, the new policy is less likely to take this action.

Now, PPO says: if this ratio goes too far from 1, we will clip it. We will not allow the update to push the policy too far.

In practice, PPO uses a small number called **epsilon**, which is usually 0.2. This means the ratio is allowed to stay between 0.8 and 1.2. If the ratio tries to go above 1.2 or below 0.8, PPO clips it.

Let's understand this with a simple number example. Suppose the new policy wants to take an action 3 times more than the old policy. Means, the ratio is 3. This is too far from 1. PPO will clip this ratio down to 1.2. So, the policy update is limited to a small change, even when the data wants to push it further.

This is how PPO keeps the new policy close to the old policy.

### The PPO Objective Function in Simple Words

The PPO objective function looks complex in math, but the idea is simple. Let's understand it in plain words.

The objective function is as below:

```
L = min( ratio * advantage, clipped_ratio * advantage )
```

Here, we have used the following:

- `ratio` is how much the new policy differs from the old policy.
- `advantage` tells us how much better or worse the action was compared to what was expected. The expected value comes from a separate **value model** that we train alongside the policy. A positive advantage means the action was better than expected, and a negative advantage means it was worse.
- `clipped_ratio` is the ratio clipped to stay between `1 - epsilon` and `1 + epsilon`.
- `min` means we take the smaller of the two values.

In simple words, PPO says: take the smaller value between the normal update and the clipped update. This makes sure that the policy does not change too much in one step.

Let's see a quick example. Suppose the advantage is positive, which means the action was good. The normal update would multiply the ratio by the advantage. If the ratio is very high, the policy would jump too much. The clipped value becomes the smaller one, and PPO uses that. The policy moves in the right direction, but in a small step.

**Note:** The `min` operation is what makes PPO safe. It prevents the policy from making large jumps even if the data suggests a big change.

### How PPO Works Step-by-Step

Now, let's see how PPO works step-by-step.

**Step 1:** Start with an initial policy. This is our old policy.

**Step 2:** Let the model interact with the environment using the old policy. Collect data about the actions taken and the rewards received.

**Step 3:** Compute the advantage for each action using the value model. The advantage tells us how much better or worse each action was compared to what the value model expected.

**Step 4:** Update the policy using the PPO objective function. The clipping makes sure the new policy stays close to the old policy.

**Step 5:** Repeat the same data multiple times to make full use of it. PPO can use the same data for many small updates, which makes it efficient.

**Step 6:** Replace the old policy with the new policy. Go back to Step 2 and repeat.

This is how PPO improves the policy step by step in a safe and stable way. The problem of unstable updates is solved.

### PPO in Large Language Models (RLHF)

Now, let's take a real use case. PPO is famously used in training Large Language Models like ChatGPT. This process is called **[Reinforcement Learning from Human Feedback (RLHF)](https://outcomeschool.com/blog/reinforcement-learning-from-human-feedback-rlhf)**.

The paper that made this pipeline famous is OpenAI's InstructGPT. We have a detailed blog on [Decoding InstructGPT](https://outcomeschool.com/blog/decoding-instructgpt) that explains all three of its steps in depth.

Let me explain how this works.

First, we have a Large Language Model that has been trained on a lot of text. This model can generate responses, but the responses are not always helpful or safe.

Then, humans rank different responses from the model. For example, for the same question, humans say which response is better.

After that, a **reward model** is trained on these human rankings. This idea of [learning a reward from human comparisons](https://outcomeschool.com/blog/decoding-deep-rl-from-human-preferences) goes back to a 2017 paper on games and robots. The reward model can give a score to any response. The higher the score, the better the response.

Once we've done that, PPO is used to update the Language Model. Here, the Language Model is the policy. The Language Model generates responses, the reward model scores them, and PPO updates the Language Model to generate higher-scoring responses.

Along with the policy, PPO also trains a **value model**, also called the **critic**. The value model predicts how good a response is expected to be before we see the actual reward. PPO uses the difference between the actual reward from the reward model and the value model's prediction to compute the **advantage**. The advantage tells us how much better or worse the response was compared to what was expected. This advantage is what PPO uses inside the clipped objective to update the policy.

So, in RLHF with PPO, we have four models working together. The policy model is the Language Model being trained. The value model predicts expected rewards. The reward model scores responses based on human preferences. The reference model is a frozen copy of the original Language Model.

We have a detailed blog on [Direct Preference Optimization (DPO)](https://outcomeschool.com/blog/direct-preference-optimization-dpo) that explains a simpler alternative for LLM alignment which avoids PPO and the reward model entirely.

Here is the important part. The updated Language Model must not become very different from the original Language Model. This is very important. If we update the model too much, it can start writing strange text or forget its language skills. Two things keep the model safe. First, PPO's clipping prevents large policy changes in any single update. Second, in RLHF we keep a frozen copy of the original model called the **reference model**. A **KL penalty** is added to the reward, which grows when the new model drifts away from the reference model. This pulls the new model back toward what it already knew.

That's the beauty of PPO. It improves the model while protecting what the model already knows.

This is how PPO helps in training models like ChatGPT to be more helpful and aligned with human preferences.

### Advantages of PPO

- **Stable training.** PPO does not make big jumps in policy updates. The training is smooth and reliable.
- **Simple to implement.** Compared to other advanced reinforcement learning methods, PPO is easier to code and understand.
- **Sample efficient.** PPO can use the same collected data for multiple updates, which saves time and computation.
- **Works well in many domains.** PPO has been used in robotics, games, and language models.
- **Widely adopted.** PPO is one of the most popular reinforcement learning algorithms in the industry.

### Disadvantages of PPO

- **Hyperparameter sensitive.** The value of epsilon and other settings can affect performance.
- **Needs a value model.** PPO trains a separate value model to estimate the advantage at each step. The value model is almost the same size as the policy, which adds significant memory and compute cost.
- **Slower than some newer methods.** Methods like [GRPO](https://outcomeschool.com/blog/group-relative-policy-optimization-grpo) are designed to be more efficient for specific tasks like training Language Models.
- **Can still be unstable in some cases.** Even with clipping, training can fail if the reward signal is noisy.

### Conclusion

Now, we have understood Proximal Policy Optimization.

PPO is a reinforcement learning algorithm that improves the policy in small, safe steps. The key idea is clipping, which keeps the new policy close to the old policy. This makes the training stable and reliable.

PPO is used in many areas, including training Large Language Models like ChatGPT through RLHF. Hence, it is one of the most important algorithms in modern AI.

## Frequently Asked Questions

### What value of epsilon does PPO usually use?

PPO usually uses an epsilon of 0.2. This means the ratio between the new policy and the old policy is allowed to stay between 0.8 and 1.2. If the ratio tries to go above 1.2 or below 0.8, PPO clips it, so the policy update stays small.

### How many models are used in RLHF with PPO?

Four models work together. The policy model is the Language Model being trained. The value model predicts expected rewards. The reward model scores responses based on human preferences. The reference model is a frozen copy of the original Language Model.

### Is clipping the only thing that keeps an LLM close to the original model in RLHF?

No. Clipping prevents large policy changes in any single update. On top of that, RLHF keeps a frozen reference model and adds a KL penalty to the reward, which grows when the new model drifts away from the reference model. This pulls the new model back toward what it already knew.

### Can PPO reuse the same data for more than one update?

Yes. PPO can use the same collected data for many small updates, which makes it sample efficient. This saves time and computation.

### Is PPO the only way to align a Large Language Model?

No. Direct Preference Optimization (DPO) is a simpler alternative for LLM alignment that avoids PPO and the reward model entirely. Methods like GRPO are also designed to be more efficient than PPO for specific tasks like training Language Models.
