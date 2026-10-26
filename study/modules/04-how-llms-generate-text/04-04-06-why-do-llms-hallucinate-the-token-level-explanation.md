---
title: Why Do LLMs Hallucinate? The Token-Level Explanation
module: 4
module_title: How LLMs Generate Text
lesson: '4.6'
source: https://outcomeschool.com/blog/why-do-llms-hallucinate-the-token-level-explanation
published: October 14, 2026
tags:
- llm
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 3697
reading_time: 18
status: full
---
# Why Do LLMs Hallucinate? The Token-Level Explanation

> **Module 4 · Lesson 4.6**  
> Source: [Outcome School](https://outcomeschool.com/blog/why-do-llms-hallucinate-the-token-level-explanation) · Published: October 14, 2026 · Reading time: ~18 min · Tags: `llm`, `ai`, `system-design`

---

![Why Do LLMs Hallucinate? The Token-Level Explanation](../../assets/images/04-04-06-why-do-llms-hallucinate-the-token-level-explanation/why-do-llms-hallucinate-the-token-level-explanation.png)

LLMs hallucinate because they write an answer one token, a small piece of text, at a time by picking a likely next token, and when they do not know the right token, they still have to pick one, so a confident-looking guess comes out.

In this blog, we will learn about why LLMs hallucinate, explained at the level of tokens. We will also see what a token is, how an LLM picks the next token, how a sharp guess differs from a flat guess, why the model can never skip a token or take one back, how one wrong token leads to a full wrong answer, and how we can reduce hallucinations in the real world.

We will cover the following:

- What is a hallucination?
- What is a token?
- How does an LLM pick the next token?
- Easy tokens and fact tokens
- When the model knows: a sharp guess
- When the model does not know: a flat guess
- Picking a token in code
- Reason 1: There is no "skip" option
- Reason 2: Randomness picks a token from the flat guess
- Reason 3: A token cannot be taken back
- Reason 4: One wrong token leads to more wrong tokens
- Reason 5: Likely tokens can combine into something that does not exist
- Reason 6: The final text hides the uncertainty
- How can we reduce hallucinations at the token level?

Let's get started.

## What is a hallucination?

**A hallucination is when an AI gives an answer that sounds correct and confident, but is actually wrong or made up.**

The AI is not lying on purpose. It just produces something that looks like a real answer, and that too with full confidence.

In this blog, AI means an LLM (Large Language Model).

Let's say we ask an AI: "In which year was the author Meera Joshi born?"

For the sake of example, assume that Meera Joshi is a little-known author, and the AI has never read anything about her. A careful human would say "I do not know." But the AI replies: "Meera Joshi was born in 1962."

The sentence sounds confident, but the year is a guess. This is a hallucination.

We will look at the exact moment, one token at a time, where the wrong answer is generated. For that, we must first understand what a token is.

## What is a token?

**A token is a small piece of text that an LLM reads and writes.**

An LLM does not see full words the way we do. It breaks text into small pieces. A token can be a full word, a part of a word, a number, or even a space with a word.

Let's see how our sentence can be broken into tokens, just for the sake of understanding:

```
"Meera Joshi was born in 1962"
→ "Me" | "era" | " Joshi" | " was" | " born" | " in" | " 19" | "62"
```

Here, we can see that:

- "Meera" got broken into two tokens: "Me" and "era".
- Common words like " was", " born", and " in" are one token each.
- The year "1962" got broken into two tokens: " 19" and "62".

The exact way of breaking depends on the model, but the idea is the same everywhere. The model writes its answer token by token.

We have a detailed blog on [Tokenization in LLMs](https://outcomeschool.com/blog/tokenization-in-llms) that explains how this breaking works step by step.

**Note:** In the rest of this blog, we will treat a full year like " 1962" as one token, just for the sake of understanding. The idea stays exactly the same.

Now, let's see how the model decides which token comes next.

## How does an LLM pick the next token?

An LLM does only one thing again and again: **it looks at all the text so far and predicts the next token.**

But it does not predict just one token. It gives a score to every token it knows, and these scores become chances. Means, the model creates a list of guesses, where each guess has a percentage.

Let's take a simple example. Suppose the text so far is:

"The capital of France is"

The model creates a list of guesses for the next token like below:

| Next token | Chance |
| --- | --- |
| " Paris" | 92% |
| " a" | 3% |
| " the" | 2% |
| " located" | 1% |
| All other tokens | 2% |

Then, the model picks one token from this list. Here, it picks " Paris". Now, " Paris" gets added to the text, and the whole process repeats for the next token.

So, writing one answer looks like below:

- **Step 1:** The model looks at the text so far.
- **Step 2:** It creates a list of guesses with chances for the next token.
- **Step 3:** It picks one token from the list.
- **Step 4:** It adds that token to the text.
- **Step 5:** It goes back to Step 1.

This loop runs until the answer is complete.

**Very important:** In this whole loop, there is no step called "check if this is true." There is only "pick a likely next token." This is the root of the problem.

## Easy tokens and fact tokens

Now, let's look closely at our hallucinated sentence again:

"Meera Joshi was born in 1962."

Not every token in this sentence is equally hard.

- " was", " born", " in" are **easy tokens**. They follow the rules of language. Any sentence about a birth year will have them. The model is almost always right about them.
- " 1962" is a **fact token**. It carries the actual information. To get it right, the model must truly know the fact.

Most tokens in any answer are easy tokens. Only a few tokens are fact tokens. But those few tokens decide whether the answer is true or false.

**The model uses the exact same loop for both kinds of tokens.** It does not slow down for a fact token. It does not switch to a "careful mode." It just creates a list of guesses and picks one, the same way it picked " was".

So, the confident grammar around the fact makes the wrong fact look confident too.

## When the model knows: a sharp guess

When the model has seen a fact many times during training, its list of guesses becomes **sharp**. Means, one token gets almost all the chance.

Let's say the text so far is:

"Albert Einstein was born in the year"

The list of guesses for the next token looks like below:

| Next token | Chance |
| --- | --- |
| " 1879" | 95% |
| " 1878" | 2% |
| " 1880" | 1% |
| All other tokens | 2% |

Here, we can see that one token is far ahead of all the others. The model has read about Einstein thousands of times. So, the fact is strongly stored inside it.

When the guess is sharp, the model picks the right token almost every time.

## When the model does not know: a flat guess

Now, let's go back to our little-known author. The text so far is:

"Meera Joshi was born in the year"

The model has never read about her. So, its list of guesses looks like below:

| Next token | Chance |
| --- | --- |
| " 1962" | 14% |
| " 1958" | 13% |
| " 1971" | 13% |
| " 1965" | 12% |
| " 1960" | 12% |
| " 1968" | 12% |
| " 1955" | 12% |
| " 1974" | 12% |

Here, we can notice that the chances are spread out almost evenly. No token is far ahead. This is called a **flat** guess.

A flat guess is the model's way of saying "I am not sure." The model knows the next token must be a year, because that is how such sentences work. But it has no idea which year.

Let's understand this with a simple analogy. Suppose there is a class of 100 students who have all read about Einstein many times. We ask them, "In which year was Einstein born?" Almost all of them shout "1879" together. That is a sharp guess. Now, we ask the same class, "In which year was Meera Joshi born?" Nobody knows, so each student shouts a different year. That is a flat guess.

So, at the token level:

- **Sharp guess** = the model knows.
- **Flat guess** = the model does not know.

The model has some sense of its uncertainty. It is hidden inside these chances. But now, the question is: what does the model do with a flat guess?

The answer is: it still picks one token. Let's see it in action.

## Picking a token in code

The best way to learn this is by taking an example. Let's write Python code that picks a token from a list of guesses, the same way an LLM does.

We can write the code as below:

```python
import random
sharp_guess = {"1879": 0.95, "1878": 0.02, "1880": 0.01, "other": 0.02}
flat_guess = {"1962": 0.14, "1958": 0.13, "1971": 0.13, "1965": 0.12,
              "1960": 0.12, "1968": 0.12, "1955": 0.12, "1974": 0.12}
def pick_next_token(guesses):
    tokens = list(guesses.keys())
    chances = list(guesses.values())
    # pick one token, where a higher chance means picked more often
    return random.choices(tokens, weights=chances)[0]
print(pick_next_token(sharp_guess))
print(pick_next_token(flat_guess))
```

Here, we have:

- `sharp_guess`: the list of guesses for Einstein. One token has 95% chance, and "other" stands for all other tokens together.
- `flat_guess`: the list of guesses for Meera Joshi. The chances are spread out.
- `pick_next_token`: a function that picks one token, where a token with a higher chance gets picked more often.

It will print something like the following:

```
1879
1971
```

If we run this code many times, the first `print` shows "1879" almost every time. But the second `print` keeps changing its answer, for example "1962" once, "1971" next time, and "1955" after that.

Here, we can see that **the function always returns a token.** It never returns "I do not know." Even for the flat guess, it gives us a year. And when that year is written into a sentence, it looks exactly as confident as "1879".

This is how a hallucination is generated at the level of a single token.

Now, let's understand each reason in detail.

## Reason 1: There is no "skip" option

At every step, the model must pick a token from its list. The list contains tokens like " 1962", " 1958", and so on. There is no special button that says "stop, I do not know this one."

Let's say a student is given a fill-in-the-blank test, and the rule is that they must write something in every blank. Even when they have no idea, they must write a word. Many of their answers will look correct but be wrong.

The LLM is in the same situation for every single token.

Now, the question is: the words "I do not know" are also made of tokens, so why does the model not pick them?

The model writes them only if they are the likely next tokens. But there are two problems:

- During training, the model has seen far more text where a question is followed by an answer than text where a question is followed by "I do not know."
- Many training and testing methods often give a better score to a confident guess than to an honest "I do not know."

So, the "I do not know" tokens usually get a small chance.

Hence, when the guess for a fact token is flat, the model still picks a year, a name, or a number. It fills the blank.

## Reason 2: Randomness picks a token from the flat guess

When an LLM picks the next token, there is usually some randomness. It does not always pick the top token. A setting called **[temperature](https://outcomeschool.com/blog/how-does-temperature-control-llm-output)** controls how much randomness is used.

So:

- **Low temperature** = the model almost always picks the top token.
- **High temperature** = the model picks other tokens more often.

With a sharp guess, randomness does not matter much. " 1879" has 95% chance, so it wins almost every time.

But with a flat guess, randomness decides the answer. Every year has about 12% to 14% chance. So, if we ask the same question five times, we can get different years each time, like below:

```
Run 1: Meera Joshi was born in 1962.
Run 2: Meera Joshi was born in 1971.
Run 3: Meera Joshi was born in 1955.
Run 4: Meera Joshi was born in 1962.
Run 5: Meera Joshi was born in 1968.
```

Here, we can see that every answer is written with full confidence, but the answers do not agree with each other. This disagreement is a strong sign that the model is guessing.

Now, someone can ask: "Then let's just set temperature to zero. The model will always pick the top token."

Yes, it will always pick " 1962" now. But " 1962" had only 14% chance. It is still a guess. Now, it is just the same guess every time.

Hence, a low temperature makes the answer the same every time, but it does not make it correct.

## Reason 3: A token cannot be taken back

When we write something by hand and notice a mistake, we use an eraser.

An LLM has no eraser. Once a token is picked and added to the text, it stays there forever. The model can only move forward and add the next token.

Let's take an example. Suppose we ask the model:

"Is 3,827 a prime number?"

The very first token of the answer is a big decision. For the sake of example, let say the list of guesses looks like below:

| Next token | Chance |
| --- | --- |
| "Yes" | 52% |
| "No" | 48% |

The two chances are almost equal. Let's say the model picks "Yes".

But 3,827 is not a prime number. It is 43 \* 89.

The model cannot go back and change "Yes" to "No". The wrong token is already written. Everything that comes after is built on top of this "Yes".

## Reason 4: One wrong token leads to more wrong tokens

Remember, at every step, the model looks at **all the text so far**, including the tokens it wrote itself. It does not go back to doubt its own tokens. It simply treats them as part of the text that it must continue.

So, after writing "Yes", the text so far is:

"Is 3,827 a prime number? Yes"

Now, the model predicts the next token based on this. And the most likely continuation of "Yes" is a reason that supports "Yes". So, it writes something like:

"Yes, 3,827 is a prime number because it cannot be divided by any number other than 1 and itself."

Each new token is a good, likely token given the text before it. The grammar is correct. The explanation sounds logical. But the whole answer is built on one wrong token at the start.

The same happens with our author:

"Meera Joshi was born in 1962. She grew up in the 1970s and published her first book in the late 1980s."

Here, we can see that the model did not stop at one wrong year. It used " 1962" to build more details: she grew up in the 1970s, published in the late 1980s. All of these follow nicely from 1962, and all of them are made up.

**One wrong fact token becomes the base for the next tokens, and a small guess grows into a full made-up story.**

## Reason 5: Likely tokens can combine into something that does not exist

Now, let's see a special type of hallucination: fake names, fake titles, and fake references.

Suppose we ask the model to suggest a research paper on a topic. The model writes something like below:

"Sharma, A. and Patel, R. (2019). Using AI to Detect Crop Diseases. Journal of Agricultural AI."

Let's look at it token by token:

- "Sharma" is a common author name. A likely token.
- "Patel" is also a common author name. A likely token.
- "2019" is a common year for such papers. A likely token.
- "Using AI to Detect Crop Diseases" is a natural title for this topic. Each token in it is likely.
- "Journal of Agricultural AI" sounds like a real journal name. Likely tokens.

Each token, on its own, is a reasonable pick. But assume that this exact paper, with these exact authors, this exact year, and this exact journal, does not exist anywhere.

The only thing that mattered to the model was that each token fits well with the tokens before it. Nothing in the loop checked that the full combination exists in the real world. Hence, it combined likely tokens into a reference that does not exist.

This is why LLMs are very good at producing references that look real, but are not.

## Reason 6: The final text hides the uncertainty

We already learned that the model has some sense of its uncertainty. A flat guess means "I am not sure."

After the model picks a token, only the token remains in the text. The chance behind it is thrown away.

So, when we read the final answer, both of these look exactly the same:

- " 1879", which had 95% chance.
- " 1962", which had 14% chance.

Both are just numbers in a sentence. Both are written in the same confident tone. There is no small "14%" written next to the second one.

Means, the model was unsure inside, but its words look sure outside. As readers, we see only the words. Hence, we have no way to tell the sure parts from the guessed parts just by reading.

## How can we reduce hallucinations at the token level?

Now, let's see how we can reduce hallucinations. Each fix addresses one of the reasons we learned.

**Fix 1: Give the model the fact.**

If we put the correct information inside the question itself, for example by pasting a document, the fact is now part of the text so far. The model can see it. So, the flat guess becomes a sharp guess.

Here comes the **[RAG](https://outcomeschool.com/blog/agentic-rag)** into the picture. RAG stands for Retrieval-Augmented Generation. In simple words, first find the right information, then give it to the model along with the question.

**Fix 2: Make "I do not know" a likely token.**

The companies that build these models can train them to say "I do not know" when they are unsure, and give a better score to an honest "I do not know" than to a confident wrong guess. Then, the "I do not know" tokens get a bigger chance when the guess for a fact token is flat. This addresses Reason 1.

**Fix 3: Look at the chances behind the tokens.**

Many AI tools can show the chance behind each token. If a fact token like a year or a name was picked with a low chance, we can flag it as "likely a guess." This brings back the uncertainty that the final text was hiding.

Similarly, we can ask the same question a few times, like we saw in Reason 2. If the fact tokens keep changing between the answers, the model is guessing. This addresses Reason 6.

**Fix 4: Ask the model to think before answering.**

If the model first [writes its thinking step by step](https://outcomeschool.com/blog/how-does-chain-of-thought-prompting-work), the important decision does not depend on a single uncertain token at the very start. For example, the model can first try dividing 3,827 by small numbers, find 43 \* 89, and only then write "No". It does not fully solve the problem, but it gives the model a better chance to reach the right token. This addresses Reason 3 and Reason 4.

**Fix 5: Use low temperature for facts.**

For factual tasks, a low temperature reduces random jumps to unlikely tokens. But remember, it makes the answer the same every time, not correct. So, use it along with the other fixes, not alone. This addresses Reason 2.

**Fix 6: Always verify fact tokens.**

As users, we now know that names, numbers, dates, and references are the fact tokens. Hallucinations mostly appear in these tokens. So, these are the places we must double-check before trusting the answer.

**Note:** None of these fixes remove hallucinations completely. As long as a model writes by picking the next likely token, there will always be some chance of a confident guess.

Now we must have understood why LLMs hallucinate at the token level: the model picks one likely token at a time, and when it does not know the answer, it still has to pick one.

## Frequently Asked Questions

### Is an LLM lying when it hallucinates?

No. An LLM is not lying on purpose when it hallucinates. It picks a likely next token at every step, and when it does not know the right token, it still has to pick one. The result is a guess that sounds correct and confident, but is actually wrong or made up.

### Which parts of an LLM answer are most likely to be hallucinated?

The fact tokens, such as names, numbers, dates, and references, are the most likely to be hallucinated. Easy tokens like " was" and " in" follow the rules of language, so the model is almost always right about them. Fact tokens need the model to truly know the fact, so these are the places we must double-check.

### How can we tell when an LLM is guessing?

We can look at the chance behind each token, because many AI tools can show it. If a fact token like a year or a name was picked with a low chance, it is likely a guess. We can also ask the same question a few times, and if the fact tokens keep changing between the answers, the model is guessing.

### Does setting temperature to zero stop hallucinations?

No. Setting temperature to zero makes the model always pick the top token, so the answer is the same every time. But if the top token had only a small chance, it is still a guess, just the same guess every time. A low temperature makes the answer the same, not correct.

### Can we remove hallucinations completely?

No. Fixes like RAG, training the model to say "I do not know", and checking the chances behind tokens reduce hallucinations, but none of them remove hallucinations completely. As long as a model writes by picking the next likely token, there will always be some chance of a confident guess.
