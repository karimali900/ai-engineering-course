---
title: What is turn-taking in a voice AI agent?
module: 16
module_title: AI Infrastructure, Deployment, and System Design
lesson: '16.9'
source: https://outcomeschool.com/blog/what-is-turn-taking-in-a-voice-ai-agent
published: October 19, 2026
tags:
- ai-agent
- llm
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 3035
reading_time: 15
status: full
---
# What is turn-taking in a voice AI agent?

> **Module 16 · Lesson 16.9**  
> Source: [Outcome School](https://outcomeschool.com/blog/what-is-turn-taking-in-a-voice-ai-agent) · Published: October 19, 2026 · Reading time: ~15 min · Tags: `ai-agent`, `llm`, `ai`, `system-design`

---

![What is turn-taking in a voice AI agent?](../../assets/images/16-16-09-what-is-turn-taking-in-a-voice-ai-agent/what-is-turn-taking-in-a-voice-ai-agent.png)

Turn-taking in a voice AI agent is the skill of knowing when the user has finished speaking, when the agent should start speaking, and when the agent should stop because the user wants to talk again.

In this blog, we will learn about turn-taking in a voice AI agent. We will also see how humans take turns in a conversation, why this is hard for a machine, how a voice AI agent detects the end of a turn using silence and meaning, how it handles interruptions and short sounds like "uh-huh", and how full-duplex models take a different path.

We will cover the following:

- What is turn-taking?
- How humans take turns
- How a voice AI agent works
- Why turn-taking is hard for a machine
- The two jobs of turn-taking
- Approach 1: Wait for silence
- Approach 2: Understand the meaning
- Handling interruptions
- Not every sound is a new turn
- Half-duplex vs full-duplex agents
- A complete walkthrough

Let's get started.

## What is turn-taking?

**Turn-taking is the way two speakers decide who talks and when, so that they do not talk over each other and do not leave long awkward silences.**

A **turn** is one chunk of speech by one speaker. When we say, "What is the weather today?", that full sentence is one turn. When the other person replies, "It is sunny," that is the next turn.

So, a conversation is a chain of turns:

```
User:  What is the weather today?      (turn 1)
Agent: It is sunny and 28 degrees.     (turn 2)
User:  Should I carry an umbrella?     (turn 3)
Agent: No, you will not need one.      (turn 4)
```

A **voice [AI agent](https://outcomeschool.com/blog/ai-agent)** is a system that talks with us using voice. We speak, it listens, it thinks, and it speaks back. Customer support phone bots, voice assistants, and AI receptionists are all voice AI agents.

For a voice AI agent, turn-taking means answering three questions again and again:

- Has the user finished speaking?
- Is it my turn to speak now?
- Has the user started speaking again while I am talking?

If the agent gets these answers right, the conversation feels natural.

## How humans take turns

Before jumping into the machine side, we must understand how we humans do it.

We humans are very good at turn-taking. A study of conversations in ten languages found that the most common gap between one person finishing and the other person starting is between 0 and 200 milliseconds.

This gap is too short to hear the full sentence, think of an answer, and then start speaking. Means, we start preparing our reply while the other person is still talking. We predict when they are about to finish.

We use many signals for this:

- **The words:** "I want to book a table for..." is clearly not finished.
- **The tone:** our voice usually falls at the end of a statement and often rises at the end of a yes-or-no question.
- **The pause:** a short pause in the middle of a thought is different from a pause at the end.

We also do two more things naturally:

- We stop talking when the other person cuts in with something important.
- We say small things like "uh-huh", "right", and "okay" while the other person is talking, just to show we are listening. These do not take the turn.

A voice AI agent must learn to do all of this, and that too over a phone line where it cannot see the user.

## How a voice AI agent works

Now, let's see what is inside a typical voice AI agent, because turn-taking sits right in the middle of it.

Many voice AI agents use a [pipeline of three main parts](https://outcomeschool.com/blog/cascaded-vs-speech-to-speech):

```
        User speaks
             ↓
+-------------------------+
| Speech-to-Text (STT)    |
| sound -> text           |
+-------------------------+
             ↓
+-------------------------+
| LLM                     |
| text -> reply text      |
+-------------------------+
             ↓
+-------------------------+
| Text-to-Speech (TTS)    |
| reply text -> sound     |
+-------------------------+
             ↓
       Agent speaks
```

- **Speech-to-Text (STT):** converts the user's voice into text. It is also called ASR (Automatic Speech Recognition).
- **LLM (Large Language Model):** reads the text and writes a reply.
- **Text-to-Speech (TTS):** converts the reply text back into voice.

Here, we can see that something must decide when to send the user's words to the LLM. If we send them too early, the LLM answers half a question. If we send them too late, [the user waits in silence](https://outcomeschool.com/blog/time-to-first-audio).

That decision is turn-taking.

## Why turn-taking is hard for a machine

A machine does not hear a conversation the way we do. It just receives a continuous stream of sound, sliced into tiny pieces, for example, one piece every 20 milliseconds.

The problem is that the same sound can mean different things.

Let's say the user is quiet for one full second. This can mean:

- The user has finished and is waiting for the answer.
- The user is thinking about what to say next.
- The user is reading their card number from a piece of paper.

The silence looks exactly the same in all three cases. Only the context tells them apart.

Now, the agent can do two kinds of mistakes:

- **Cutting in too early:** The user says, "My phone number is 98765..." and pauses to check the next digits. The agent jumps in with "Thank you" before the user is done.
- **Waiting too long:** The user asks a simple question, and the agent waits two seconds before replying. The user thinks the call has dropped and says "Hello?"

Good turn-taking keeps both mistakes as low as possible.

## The two jobs of turn-taking

Now, we can split turn-taking into two jobs:

- **End-of-turn detection:** knowing when the user has finished, so the agent can start speaking.
- **Interruption handling:** knowing when the user starts speaking while the agent is talking, so the agent can stop.

End-of-turn detection is also called **endpointing**, because it finds the end point of the user's speech.

Let's start with end-of-turn detection.

## Approach 1: Wait for silence

The simplest idea is this: if the user stops making sound for some time, their turn is over.

To do this, the agent needs a way to know whether the user is speaking at all. Here comes the **Voice Activity Detection (VAD)** into the picture.

**Voice Activity Detection (VAD) is a small, fast component, usually a small model, that looks at each tiny piece of audio and says whether it contains human speech or not.**

It does not understand words. It only answers "speech" or "no speech" for every piece of sound, as below:

```
Audio piece:  1       2       3       4       5       6       7
Sound:        hello   how     are     you     (quiet) (quiet) (quiet)
VAD says:     speech  speech  speech  speech  silent  silent  silent
```

Now, we add a rule on top of the VAD:

**If the VAD reports silence for longer than a fixed time, for example, 700 milliseconds, the turn is over.**

This fixed time is called the **silence threshold** or **silence timeout**.

Let's see it in action:

```
+-------------------------------------------+
| User says "What is the weather today?"    |
+-------------------------------------------+
                      ↓
+-------------------------------------------+
| VAD: speech, speech, speech, then silence |
+-------------------------------------------+
                      ↓
+-------------------------------------------+
| Silence lasts 700 milliseconds            |
+-------------------------------------------+
                      ↓
+-------------------------------------------+
| End of turn detected                      |
+-------------------------------------------+
                      ↓
+-------------------------------------------+
| Text is sent to the LLM                   |
+-------------------------------------------+
```

This approach is simple, fast, and cheap.

The problem is that the agent now has to pick one number for the timeout, and no single number works for everyone.

- If the timeout is short, for example, 300 milliseconds, the agent replies fast, but it cuts in whenever the user pauses to think.
- If the timeout is long, for example, 1500 milliseconds, the agent rarely cuts in, but every reply feels slow.

We have a detailed blog on [how to build a latency budget for a voice AI agent](https://outcomeschool.com/blog/voice-agent-latency-budget) that explains how this waiting time fits with every other stage of the reply.

Silence alone does not know whether the sentence is complete. "My number is 98765" followed by a pause looks the same as "Thank you" followed by a pause.

The issue with this approach is that it only listens to the sound, not to the meaning. Let's see how the next approach solve this issue.

## Approach 2: Understand the meaning

We humans do not wait for a fixed silence. We listen to what is being said. So, the better idea is to give the agent the same ability.

This is called **semantic turn detection**. Semantic means "related to meaning".

**Semantic turn detection uses a model that reads the words (and sometimes listens to the tone) and predicts the chance that the user has finished their turn.**

The model gives a number between 0 and 1. A number close to 1 means the user has most likely finished. Let's take an example. The user stops speaking after each of these:

| What the user said | Chance the turn is over | What the agent does |
| --- | --- | --- |
| "What time do you open?" | High, for example 0.95 | Reply quickly |
| "I want to book a table for" | Low, for example 0.05 | Wait longer |
| "My card number is 4512 8890" | Low, for example 0.20 | Wait longer |
| "Okay, that is all, thank you." | High, for example 0.97 | Reply quickly |

Here, we can see that the words tell us a lot. A sentence ending with "for" is clearly unfinished. A complete question like "What time do you open?" is finished.

In practice, the two approaches are combined. The VAD still detects when the user goes silent. Then the turn detection model decides how long to wait, as below:

```
+---------------------------------------------------------------+
| VAD detects silence                                           |
+---------------------------------------------------------------+
                                ↓
+---------------------------------------------------------------+
| Turn detection model reads the words so far                   |
+---------------------------------------------------------------+
                ↓                                ↓
+-------------------------------+ +-----------------------------+
| Sentence looks complete       | | Sentence looks incomplete   |
| wait a short time             | | wait a longer time          |
+-------------------------------+ +-----------------------------+
                ↓                                ↓
+---------------------------------------------------------------+
| End of turn detected                                          |
+---------------------------------------------------------------+
```

So, the silence timeout is no longer one fixed number. It becomes short when the user seems done and long when the user seems to be in the middle of a thought.

Some turn detection models only read the text from the STT. Some models listen to the audio directly, so they can also use the tone of the voice, like the falling pitch at the end of a statement.

## Handling interruptions

Now, let's move to the second job of turn-taking: handling interruptions.

Suppose the agent is reading out a long list of available flights. In the middle, the user says, "Wait, I only want morning flights." The agent must stop talking and listen.

When the user speaks while the agent is speaking, it is called **[barge-in](https://outcomeschool.com/blog/what-is-barge-in-in-a-voice-ai-agent)**. The user "barges in" on the agent's turn.

To handle barge-in, the agent keeps its VAD running even while it is speaking. The flow looks like below:

```
+--------------------------------------+
| Agent is speaking                    |
+--------------------------------------+
                    ↓
+--------------------------------------+
| VAD detects user speech              |
+--------------------------------------+
                    ↓
+--------------------------------------+
| Agent stops its audio immediately    |
+--------------------------------------+
                    ↓
+--------------------------------------+
| Agent listens to the user's new turn |
+--------------------------------------+
                    ↓
+--------------------------------------+
| LLM replies using the new request    |
+--------------------------------------+
```

There are a few important details here.

**First,** the agent must stop fast. If the agent keeps talking for another two seconds after the user starts, the user feels ignored.

**Second,** the agent must not hear itself. The microphone can pick up the agent's own voice coming out of the speaker. If the agent treats its own voice as the user, it will keep interrupting itself. To solve this, voice systems use **echo cancellation**, which removes the agent's own voice from the microphone input.

**Third,** the agent must remember what the user actually heard. If the agent planned to say five sentences but was interrupted after two, the [conversation history](https://outcomeschool.com/blog/ai-agent-memory) must record only those two. Otherwise, the LLM will assume the user heard information that was never spoken.

## Not every sound is a new turn

Now, the next big question is: should the agent stop every time the user makes a sound?

The answer is no.

While the agent is speaking, the user can say "uh-huh", "okay", "right", or "mm-hmm". These are called **backchannels**. They mean "I am listening, please continue." They are not an attempt to take the turn.

There are also sounds that are not speech from the user at all: a cough, a door closing, a TV in the background, or someone else talking in the room.

If the agent stops for every such sound, it keeps breaking off in the middle of its sentences. So, the agent must tell the difference:

| Sound while agent is speaking | What it means | What the agent does |
| --- | --- | --- |
| "Uh-huh", "okay", "right" | I am listening | Keep speaking |
| Cough, background noise | Not a turn at all | Keep speaking |
| "Wait, stop", "No, I meant Monday" | I want the turn | Stop and listen |

A common way to do this is to wait a little before stopping. For example, the agent stops only if the user keeps speaking for a minimum time, like half a second, or only if the user's words are more than a simple "okay". Some systems also use a model trained to recognize backchannels.

## Half-duplex vs full-duplex agents

Now, it's time to learn about a different design.

The pipeline agent we have seen works in a **half-duplex** way. Means, it treats the conversation as strict turns. Either it is the user's turn, or it is the agent's turn. The turn-taking system decides when to switch between the two. A walkie-talkie works this way: one person talks, then the other. Even with barge-in, the agent listens while speaking only to know when to stop.

A **full-duplex** agent works more like a phone call between two people. It listens and speaks at the same time, all the time.

Full-duplex speech models, such as Moshi from Kyutai, take in the user's audio and produce the agent's audio together, in parallel streams. There is no separate component that says "now the turn is over". The model itself learns when to speak, when to stay silent, when to say "uh-huh", and when to stop, by training on large amounts of conversation audio.

Let me tabulate the differences between half-duplex and full-duplex agents for your better understanding.

| Point | Half-duplex (pipeline) | Full-duplex |
| --- | --- | --- |
| Listening and speaking | Strict turns, one side at a time | Both at the same time |
| Turn decision | Separate VAD and turn detection model | Learned inside the model |
| Backchannels | Must be handled with extra logic | Learned by the model from conversations |
| Control and debugging | Easier, each part can be checked | Harder, everything is inside one model |
| Typical use | Many production voice agents | Research and early products |

Here, we can see that the full-duplex approach is closer to how humans talk. But the pipeline approach is easier to build, control, and [connect with tools](https://outcomeschool.com/blog/how-does-function-calling-work-in-llms) and business logic. So, many voice AI agents in production use the pipeline with careful turn-taking.

We have a detailed blog on [Design a Real-Time Voice AI Agent](https://outcomeschool.com/blog/design-a-real-time-voice-ai-agent) that covers the full system end to end.

## A complete walkthrough

Now, let's put everything together with one complete example. Suppose a user calls a restaurant's voice AI agent.

**Step 1:** The user says, "I want to book a table for..." and pauses to think. The VAD detects silence. The turn detection model sees an unfinished sentence and gives a low score, so the agent keeps waiting instead of cutting in.

**Step 2:** The user continues, "...four people tomorrow at 8 PM." The VAD detects silence again. This time, the turn detection model sees a complete sentence and gives a high score, so the agent waits only a short time. The end of the turn is detected.

**Step 3:** The text goes to the LLM, which writes a reply. The TTS starts speaking: "Sure. We have tables available at 8 PM in the main hall and on the terrace. The terrace has a view of..."

**Step 4:** While the agent is speaking, the user says "uh-huh". The agent recognizes this as a backchannel and keeps speaking.

**Step 5:** Then the user says, "Wait, terrace please." This is a real interruption. The VAD detects continued speech, and the agent stops its audio immediately. The conversation history records only the part of the reply that the user actually heard.

**Step 6:** The agent processes the new turn and replies, "Great, I have booked a terrace table for four people tomorrow at 8 PM."

Now we must have understood what turn-taking in a voice AI agent is, how the agent decides when to speak and when to stop, and how full-duplex models handle it differently.

## Frequently Asked Questions

### What is endpointing in a voice AI agent?

Endpointing is another name for end-of-turn detection. It finds the end point of the user's speech, so the agent knows the user has finished and it can start speaking. A simple version waits for a fixed silence, and a better version also reads the words to judge whether the sentence is complete.

### What is a good silence timeout for a voice AI agent?

There is no single number that works for everyone. A short timeout, like 300 milliseconds, makes the agent reply fast but cut in when the user pauses to think. A long timeout, like 1500 milliseconds, avoids cutting in but makes every reply feel slow. Semantic turn detection solves this by making the timeout short when the sentence looks complete and long when it does not.

### Why does a voice AI agent need echo cancellation?

The microphone can pick up the agent's own voice coming out of the speaker. If the agent treats its own voice as the user, it keeps interrupting itself. Echo cancellation removes the agent's own voice from the microphone input, so only the user's speech triggers an interruption.

### What happens to the agent's reply when the user interrupts it?

The agent stops its audio immediately, and the conversation history records only the part of the reply that the user actually heard. If the agent planned five sentences but was interrupted after two, only those two are kept. Otherwise, the LLM would assume the user heard information that was never spoken.

### How fast do humans take turns in a conversation?

Very fast. A study of conversations in ten languages found that the most common gap between one person finishing and the other person starting is between 0 and 200 milliseconds. This is too short to hear the full sentence and then think of a reply, so we prepare our reply while the other person is still talking.
