---
title: How does the voice-to-voice latency of a voice agent get measured?
module: 16
module_title: AI Infrastructure, Deployment, and System Design
lesson: '16.13'
source: https://outcomeschool.com/blog/voice-to-voice-latency
published: October 22, 2026
tags:
- ai-agent
- llm
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 3080
reading_time: 15
status: full
---
# How does the voice-to-voice latency of a voice agent get measured?

> **Module 16 · Lesson 16.13**  
> Source: [Outcome School](https://outcomeschool.com/blog/voice-to-voice-latency) · Published: October 22, 2026 · Reading time: ~15 min · Tags: `ai-agent`, `llm`, `ai`, `system-design`

---

![How does the voice-to-voice latency of a voice agent get measured?](../../assets/images/16-16-13-how-does-the-voice-to-voice-latency-of-a-voice-agent-get-measured/voice-to-voice-latency.png)

Voice-to-voice latency of a voice agent gets measured as the time from the moment the user stops speaking to the moment the user hears the first sound of the agent's reply. We measure it by recording both voices on one timeline, finding the end of the user's speech and the start of the agent's speech, and subtracting the two.

In this blog, we will learn about how the voice-to-voice latency of a voice agent gets measured. We will also see where the time goes inside a voice agent, why the server logs give the wrong answer, how a two-channel recording gives the right answer, how we automate it over many calls, why we look at percentiles instead of the average, and where it works well and where it fails.

We will cover the following:

- What is voice-to-voice latency?
- Why is this latency important?
- Where does the time go?
- Approach 1: Using the logs on the server
- Approach 2: Adding timestamps at every step
- Approach 3: Recording the call on one timeline
- Automating the measurement over many calls
- Why do we look at percentiles and not the average?
- Where it works well and where it fails

Let's get started.

## What is voice-to-voice latency?

A **[voice agent](https://outcomeschool.com/blog/design-a-real-time-voice-ai-agent)** is an AI system that we talk to with our voice, and it talks back to us with its voice. A support agent on a phone call is a good example.

**Latency** is the waiting time between an action and its result.

**Voice-to-voice latency is the time from the moment the user stops speaking to the moment the user hears the first sound of the agent's reply.**

The best way to learn this is by taking an example.

Let's say we call a pizza shop voice agent and say:

```
"I want one large cheese pizza."
```

We finish the word "pizza" and go quiet. Then we wait. After some time, we hear the agent say "Sure, one large cheese pizza."

The silent gap between the end of our word "pizza" and the first sound of "Sure" is the voice-to-voice latency.

```
User speaking:   [I want one large cheese pizza.]
                                                 |<-- gap -->|
Agent speaking:                                              [Sure, one large...]
```

Here, we can notice two things:

- The start point is the end of the user's voice, not the moment the agent decided the user was done.
- The end point is the first sound that reaches the user's ear, not the moment the agent created the reply. We count only up to the first sound, because [the user stops waiting as soon as the agent starts speaking](https://outcomeschool.com/blog/time-to-first-audio).

If we pick the wrong start point or the wrong end point, we get a wrong number. We will see this in detail.

## Why is this latency important?

When two humans talk, the gap between one person finishing and the other person starting is very short. A well-known study on conversations across ten languages found that this gap is often only about 200 milliseconds, which is one-fifth of a second.

So, our brain expects a quick reply from a voice agent too.

When a voice agent takes too long, the user starts to feel that something is wrong. The user says "Hello?", or starts speaking again, and now both are talking at the same time. The conversation breaks.

Hence, teams building voice agents watch this number closely. And, in order to improve a number, we must first measure it correctly.

## Where does the time go?

Before jumping into the measurement, we must know what happens inside a voice agent between the end of our voice and the start of its reply.

A common voice agent works like a [chain of steps](https://outcomeschool.com/blog/cascaded-vs-speech-to-speech):

- **Speech-to-Text (STT)**: It converts our voice into text.
- **LLM (Large Language Model)**: It reads the text and writes the reply text.
- **Text-to-Speech (TTS)**: It converts the reply text into voice.

But, the time is not spent only in these three steps. Let's see the full journey of one turn, with some example numbers just for the sake of understanding:

```
User stops speaking
        ↓
Audio travels from the phone to the server           50 ms
        ↓
Agent waits in silence to be sure the user is done   500 ms
        ↓
STT gives the final text                             100 ms
        ↓
LLM gives the first part of the reply                300 ms
        ↓
TTS gives the first piece of audio                   150 ms
        ↓
Audio travels from the server to the phone           50 ms
        ↓
Phone buffers the audio before playing it            50 ms
        ↓
User hears the first sound
```

Total = 50 + 500 + 100 + 300 + 150 + 50 + 50 = 1200 milliseconds.

Here, we can see that the voice-to-voice latency is the sum of all these steps, not just the AI models.

We have a detailed blog on [how to build a latency budget for a voice AI agent](https://outcomeschool.com/blog/voice-agent-latency-budget) that explains how to split this total across every step.

Two steps here need a little explanation.

**The silence wait:** The agent cannot know the user is done the moment the voice stops. The user can be taking a breath. So, the agent waits for some silence before it decides the turn is over. This decision is called **[endpointing](https://outcomeschool.com/blog/what-is-turn-taking-in-a-voice-ai-agent)**. This wait is often one of the biggest parts of the total, and it is also the part that a wrong measurement misses most easily.

**The buffer on the phone:** Audio comes over the internet in small pieces, and the pieces do not arrive at a perfectly even speed. So, the phone keeps a few pieces in a small waiting area before it plays them, so that the sound does not break. This waiting area is called a **jitter buffer**. It adds a little delay.

Now, the question is: how do we measure this total correctly? Let's see the approaches one by one.

## Approach 1: Using the logs on the server

Our server already writes logs. So, the first idea is to use them.

The server writes a log line when the agent decides the user is done. Then, it writes a log line when the first piece of reply audio leaves the server.

```
10:15:02.300  End of user turn detected
10:15:02.850  First reply audio sent
```

Here, the difference is 550 milliseconds. It looks good.

But, this number is wrong. Let's see why.

- The log starts the clock when the agent decided the user was done, not when the user actually stopped speaking. So, the silence wait of 500 ms is not counted. Also, the 50 ms the audio took to reach the server is not counted.
- The log stops the clock when the audio leaves the server, not when the user hears it. So, the 50 ms on the way back and the 50 ms in the phone buffer are not counted.

In our example, the real latency is 1200 ms, but the server log says 550 ms. Means, the server log hides more than half of the waiting time.

The issue with this approach is that it measures only the part of the journey that happens inside the server. Let's see how the next approach solve this issue.

## Approach 2: Adding timestamps at every step

Now, we can [add a timestamp at every step of the journey](https://outcomeschool.com/blog/ai-agent-observability), including on the user's phone.

The phone writes the time when the user's voice ends. The server writes the time at every step. The phone again writes the time when the first reply sound plays.

This approach is useful for one thing. It tells us how much time each step takes. If the LLM suddenly becomes slow, we can see it at once.

But, there is a problem. The phone and the server have two different clocks. These clocks are never perfectly in sync. The phone clock can be ahead or behind the server clock by tens of milliseconds, or even more.

Let's say the phone clock is 80 ms ahead of the server clock. When we subtract a phone time from a server time to find how long a step took, we get an error of 80 ms in our result, and the result does not show this error.

There is one more problem. Even the total, which uses only the two phone times, is not exact.

- "When the user's voice ends" is not easy for the phone to know exactly. The phone must use its own silence detector, and it marks the end a little late or a little early.
- "When the first reply sound plays" is also not exact. The app writes the time when it hands the audio to the speaker, but the audio system of the phone adds its own small delay before the sound actually comes out.

The issue with this approach is that the per-step timestamps come from different clocks, and the start and end points of the total are still not exact. Let's see how the next approach solve this issue.

## Approach 3: Recording the call on one timeline

Here comes the **two-channel recording** into the picture.

The idea is to record the whole conversation, the way the user hears it, into one audio file with two channels.

- The **left channel** has the user's voice.
- The **right channel** has the agent's voice, exactly as it is played on the user's side.

Now, both voices are on the same timeline, recorded by the same clock. So, there is no difference between two clocks.

```
Left  (user):   ~~~~~~~~~~~~~~~~~~~~~~~______________________________
Right (agent):  _____________________________________~~~~~~~~~~~~~~~~
                                       ^             ^
                                 user stops     agent starts
```

Here, `~` means sound and `_` means silence.

Now, the measurement is simple:

**Step 1:** Find the moment where the user's voice ends on the left channel.

**Step 2:** Find the moment where the agent's voice starts on the right channel.

**Step 3:** Subtract the first moment from the second moment.

Let's say the user's voice ends at 4.20 seconds in the file and the agent's voice starts at 5.40 seconds. Then the voice-to-voice latency is 5.40 - 4.20 = 1.20 seconds, which is 1200 milliseconds.

One more thing to notice. We measure on the recording after the call is over. So, we can look at the audio both before and after any moment. We do not need to wait in silence to be sure the user is done, like the agent did during the live call. We can find where the user's voice really ended much more accurately.

This approach captures every part of the journey:

- The travel time in both directions.
- The silence wait.
- The time taken by all the AI models.
- The buffer on the phone.

That's why this approach gives the measurement that is closest to what the user experiences.

In practice, teams get this recording in two ways. They record the call on the user's device. Or, they place a test call from a computer that plays a recorded user voice into the call and records what comes back. Then, they open the recording in an audio editor and read the gap by eye on the sound waves.

Looking by eye works for a few calls. But, we cannot do this for thousands of turns. Now, let's automate it.

## Automating the measurement over many calls

To automate it, we need a program that can tell where speech is present and where it is silent. Such a program is called a **Voice Activity Detector (VAD)**. It looks at small pieces of audio, for example 20 milliseconds each, and says "speech" or "no speech" for each piece. The silence detectors we saw earlier are also VADs.

We run the VAD on each channel separately. Then, for every turn, we find the end of the user's speech and the start of the agent's next speech.

We can write the code as below:

```python
def measure_latencies(user_speech, agent_speech):
    # user_speech and agent_speech are lists of (start, end) times in seconds
    latencies = []
    for user_start, user_end in user_speech:
        # find the first agent speech that starts after the user stopped
        for agent_start, agent_end in agent_speech:
            if agent_start > user_end:
                latencies.append(round(agent_start - user_end, 2))
                break
    return latencies
```

Here, we have:

- `user_speech`: the list of speech segments that the VAD found on the left channel.
- `agent_speech`: the list of speech segments that the VAD found on the right channel.
- For each user segment, we search for the first agent segment that starts after the user ends.
- The difference between the two is the voice-to-voice latency for that turn.

Let's say the VAD gives us this:

```python
user_speech = [(0.5, 2.1), (6.0, 8.3)]
agent_speech = [(3.0, 5.2), (9.1, 11.0)]
print(measure_latencies(user_speech, agent_speech))
```

It will print the following:

```
[0.9, 0.8]
```

So, the first turn took 900 ms and the second turn took 800 ms.

This code is kept simple. A real version must handle a few more cases. The user can pause in the middle of a sentence, so two user segments with a short gap must be joined into one turn. The user can also [interrupt the agent](https://outcomeschool.com/blog/what-is-barge-in-in-a-voice-ai-agent), and such turns must be skipped, because there is no clean gap to measure.

Now, we can run this on hundreds of test calls every day and get a large list of latency numbers.

## Why do we look at percentiles and not the average?

Now, we have many numbers. The next big question is: how do we summarize them into one number?

The first idea is the average. But, the average mixes the fast turns and the slow turns into one number that describes neither of them well.

Let's say we measure 10 turns and get these numbers in milliseconds, sorted from small to big:

```
700, 750, 800, 800, 850, 900, 950, 1000, 1100, 2400
```

The average is 10250 / 10 = 1025 ms.

But, look at the numbers. Most of the turns are at or below 1000 ms, so the average makes the normal turn look slower than it is. At the same time, the last turn took 2400 ms. That user waited almost two and a half seconds in silence, and the average does not tell us about this user at all.

So, we use the **percentile**.

**A percentile tells us the value below which a given percentage of our measurements fall.**

- **p50** (also called the median): half of the turns are faster than this. Here, the two middle values are 850 and 900, so p50 = (850 + 900) / 2 = 875 ms.
- **p90**: 90 percent of the turns are this fast or faster. Here, 9 out of 10 turns are at or below 1100 ms, so p90 = 1100 ms.
- **p95** and **p99**: the same idea for 95 percent and 99 percent. We need many more turns to calculate them reliably.

The p50 tells us the typical experience. The p90, p95, and p99 tell us how slow the slowest turns are. In real testing, we measure thousands of turns, so the p95 and p99 show us turns like the 2400 ms one clearly.

A voice agent with a good p50 but a very bad p99 still makes some users feel ignored. Hence, teams track the p50 along with a high percentile like p95, and they try to bring both down.

## Where it works well and where it fails

**Where it works well:**

- The two-channel recording measures what the user experiences, from the end of the user's voice to the first sound in the user's ear.
- It uses one clock, so there is no error from clocks that are not in sync.
- It works the same way for any voice agent, whether it uses separate STT, LLM, and TTS steps or one single speech-to-speech model.
- When we combine it with the timestamps from Approach 2, we get both the true total and the time taken by each step.

**Where it fails:**

- The VAD itself is not perfect. A soft last word or a breath at the end can move the detected end point by tens of milliseconds.
- Background noise on the user's channel can look like speech, and this creates wrong measurements.
- If the agent starts with a short filler sound like "Hmm" before the real answer, we must decide which sound counts as the start of the reply.
- Test calls from a computer usually run on a clean network. Many real users call from weak mobile networks, so the real numbers are often worse than the test numbers.

Now we must have understood how the voice-to-voice latency of a voice agent gets measured, where the time goes, and why we look at percentiles over many turns.

## Frequently Asked Questions

### Where does the clock start and stop for voice-to-voice latency?

The clock starts at the end of the user's voice, not at the moment the agent decides the user is done. It stops at the first sound of the reply that reaches the user's ear, not at the moment the agent creates the reply. If we pick the wrong start point or the wrong end point, we get a wrong number.

### Which part of a voice agent adds the most latency?

The silence wait is often one of the biggest parts of the total. The agent cannot know the user is done the moment the voice stops, because the user can be taking a breath, so it waits for some silence first. This wait is also the part that a wrong measurement misses most easily.

### Can we use one clock on the phone and another on the server?

Not for exact results. The phone and the server have two different clocks that are never perfectly in sync, and they can differ by tens of milliseconds or more. When we subtract a phone time from a server time, the result carries this error without showing it. A two-channel recording avoids the problem by using one clock.

### Is a two-channel recording useful for a speech-to-speech model?

Yes. The two-channel recording works the same way for any voice agent, whether it uses separate STT, LLM, and TTS steps or one single speech-to-speech model. It only looks at the end of the user's voice and the start of the agent's voice on one timeline.

### Why are test call numbers often better than real user numbers?

Test calls from a computer usually run on a clean network. Many real users call from weak mobile networks, so the real numbers are often worse than the test numbers.
