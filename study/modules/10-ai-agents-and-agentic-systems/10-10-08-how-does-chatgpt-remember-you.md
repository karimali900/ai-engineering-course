---
title: How does ChatGPT remember you?
module: 10
module_title: AI Agents and Agentic Systems
lesson: '10.8'
source: https://outcomeschool.com/blog/how-does-chatgpt-remember-you
published: October 12, 2026
tags:
- ai-agent
- llm
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 2655
reading_time: 13
status: full
---
# How does ChatGPT remember you?

> **Module 10 · Lesson 10.8**  
> Source: [Outcome School](https://outcomeschool.com/blog/how-does-chatgpt-remember-you) · Published: October 12, 2026 · Reading time: ~13 min · Tags: `ai-agent`, `llm`, `ai`, `system-design`

---

![How does ChatGPT remember you?](../../assets/images/10-10-08-how-does-chatgpt-remember-you/how-does-chatgpt-remember-you.png)

ChatGPT remembers you by saving small notes about you outside the AI model and adding those notes back into the conversation whenever you chat. The model itself does not change when you chat with it, it reads your notes before it replies.

In this blog, we will learn about how ChatGPT remembers you. We will also see why an LLM forgets everything by default, what the context window is, how saved memories, chat history, and Custom Instructions work, how these memories are added to our message behind the scenes, how we can see and delete what it remembers, and where memory helps and where it fails.

We will cover the following:

- Does ChatGPT really remember us?
- Why does an LLM forget everything by default?
- What is the context window?
- How does ChatGPT remember within one chat?
- What is ChatGPT Memory?
- Saved memories: facts it writes down about us
- Reference chat history: learning from past chats
- Custom Instructions: what we tell it about ourselves
- How are memories added into the prompt?
- A complete example: from "I am a vegetarian" to a recipe suggestion
- A simple code example
- How can we see and delete memories?
- Temporary Chat: talking without memory
- Where memory helps and where it fails

Let's get started.

## Does ChatGPT really remember us?

Let's say Riya is a school teacher. On Monday, she tells ChatGPT: "I am a vegetarian and I live in Bengaluru."

On Saturday, she opens a brand new chat and asks: "Suggest a quick dinner recipe for tonight."

ChatGPT replies with a vegetarian recipe. It feels like talking to a friend who remembers her.

Now, the question is: does ChatGPT really remember us like a human does?

The answer is no, not in the way we think. The AI model inside ChatGPT does not remember anything at all. There is a separate system around the model that keeps notes about us and shows those notes to the model at the right time.

The AI model writes the replies. The note-keeping system does the remembering.

## Why does an LLM forget everything by default?

The AI model inside ChatGPT is an **LLM** (Large Language Model). An LLM is a model that has learned from a huge amount of text to [predict the next word](https://outcomeschool.com/blog/autoregressive-models). That is how it writes answers, one small piece at a time.

This learning is called **training**, and it happens once, before we ever use the model. After training, the model is frozen. When we chat with it, nothing inside the model changes. It does not learn our name. It does not store our chats.

An LLM is like a very smart person with no memory at all. Every time we talk to this person, they meet us for the first time.

Means, every reply depends only on the text that is sent to the model at that moment. Nothing else.

## What is the context window?

**The context window is all the text that the LLM can read at one time before writing its reply.**

Think of it as a desk. Whatever papers are kept on the desk, the LLM can read them. Whatever is not on the desk, the LLM cannot see.

The desk has a limited size. We cannot put unlimited papers on it. So, ChatGPT cannot keep everything about us on the desk, it must choose.

So, if we want the LLM to know something, that thing must be on the desk.

We have a detailed blog on [Context Engineering](https://outcomeschool.com/blog/context-engineering) that explains how to choose what goes on this desk.

## How does ChatGPT remember within one chat?

Suppose Riya is chatting like below:

```
Riya: My name is Riya.
ChatGPT: Nice to meet you, Riya.
Riya: What is my name?
ChatGPT: Your name is Riya.
```

How did it remember her name? We just learned that the model has no memory.

The answer is simple. When Riya sends her second message, ChatGPT does not send only "What is my name?" to the model. It sends the full conversation so far, like below:

```
Riya: My name is Riya.
ChatGPT: Nice to meet you, Riya.
Riya: What is my name?
```

Here, the model reads the whole conversation on the desk, finds "My name is Riya", and answers.

So, within one chat, the memory is just the old messages being sent again with every new message.

When Riya starts a new chat, the desk is empty. The old chat is not on it. The model has no idea who she is.

We needed a solution for that, and ChatGPT Memory was introduced to solve this problem.

## What is ChatGPT Memory?

**ChatGPT Memory is a feature that keeps useful information about us across different chats, so that we do not have to repeat ourselves every time.**

In simple words, ChatGPT keeps a notebook about us. This notebook is kept outside the model, in a separate storage place. Before every reply, ChatGPT opens the notebook and puts the useful pages on the desk.

We have a detailed blog on [AI Agent Memory](https://outcomeschool.com/blog/ai-agent-memory) that covers this idea end to end.

ChatGPT fills this notebook in two ways:

- **Saved memories**: clear facts that are written down as short notes.
- **Reference chat history**: useful details picked up from our past chats.

Along with these, there is one more thing called **Custom Instructions**, which we write ourselves.

We will learn about each of them in detail.

## Saved memories: facts it writes down about us

**Saved memories are short facts about us that ChatGPT writes down and keeps until we delete them.**

There are two ways a fact gets saved.

First, we can ask directly, like below:

"Remember that I am a vegetarian."

Second, ChatGPT can decide on its own that a fact will be useful in the future. For example, if Riya says "I teach maths to class 8 students", ChatGPT can save that as a memory.

When a memory is saved, ChatGPT shows a small message like "Memory updated" in the chat.

The saved memories look like below:

```
- Riya is a vegetarian.
- Riya lives in Bengaluru.
- Riya teaches maths to class 8 students.
```

Here, we can see that these are not full chats. These are short notes. Short notes take very less space on the desk, so ChatGPT can bring them into any new chat.

## Reference chat history: learning from past chats

Saved memories need a clear fact to be written down. But many useful details are hidden inside our old chats, and nobody wrote them down as a note.

Here comes the reference chat history into the picture.

**Reference chat history lets ChatGPT look at our past chats and use the useful parts in a new chat.**

Let's say last month Riya had a long chat about planning a trip to Goa in December. She never said "remember this". Today, she asks: "What should I pack for my trip?" ChatGPT can connect this with her earlier Goa plan and suggest light cotton clothes and sunscreen.

But, ChatGPT cannot put all our old chats on the desk. There are too many of them, and the desk is limited. So, it picks only the small parts that look useful for the current chat, and puts only those on the desk.

Let me tabulate the differences between saved memories and reference chat history for your better understanding.

|  | Saved memories | Reference chat history |
| --- | --- | --- |
| What it is | Clear facts written as short notes | Useful details picked from past chats |
| How it is created | We ask, or ChatGPT decides to save | Picked from our old chats when needed |
| Can we see a list? | Yes, in the settings | No fixed list |
| How long it stays | Until we delete it | Changes as our chats change |

## Custom Instructions: what we tell it about ourselves

**Custom Instructions are a short piece of text that we write ourselves in the settings, telling ChatGPT about us and how we want it to reply.**

For example, Riya can write like below:

```
About me: I am a school teacher. I teach maths to class 8 students.
How to reply: Keep answers short and use simple examples.
```

The difference is that we write Custom Instructions by hand, and ChatGPT never changes them on its own. Saved memories and chat history are collected by ChatGPT while we chat.

## How are memories added into the prompt?

A **prompt** is the full text that is sent to the LLM. Means, the prompt is whatever is kept on the desk.

Before the LLM sees our new message, ChatGPT builds a bigger prompt. Just for the sake of understanding, the prompt looks like below:

```
[Rules from the company that makes ChatGPT]
You are ChatGPT, a helpful assistant.
[Custom Instructions]
I am a school teacher. Keep answers short.
[Saved memories]
- Riya is a vegetarian.
- Riya lives in Bengaluru.
[Useful details from past chats]
- Riya often asks for South Indian dishes.
[Current chat]
Riya: Suggest a quick dinner recipe for tonight.
```

Here, we can notice that Riya typed only one line. But the LLM receives many lines. Those extra lines are the memory.

One more thing to notice: the Goa trip is not in this prompt. It is not useful for a dinner recipe, so ChatGPT did not put it on the desk.

**Note:** The real prompt used inside ChatGPT is not public, and its exact format is different. This is a simplified picture, just for the sake of understanding.

**Very important:** The model is not remembering anything. It is reading. ChatGPT Memory is just the right notes put on the desk at the right time.

This is how ChatGPT remembers you.

## A complete example: from "I am a vegetarian" to a recipe suggestion

Let's put everything together, step by step.

**Step 1:** On Monday, in chat A, Riya types: "Remember that I am a vegetarian."

**Step 2:** ChatGPT writes the note "Riya is a vegetarian." into the notebook and shows "Memory updated".

**Step 3:** Chat A ends. The model forgets everything, as always. But the note is safe in the notebook, because the notebook is outside the model.

**Step 4:** On Saturday, Riya opens a new chat B and types: "Suggest a quick dinner recipe."

**Step 5:** Before sending this message to the model, ChatGPT opens the notebook and adds "Riya is a vegetarian." to the prompt.

**Step 6:** The model reads the prompt, sees the note, and suggests a vegetable upma instead of a chicken curry.

The model never changed. Only the prompt changed.

## A simple code example

Now, let's see the same idea in code. We can write the code as below:

```python
memory_store = []  # our notebook, kept outside the model
def save_memory(note):
    memory_store.append(note)
def build_prompt(user_message):
    notes = "\n".join("- " + note for note in memory_store)
    return (
        "You are a helpful assistant.\n"
        "What you know about the user:\n" + notes + "\n\n"
        "User: " + user_message
    )
# Chat A on Monday
save_memory("Riya is a vegetarian.")
# Chat B on Saturday, a brand new chat
prompt = build_prompt("Suggest a quick dinner recipe.")
reply = call_llm(prompt)  # send the full prompt to the LLM
```

Here, we have:

- `memory_store`: our notebook. It lives outside the LLM, so it is not erased when a chat ends.
- `save_memory`: writes a new note into the notebook.
- `build_prompt`: takes all the notes and puts them before the user's message. Here, `\n` means "start a new line".
- `call_llm`: sends the full prompt to the model. For the sake of example, assume that it is a function that talks to any LLM.

If we print the `prompt`, it will print the following:

```
You are a helpful assistant.
What you know about the user:
- Riya is a vegetarian.
User: Suggest a quick dinner recipe.
```

Here, we can see that the note from Monday is now on the desk in Saturday's chat.

**Note:** In a real system, the notes are not kept in a simple list. They are saved in a database. So, they stay safe even when we close the app. Also, a real system picks only the useful notes for each chat, not all of them.

## How can we see and delete memories?

ChatGPT gives us control over what it remembers. We can:

- Ask directly: "What do you remember about me?"
- Open the settings, under **Personalization**, to see the list of saved memories and delete any of them.
- Ask in the chat: "Forget that I live in Bengaluru."
- Update a fact by telling it: "I have moved to Pune."
- Turn off saved memories or reference chat history completely.

**Note:** Deleting a chat does not delete the saved memories that were created in that chat. A saved memory stays until we delete the memory itself.

## Temporary Chat: talking without memory

Sometimes, we want a chat that is not remembered at all. For example, Riya wants to plan a surprise birthday gift for her sister, and she does not want this to show up in her future chats.

So, here comes the **Temporary Chat** to the rescue.

A Temporary Chat does not use our saved memories, and it does not create new memories. It also does not appear in our chat history.

It is like talking to the LLM with a closed notebook.

## Where memory helps and where it fails

Now, let's see where memory works well and where it fails.

**Where it helps:**

- We do not need to repeat ourselves in every chat.
- Answers fit our needs, like our diet, our job, and the way we like replies.
- Long work, like preparing for an exam, continues smoothly across many chats.

**Where it fails:**

- **Old or wrong notes:** If Riya moves to Pune but the note still says Bengaluru, the answers will be wrong until she fixes it.
- **Missed details:** The desk is limited, so sometimes ChatGPT does not pick the useful detail from our past chats.
- **Unwanted notes:** ChatGPT can save something we did not want it to keep. So, we must check our saved memories from time to time.
- **No real understanding:** It is still reading notes. It does not know us like a friend does.

The model itself never remembers anything. ChatGPT keeps notes about us outside the model, and before every reply, it puts the right notes on the desk for the model to read.

## Frequently Asked Questions

### Does ChatGPT Memory change the AI model?

No. The AI model inside ChatGPT is frozen after training, and nothing inside it changes when we chat. ChatGPT keeps notes about us outside the model, in a separate storage place, and adds the useful notes to the prompt before every reply. The model only reads them.

### Does deleting a chat also delete the memories saved from it?

No. Deleting a chat does not delete the saved memories that were created in that chat. A saved memory stays until we delete the memory itself, either from the list under Personalization in the settings or by asking ChatGPT to forget it.

### Can ChatGPT save a memory without us asking?

Yes. Along with the facts we ask it to remember, ChatGPT can decide on its own that a fact will be useful in the future and save it. When this happens, it shows a small "Memory updated" message in the chat. This is why we should check our saved memories from time to time.

### Does ChatGPT send all our past chats to the model?

No. The context window is limited, so ChatGPT cannot put all our old chats into it. It picks only the small parts of past chats that look useful for the current chat. For example, an old chat about a Goa trip is left out when we ask for a dinner recipe.

### Can ChatGPT change our Custom Instructions on its own?

No. We write Custom Instructions by hand in the settings, and ChatGPT never changes them on its own. Saved memories and chat history are different, because ChatGPT collects those while we chat.
