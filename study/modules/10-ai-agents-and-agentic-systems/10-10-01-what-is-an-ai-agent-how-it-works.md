---
title: What is an AI Agent? How It Works
module: 10
module_title: AI Agents and Agentic Systems
lesson: '10.1'
source: https://outcomeschool.com/blog/ai-agent
published: April 27, 2026
tags:
- ai-agent
- llm
- ai
- machine-learning
videos:
- title: 'AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization'
  url: https://www.youtube.com/watch?v=lnfWvX66FUk
fetched: '2026-10-24'
words: 3980
reading_time: 20
status: full
---
# What is an AI Agent? How It Works

> **Module 10 · Lesson 10.1**  
> Source: [Outcome School](https://outcomeschool.com/blog/ai-agent) · Published: April 27, 2026 · Reading time: ~20 min · Tags: `ai-agent`, `llm`, `ai`, `machine-learning`
> Video: [AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization](https://www.youtube.com/watch?v=lnfWvX66FUk)

---

![AI Agent](../../assets/images/10-10-01-what-is-an-ai-agent-how-it-works/ai-agent.png)

An AI Agent is a system where an LLM takes a goal from us, decides the steps, uses tools, and keeps working until the goal is done.

In this blog, we will learn about the AI Agent. We will also see how it is different from a plain LLM, its five core parts, how it works end to end, the main types, and when to use one.

We will cover the following:

- The Big Picture
- What is an AI Agent?
- AI Agent vs Plain LLM vs Chatbot
- The Five Core Parts
- How an AI Agent Works End to End
- A Concrete Example: Research Agent
- Types of AI Agents
- What AI Agents Can Do Today
- When to Use an AI Agent
- Common Failure Modes
- Quick Summary

Let's get started.

## The Big Picture

Before we go into the details, let's understand the big picture.

An **AI Agent** is a system that can take a goal from us, figure out the steps to achieve it, use tools when needed, and keep working until the goal is done. It is not just an LLM that answers one question. It is an LLM wrapped in [a loop](https://outcomeschool.com/blog/ai-agent-loop), with tools and memory, so it can actually get things done.

In simple words:

**AI Agent = An LLM + Instructions + Tools + Memory + A loop that runs until the goal is achieved.**

Think of an AI Agent like a new intern on their first day. They do not do the whole job in one go. They read the task, think about what to do first, use a tool (open a file, send a message, run a query), check the result, and decide the next step. They repeat this until the job is done. An AI Agent does the same thing - just faster and without breaks. Same shape of work. Different speed.

## What is an AI Agent?

**An AI Agent is a software system that uses an LLM to decide what to do, takes actions using tools, and keeps working in a loop until the goal is achieved.**

Now that we have the big picture, let's decompose the term itself.

**AI Agent = AI + Agent**

**AI** means the reasoning engine - almost always an LLM like Claude, GPT, or Gemini. **Agent** means something that can act on its own - that can perceive the world, decide what to do, and take actions to reach a goal.

Put these two together, and we get a software system where the **LLM is the decision-maker**. It does not just generate text. It decides what action to take, picks the right tool, reads the result that the loop feeds back, and plans the next move. A plain LLM gives us one answer and stops. An AI Agent keeps going - thinking, acting, observing, and thinking again - until the goal is reached.

So, here the AI Agent comes into the picture whenever a task is too big to solve in a single LLM call.

## AI Agent vs Plain LLM vs Chatbot

There is a lot of confusion between these three. Let's clear it up.

**Plain LLM.** One request, one response. We send a prompt, we get text back. Nothing else happens.

**Chatbot.** A plain LLM with a memory of the current conversation. We can chat back and forth. In its classic form, each response is just text. It does not take real-world actions on its own.

**AI Agent.** A chatbot that can also use tools and run in a loop to complete tasks - or an LLM running in the background with the same setup, no chat surface needed. The defining property is tool use plus the loop, not the chat UI. It does not just talk - it can search the web, run code, send emails, update databases, and anything else we give it access to.

In simple words:

**Plain LLM talks once. Chatbot talks many times. AI Agent talks AND acts, many times, until the task is done.**

**Note:** Today, the line between a chatbot and an agent is blurring - once a chatbot gains tools and a loop, it becomes an agent. Products like ChatGPT and Claude.ai have already crossed that line.

That one difference - the ability to take actions and run in a loop - is what separates an AI Agent from a plain LLM or a classic chatbot.

## The Five Core Parts

Now, let's zoom in. Every AI Agent, no matter how complex, has the same five core parts. Let's decode each one.

```
+------------------------------------------------+
|                      Loop                      |
|                                                |
|   Instructions --->  +-------+                 |
|                      |       |                 |
|   Memory       --->  |  LLM  | <-----+         |
|                      +-------+       |         |
|                          |           |         |
|                          | pick      | result  |
|                          v           |         |
|                      +-------+       |         |
|                      | Tools | ------+         |
|                      +-------+                 |
+------------------------------------------------+
```

**1. The LLM (the brain).** This is the reasoning engine. It reads the current situation and decides the next action - either pick a tool for the loop to call, or return a final answer. Every meaningful decision in the agent goes through the LLM. The LLM does not call tools itself - it only recommends which tool to use and what inputs to pass. The loop is the one that actually calls the tool.

**2. The Instructions (the system prompt).** This tells the LLM what its job is, what tools it has, and what rules to follow. Without good instructions, the agent is confused. With good instructions, the agent knows exactly what to do. Long procedures do not have to sit here permanently either - [Agent Skills](https://outcomeschool.com/blog/what-are-agent-skills) keep each one in its own folder, and the agent loads it only when the task needs it.

**3. The Tools (the hands).** These are the actions the agent can take - search, calculate, read files, call APIs, send emails, run code. Each tool has a **name**, a **description**, and an **input schema**.

Here is what a tool definition looks like in practice, as below:

```json
{
  "name": "web_search",
  "description": "Search the web for pages matching the query. Use this tool when the user asks for current information, news, or anything not available in the model's training data.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search query to run."
      },
      "max_results": {
        "type": "integer",
        "description": "Maximum number of results to return. Default is 5."
      }
    },
    "required": ["query"]
  }
}
```

Here, the LLM reads the `name` to identify the tool, the `description` to decide **when** to use it, and the `input_schema` to know **what arguments** to pass and in what format. The `description` is the most important field - every word matters, because this is what the LLM uses to pick between tools. A vague description leads to the wrong tool being picked. A precise description leads to the right one.

These tool definitions do not have to be hand-written for every application either. An open standard called MCP lets a server describe its own tools, so an agent can discover them the moment it connects. We have a detailed blog on [What is MCP (Model Context Protocol)?](https://outcomeschool.com/blog/what-is-mcp-model-context-protocol) that covers this end to end.

**4. The [Memory](https://outcomeschool.com/blog/ai-agent-memory).** This is what lets the agent keep track of progress and avoid repeating work. There are two kinds. **Short-term memory** is the conversation history of the current run - every prompt, [tool call](https://outcomeschool.com/blog/how-does-function-calling-work-in-llms), and observation so far. It lives in the runtime, and the full history is fed back to the LLM on every call, because the LLM itself is stateless. **Long-term memory** is anything we want the agent to remember across runs - user preferences, past decisions, learned facts. It lives in an external store like a [vector database](https://outcomeschool.com/blog/how-does-a-vector-database-work) or a user profile, and the agent retrieves from it when needed.

**5. The Loop (the runtime).** This is the code that keeps the agent going. Send prompt to LLM. Read the LLM's response. If the LLM picked a tool, run that tool. Feed the result back. Repeat until the LLM says "done." The loop is what makes it an agent, not just a chatbot. The loop is also where tool calls actually happen - the LLM only decides which tool to use. Shaping this loop on purpose - the step budget, the checks, and the exits - is [Loop Engineering](https://outcomeschool.com/blog/what-is-loop-engineering).

Going back to our intern analogy - the LLM is the intern's brain, the Instructions are the job description the manager handed over, the Tools are the laptop and email and office systems they can use, the Memory is the notebook where they track progress, and the Loop is the workday itself that keeps them going from one task to the next.

All five parts work together. Remove any one, and it is no longer an AI Agent. Hence, every real AI Agent, from a simple chatbot-with-tools to an autonomous coding assistant, has all five.

## How an AI Agent Works End to End

Now, let's put all the parts together to see how an AI Agent actually runs.

Here is the shape of the loop:

```
   +----------------+
   |  User's Goal   |
   +----------------+
            |
            v
   +----------------+        +-------------+
   |      LLM       |------->|    Tool     |
   |  (decides:     |        +-------------+
   |   pick a tool  |              |
   |   or return    |              v
   |   final answer)|        +-------------+
   |                |<-------| Observation |
   +----------------+        +-------------+
            |
            | when goal is achieved
            v
   +----------------+
   |  Final Answer  |
   +----------------+
```

The goal comes in at the top. The LLM looks at it and decides one of two things - which tool the loop should call next, or the final answer directly. When the LLM picks a tool, the loop runs it and produces an observation, which is fed back to the LLM. The LLM then decides again. This little loop between the LLM, the Tool, and the Observation keeps running until the LLM decides the goal is achieved and returns the final answer.

Here is what happens on every request:

**Step 1:** The user gives the agent a goal - for example, "Find me the 3 cheapest direct flights to Delhi tomorrow under 8000 rupees."

**Step 2:** The Loop sends the goal, the instructions, and any memory to the LLM.

**Step 3:** The LLM thinks and decides the next action. For example, "First I need to search for flights."

**Step 4:** The Loop runs the tool the LLM asked for (the flight search tool).

**Step 5:** The tool returns a result. The Loop feeds it back to the LLM as an observation.

**Step 6:** The LLM reads the observation and decides the next action. Maybe filter by price. Maybe pick the top 3 cheapest.

**Step 7:** The Loop runs the next tool. The cycle repeats.

**Step 8:** When the LLM decides the goal is achieved, it returns a final answer to the user - "Done. Here are the 3 cheapest direct flights - AI-123 at 6500 rupees, IX-201 at 7200 rupees, and SG-312 at 7800 rupees."

**Note:** Modern LLMs like Claude and GPT can output multiple tool calls in a single step, and a real runtime can run them in parallel to save time. The shape of the loop stays the same - the LLM decides, the tools run, the observations feed back - just with more than one action per turn when the LLM chooses to.

The whole thing is a loop. The LLM is the decision-maker. The tools are the hands. The memory holds the progress. The loop keeps it all going.

That's the beauty of an AI Agent. Every decision comes from the LLM. Every action is executed by the tools. The loop keeps them going together until the job is done. The flow is not hardcoded - the agent figures it out as it goes.

## A Concrete Example: Research Agent

The best way to learn this is by taking an example.

Suppose we tell an agent: "Research the best laptop for video editing under $1500."

This is a Research Agent. Let's see what it does behind the scenes.

The agent uses these tools:

- A web search tool - to find pages about laptops and software
- A web page reader - to read reviews, specs, and prices
- A calculator - to compare numbers like RAM, storage, and price

The agent makes decisions:

- Which laptops to investigate
- What factors matter most - RAM, GPU, storage
- Which sources are trustworthy

The agent takes multiple actions:

- Searches for "best video editing laptops 2026" (the LLM decides to start with a broad search)
- Reads the top results (the LLM picks which pages are worth opening)
- Compares the specs of 5 laptops (the LLM extracts the factors that matter)
- Checks prices on Amazon (the LLM verifies the budget constraint)
- Reads user reviews (the LLM weighs real-world quality signals)
- Creates a summary with pros and cons (the LLM drafts the shortlist)
- Returns the top 3 recommendations with reasons (the LLM produces the final answer)

Here, the LLM is the decision-maker. The tools are the hands. The loop keeps it running until the final report is ready. Same five parts we decoded earlier, just wired for a real task.

Now, here is the important realization:

**If we write code that takes the input, sends it to an LLM, executes the actions, and repeats this loop until the task is complete - our piece of code is an AI Agent.**

That is all an AI Agent is. No magic. No black box. Just a loop, an LLM, some tools, and memory - all wired together in code.

Let's see what this looks like in real Python code, as below. Here, `call_llm` is any function that sends the messages and the list of tools to the LLM of our choice - Claude, GPT, Gemini, or any other - and returns its response. And `call_tool` is any function that runs a tool by name with the given arguments and returns the result. The code below is independent of any specific provider.

```python
async def run_agent(user_goal, tools, max_steps=10):
    messages = [{"role": "user", "content": user_goal}]
    step = 0
    while True:
        # Safety stop: bail out if we hit the step limit
        if step >= max_steps:
            return "Reached step limit without completing the task."
        step += 1
        # Ask the LLM what to do next
        response = await call_llm(messages, tools)
        # If the LLM says "I am done", stop the loop and return the final answer
        if response.is_done:
            return response.final_answer
        # Otherwise, run each tool the LLM picked and feed the result back
        for tool_call in response.tool_calls:
            result = await call_tool(tool_call.name, tool_call.arguments)
            messages.append({
                "role": "tool",
                "name": tool_call.name,
                "content": str(result),
            })
```

Here, we have the entire AI Agent in about 20 lines of Python. Let's walk through the important parts:

- **The `while True` loop.** This is the runtime of the agent. It keeps going until either the LLM says it is done or we hit the step limit.
- **The step limit.** We bail out after `max_steps` iterations. This protects us from infinite loops - one of the most common failure modes.
- **The LLM call.** We send the full conversation history along with the list of tools. The `await` is what makes this asynchronous - while the LLM is thinking, our program can do other work.
- **The stop check.** If `response.is_done` is `True`, the LLM is telling us **"I am done, here is the final answer."** We return that answer and exit the loop.
- **The tool-call branch.** If the LLM picked one or more tools, we run each one with `call_tool` using the arguments the LLM gave, and feed the result back to the LLM on the next turn.

That is the complete skeleton of an AI Agent - a `while` loop, an LLM call inside it, a check for the stop signal, and a tool-call branch that feeds results back. Everything else we add on top - memory, parallel tool calls, retries, logging - is polish around this core loop.

## Types of AI Agents

Not all AI Agents look the same. Here are the main types we will see in practice. Each one is the same five core parts, just wired a little differently.

**[ReAct Agent](https://outcomeschool.com/blog/react-agent).** The agent alternates between Thought, Action, and Observation at every step. The most common pattern.

**[Plan-and-Execute Agent](https://outcomeschool.com/blog/plan-and-execute-agent).** The agent first creates a complete plan, then executes each step one by one. Good for long tasks.

**[Reflection Agent](https://outcomeschool.com/blog/reflection-agent).** The agent writes a draft, critiques its own work, and revises. Good when quality matters more than speed.

**[Agentic RAG](https://outcomeschool.com/blog/agentic-rag).** The agent decides when and how to retrieve documents, then uses them to answer. Good for knowledge-heavy tasks.

**[Multi-Agent System](https://outcomeschool.com/blog/multi-agent-systems).** Several agents with different roles work together. One researches, another writes, another reviews.

**Note:** These are not mutually exclusive. A real system often combines patterns - for example, a ReAct agent that uses Agentic RAG for knowledge lookups, with a Reflection step at the end for quality.

## What AI Agents Can Do Today

Let's look at some real things AI Agents are doing right now. This is not theory - these are in production.

**Coding agents.** Read a repository, understand the code, make changes, run tests, and submit a pull request. Examples: [Claude Code](https://outcomeschool.com/blog/how-does-claude-code-work), [Cursor](https://outcomeschool.com/blog/how-does-cursor-work), GitHub Copilot agent mode.

**Research agents.** Search the web, read papers, synthesize findings, and produce a structured report. Examples: OpenAI Deep Research, Perplexity, Gemini Deep Research.

**Customer support agents.** Read a ticket, look up the user's account, check order status, and reply with a fix - with handoff to a human when needed.

**[Browser agents](https://outcomeschool.com/blog/how-do-browser-agents-work).** Open a browser, navigate websites, fill forms, and complete tasks like booking or purchasing. Examples: Claude Code ([Computer Use](https://outcomeschool.com/blog/how-do-computer-use-agents-work) is now in Claude Code), ChatGPT Agent.

**Data analysis agents.** Query databases, run calculations, create charts, and summarize the findings. Examples: ChatGPT data analysis, Claude's code execution. These agents also need to know what our tables actually mean, otherwise they guess, and OKF is an open standard for writing that knowledge down in files an agent can read. We have a detailed blog on [What is OKF (Open Knowledge Format)?](https://outcomeschool.com/blog/what-is-okf-open-knowledge-format) that explains this in depth.

**Personal assistants.** Manage calendar, read and draft emails, search files, and complete multi-step tasks on the user's behalf. Examples: Apple Intelligence, Google Gemini assistant.

Every one of these is the same five-part structure. Only the tools and instructions change. Once we understand the five parts, we understand all AI Agents.

## When to Use an AI Agent

Now, a natural question arises - when should we actually build an AI Agent, and when is a simpler tool the better choice?

**Use an AI Agent when:**

- The task needs more than one step to complete.
- The next step depends on the result of the current step.
- The task needs external information or real-world actions (not just knowledge from the model).
- The path is not fixed - the agent has to decide what to do as it goes.

**Do not use an AI Agent when:**

- A single LLM call can solve the task (like summarizing a paragraph).
- The task is a fixed pipeline with no branching - a regular script is simpler.
- Latency and cost matter more than flexibility, and the task is simple.
- We cannot tolerate the non-determinism that comes with LLM decisions.

The rule of thumb is simple: if the task needs decisions and actions that depend on each other, an AI Agent is the right tool. If not, stick with a plain LLM call or a script. Using an agent when a script would do is over-engineering.

## Common Failure Modes

AI Agents are powerful, but they fail in specific ways. Knowing these failures helps us build more reliable agents. Let's decode each one.

**1. Infinite loops.** The agent keeps calling the same tool and never produces a final answer.

**How to fix:** Set a hard limit on the number of steps.

**2. Wrong tool selection.** The agent picks the wrong tool for the job.

**How to fix:** Write very clear tool descriptions. Every word in the description matters.

**3. Hallucinated actions.** The LLM picks a tool that does not exist or passes invalid arguments.

**How to fix:** Use native tool-use support from the LLM, and validate inputs in the loop before running the tool. Return a clear error as an observation if the input is invalid so the agent can self-correct.

**4. Context overflow.** The conversation history grows too large and no longer fits in the model's context window.

**How to fix:** [Summarize older steps](https://outcomeschool.com/blog/how-does-context-compaction-work) or drop stale observations, and keep the goal at the start and the newest steps at the end so that nothing important gets [lost in the middle](https://outcomeschool.com/blog/lost-in-the-middle-problem-in-llms).

**5. Premature stopping.** The agent gives up before finishing the task.

**How to fix:** Make the instructions clear about when the task is truly complete.

**Very important:** Production-grade AI Agents are mostly about handling these failure modes well. The happy path is easy. The edge cases are where the real engineering happens. We have a detailed blog on [AI Agent Evaluation](https://outcomeschool.com/blog/ai-agent-evaluation) that explains how to systematically measure outcome, trajectory, and tool use for AI Agents.

Now, we have understood what an AI Agent is, how it works, and when to use one. Let's wrap up with a quick recap.

## Quick Summary

Let's recap what we have decoded:

- **AI Agent = LLM + Instructions + Tools + Memory + Loop.** The LLM is the decision-maker. The tools are the hands. The loop keeps it going until the goal is done.
- **Not just a chatbot.** An AI Agent talks AND acts. It takes real actions, not just produces text.
- **Five core parts.** LLM, Instructions, Tools, Memory, Loop. Remove any one, and it is no longer an AI Agent.
- **End-to-end flow.** The loop sends the prompt to the LLM -> if the LLM picks a tool, the loop runs it and feeds the result back -> if the LLM returns a final answer, the loop stops. Repeat until done.
- **Types.** ReAct, Plan-and-Execute, Reflection, Agentic RAG, and Multi-Agent Systems. Real systems often combine them.
- **Use cases today.** Coding, research, customer support, browsing, data analysis, personal assistance. Same five-part structure everywhere.
- **When to use one.** The task needs multiple steps, tool use, and adaptive decisions. Otherwise, stick with a plain LLM call or a script.
- **Failure modes.** Infinite loops, wrong tool selection, hallucinated actions, context overflow, premature stopping. Handling these is the real work.

AI Agents bring dynamic, goal-driven control flow into mainstream software - the program decides its own next step instead of following a fixed script. That is what makes them powerful, and what makes them hard. Every serious AI application going forward is moving in this direction.

## Frequently Asked Questions

### Is ChatGPT an AI Agent?

Yes, in its current form. The line between a chatbot and an agent is blurring, because once a chatbot gains tools and a loop, it becomes an agent. Products like ChatGPT and Claude.ai have already crossed that line.

### Does an AI Agent need a chat interface?

No. The defining property of an AI Agent is tool use plus the loop, not the chat UI. An LLM running in the background with the same setup of instructions, tools, memory, and a loop is also an AI Agent, with no chat surface needed.

### Which part of a tool definition matters most for an AI Agent?

The description matters most. The LLM reads the name to identify the tool, the description to decide when to use it, and the input schema to know what arguments to pass. A vague description leads to the wrong tool being picked, while a precise one leads to the right tool.

### Can we combine different types of AI Agents in one system?

Yes. The agent types are not mutually exclusive. A real system often combines patterns, for example a ReAct agent that uses Agentic RAG for knowledge lookups, with a Reflection step at the end for quality.

### What should an AI Agent do when the LLM passes invalid tool arguments?

The loop should validate the inputs before running the tool. If the input is invalid, it returns a clear error as an observation so the agent can self-correct. Using native tool-use support from the LLM also helps avoid these hallucinated actions.
