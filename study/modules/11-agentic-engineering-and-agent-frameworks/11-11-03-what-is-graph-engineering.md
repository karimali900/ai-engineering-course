---
title: What is Graph Engineering?
module: 11
module_title: Agentic Engineering and Agent Frameworks
lesson: '11.3'
source: https://outcomeschool.com/blog/what-is-graph-engineering
published: August 21, 2026
tags:
- ai-agent
- llm
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 4897
reading_time: 24
status: full
---
# What is Graph Engineering?

> **Module 11 · Lesson 11.3**  
> Source: [Outcome School](https://outcomeschool.com/blog/what-is-graph-engineering) · Published: August 21, 2026 · Reading time: ~24 min · Tags: `ai-agent`, `llm`, `ai`, `system-design`

---

![What is Graph Engineering?](../../assets/images/11-11-03-what-is-graph-engineering/what-is-graph-engineering.png)

Graph Engineering is the practice of designing an AI system as a graph, where every step of the work is a node, and every path from one step to another is an edge. We break the work into small steps and clearly decide which step runs after which.

In this blog, we will learn about Graph Engineering, the practice of building an AI system as a graph of small steps connected by clear paths instead of one giant prompt or one endless loop. We will also see why we need it, what nodes and edges actually mean, how the state travels through the graph, how conditional edges take decisions, how cycles let the system do the work again, how parallel branches save time, how checkpoints let us pause and resume, and where it works well and where it fails.

We will cover the following:

- What is Graph Engineering?
- Graph = Nodes + Edges
- Why do we need Graph Engineering?
- The three building blocks: Node, Edge, and State
- Let's build our first graph
- Conditional edges: taking decisions inside the graph
- Cycles: doing the work again when needed
- One full run, step by step
- Parallel branches: doing many things at the same time
- Checkpoints: pause and resume the graph
- Human in the loop
- Handling errors inside a graph
- Graph Engineering vs Loop Engineering
- Where Graph Engineering works well
- Where Graph Engineering fails
- Best practices in Graph Engineering
- Conclusion

Let's get started.

## What is Graph Engineering?

**Graph Engineering is the practice of designing an AI system as a graph, where every step of the work is a node and every path from one step to another step is an edge.**

Graph Engineering = Graph + Engineering.

In simple words, instead of writing one huge instruction and hoping that the model does everything correctly in one go, we break the work into small steps, and then we clearly decide which step runs after which step.

Here, whenever we say the model, we mean the AI model that reads text and writes text, and whenever we say a [tool](https://outcomeschool.com/blog/how-does-function-calling-work-in-llms), we mean anything outside the model that our system can call, like a search, a database, or an email service.

We hear this word mostly around [AI agents](https://outcomeschool.com/blog/ai-agent) today, and there is a good reason for that. Real work is never one step. Real work is many steps, with going back, waiting, checking, and approving in between. Graph Engineering is how we give that shape to our system.

## Graph = Nodes + Edges

Before jumping into Graph Engineering, we must know what a graph is.

A graph is just two things.

- **Nodes**: the places where something happens.
- **Edges**: the paths that connect one place to another place.

The best way to learn this is by taking an example.

Let's say we are looking at the metro map of a city. Every station on that map is a node. Every track between two stations is an edge. A train starts from one station, travels on a track, reaches the next station, and continues like this until it reaches the last station.

Now, replace the stations with the steps of our work, and replace the tracks with the order of our work. That is exactly the graph we build in Graph Engineering.

| Metro map | Our AI system |
| --- | --- |
| Station | Node, which means one small step of work |
| Track between two stations | Edge, which means the path to the next step |
| Bag that the passenger carries | State, which means the information that travels along |
| First station | The step where our system starts |
| Last station | The step where our system stops |

Here, we can see that an edge is simply the answer to one small question. After this step is over, which step runs next?

Now, we have understood the graph. Now, let's understand why we need Graph Engineering at all.

## Why do we need Graph Engineering?

Let's say we are building a system that answers questions about a company's internal documents. A user asks a question, and our system must give a correct answer with proper sources.

We will build this system step by step. At every step we will see the problem, and then we will move to a better approach.

### Approach 1: One big prompt

We write one long instruction and send it to the model.

```text
You are a helpful assistant. Read the user question. Search the company
documents. Read the results. Write an answer. Check that the answer is
correct. Add the sources. If something is missing, search again.
```

The model reads all of this and tries to do everything at once.

**Problem:** The model does some parts and quietly forgets the other parts. Sometimes it writes the answer without searching. Sometimes it searches but never checks the answer. And when the output is wrong, we have no idea which part went wrong, because everything happened inside one single call. We cannot fix what we cannot see.

The issue with this approach is that there is no structure at all. Let's see how the next approach solve this issue.

### Approach 2: A chain of steps

Now, we break the work into separate calls, and we run them one after another.

```text
Step 1: understand the question
Step 2: search the documents
Step 3: write the answer
Step 4: send the answer
```

This is [prompt chaining](https://outcomeschool.com/blog/how-does-prompt-chaining-work), and it is much better. Every step has only one job. When something goes wrong, we know exactly which step failed.

**Problem:** A chain always moves forward in a straight line. It never comes back. But real work needs coming back. What if the search returns nothing useful? What if the answer is wrong and needs to be written again? A straight chain cannot do this. It simply walks forward and delivers a bad answer.

The issue with this approach is that it cannot go back. Let's see how the next approach solve this issue.

### Approach 3: One loop

Now, we put the whole thing inside an [agent loop](https://outcomeschool.com/blog/ai-agent-loop). The model thinks, calls a tool, looks at the result, and thinks again, again and again, until it decides that the work is done.

This solves the coming back problem. The model can search again, write again, and correct itself.

**Problem:** Now we have gone to the other extreme. Every decision is taken by the model inside one loop, so we have very less control. The model repeats the same failing search ten times. It skips the checking step because it feels confident. It calls a dangerous tool that we never wanted it to call at that moment. The path is different on every run, so testing becomes very hard.

The issue with this approach is that the flow is completely in the model's hands. Let's see how the next approach solve this issue.

### Approach 4: A graph

So, here comes Graph Engineering to the rescue.

We keep the small steps of Approach 2, we keep the coming back ability of Approach 3, and we write down the paths ourselves.

```text
understand  ->  search  ->  write  ->  check
check       ->  send        (when the answer is good)
check       ->  search      (when the sources are missing)
check       ->  write       (when the answer is weak)
```

Here, we can see that every step is small and visible, the system can go back when it needs to, and the model takes decisions only at the places where we allow it to take decisions.

The problem is solved. This is Graph Engineering.

The example we took here, where the system searches, writes, checks, and searches again, is what we call [Agentic RAG](https://outcomeschool.com/blog/agentic-rag), and we have a detailed blog on it that explains this in depth.

## The three building blocks: Node, Edge, and State

Every graph we build has only three parts.

**Node:** A node is one step of the work. It is just a function. It takes the current information, does one small job, and gives the updated information back. A node can call a model, call a tool, hit a database, or run plain code with no model at all.

**Edge:** An edge is a path from one node to another node. It answers only one question. Which node runs next?

**State:** The state is the shared notebook of the graph. Every node reads from this notebook and writes into this notebook. This is how the second node knows what the first node did.

Let's see the state for our document question system as below:

```python
state = {
    "question": "What is our refund policy?",
    "intent": None,
    "documents": [],
    "answer": None,
    "score": None,
    "attempts": 0,
}
```

Here, we have created a simple notebook with empty values. As the graph runs, the nodes will keep filling these values. The `understand` node fills `intent`. The `search` node fills `documents`. The `write` node fills `answer`. The `check` node fills `score` and `attempts`.

This state is the most important design decision in Graph Engineering. If the state is clean, the graph stays simple. If the state becomes a dumping ground of random keys, the graph becomes impossible to understand. Whatever a node puts in front of the model also comes out of this state, so keeping it clean is good [Context Engineering](https://outcomeschool.com/blog/context-engineering) as well.

Now that we have learned about the building blocks, it is time to build a real graph.

## Let's build our first graph

First, we will write the nodes. Every node is a plain function.

```python
def understand(state):
    state["intent"] = model.find_intent(state["question"])
    return state
def search(state):
    state["documents"] = db.search(state["intent"])
    return state
def write(state):
    state["answer"] = model.write_answer(state["question"], state["documents"])
    return state
```

Here, we can notice that each function does exactly one job and returns the updated state. There is no big instruction anywhere. The `understand` node only finds the intent. The `search` node only searches. The `write` node only writes the answer from the documents that the `search` node found.

Then, we will connect these nodes with edges.

```python
graph = Graph(state)
graph.add_node("understand", understand)
graph.add_node("search", search)
graph.add_node("write", write)
graph.add_edge("understand", "search")
graph.add_edge("search", "write")
graph.set_entry("understand")
graph.set_finish("write")
```

Here, we have first added the three nodes to the graph. Then, we have added two edges. The first edge says that after `understand`, the `search` node runs. The second edge says that after `search`, the `write` node runs. Finally, we have told the graph where to start and where to stop.

After this, we can run the graph.

```python
final_state = graph.run(state)
print(final_state["answer"])
```

Here, we are giving the starting notebook to the graph. The graph walks from node to node, each node updates the notebook, and at the end we read the answer from the same notebook.

It works perfectly. But this graph is still a straight line, exactly like Approach 2. Now, let's give it the power to take decisions.

**Note:** The code in this blog is kept simple just for the sake of understanding. The real libraries built for this work give us the same three ideas of node, edge, and state, only with slightly different names. [LangGraph](https://outcomeschool.com/blog/how-does-langgraph-work) is the most popular one of them, and we have a detailed blog on it that explains how it works step by step.

## Conditional edges: taking decisions inside the graph

A normal edge always goes to the same next node. A **conditional edge** looks at the state first and then decides which node runs next.

Let's add a `check` node that gives a score to our answer.

```python
def check(state):
    state["score"] = model.rate_answer(state["answer"], state["documents"])
    state["attempts"] = state["attempts"] + 1
    return state
```

Here, we have used the model as a reviewer, which is the [LLM as a Judge](https://outcomeschool.com/blog/llm-as-a-judge) pattern. It reads the answer along with the documents, and it gives a score out of ten. We are also counting the attempts, and we will see very soon why this count matters so much.

Now, we will write the routing function.

```python
def route_after_check(state):
    if state["score"] >= 8:
        return "send"
    if not state["documents"]:
        return "search"
    return "write"
```

Here, we can see that the decision is plain code, and it is fully in our hands. If the score is good, we go to `send`. If there were no documents at all, we go back to `search`. In every other case, we go back to `write` and try again.

Then, we attach this function as a conditional edge.

```python
graph.add_node("check", check)
graph.add_node("send", send)
graph.add_edge("write", "check")
graph.add_conditional_edge("check", route_after_check)
graph.set_finish("send")
```

We have followed the following steps:

- We have added the `check` node and the `send` node. The `send` node is a small node that simply delivers the final answer to the user.
- We have added a normal edge from `write` to `check`, so every answer goes for review.
- We have added a conditional edge from `check`. This edge has three possible destinations, and our routing function picks one of them by reading the state.
- We have moved the finish point from `write` to `send`, because `send` is the last station of our graph now.

**Note:** The model gave the score, but the model did not choose the path. The path was chosen by our own code. This is the heart of Graph Engineering. We let the model do the thinking, and we keep the control of the flow with ourselves.

## Cycles: doing the work again when needed

In the graph above, `check` can send us back to `write`, and `write` sends us to `check` again. This going back and forth between two nodes is called a **cycle**.

A cycle is a very powerful thing, because this is how a system corrects itself. Write, review, write better, review again. This is exactly how a human works, and this is also the idea behind a [Reflection Agent](https://outcomeschool.com/blog/reflection-agent).

But, here is the catch. A cycle can run forever. If the reviewer never gives a score of eight, our graph will keep writing and checking until our money is over.

So, every cycle must have a stop condition. This is why we were counting the attempts inside the `check` node.

```python
def route_after_check(state):
    if state["score"] >= 8:
        return "send"
    if state["attempts"] >= 3:
        return "ask_human"
    if not state["documents"]:
        return "search"
    return "write"
```

Here, we have added two highlighted lines. After three attempts, the graph stops trying on its own and hands the work over to a human through a new `ask_human` node. We must also add this node to the graph, otherwise the graph will not know where this path goes.

```python
graph.add_node("ask_human", ask_human)
graph.add_edge("ask_human", "send")
```

Here, we have added the `ask_human` node and joined it to `send`, so even this sad path reaches the last station properly.

Our full graph looks like below now:

```text
understand  ->  search  ->  write  ->  check
check       ->  send        (the score is good)
check       ->  ask_human   (three attempts are over)
check       ->  search      (there are no documents)
check       ->  write       (the answer is weak)
ask_human   ->  send
```

Here, we can see the complete shape of our system on one screen. Every step is a node, every line is an edge, and there is no hidden behaviour anywhere.

Our system now fails in a safe and predictable way instead of running forever.

**Very important:** Every cycle in our graph must have a hard limit.

## One full run, step by step

Now, let's walk through one complete run and see what the notebook looks like after every node. This is the best way to feel how a graph really works.

**Step 1:** The user asks a question, so the starting state is:

```text
question: "What is our refund policy?"
intent: None, documents: [], answer: None, score: None, attempts: 0
```

**Step 2:** The `understand` node runs and fills the intent:

```text
intent: "refund policy duration and conditions"
```

**Step 3:** The `search` node runs and fills the documents:

```text
documents: ["policy-v3.pdf", "faq-refunds.md"]
```

**Step 4:** The `write` node runs and fills the answer:

```text
answer: "Refunds are allowed within 30 days."
```

**Step 5:** The `check` node runs. The answer has no sources in it, so the reviewer gives a low score:

```text
score: 5, attempts: 1
```

**Step 6:** The conditional edge reads the state. The score is below eight, the documents are present, and the attempts are below three, so the path goes back to `write`.

**Step 7:** The `write` node runs again, and this time it writes a better answer with sources:

```text
answer: "Refunds are allowed within 30 days of purchase, as per policy-v3.pdf."
```

**Step 8:** The `check` node runs again:

```text
score: 9, attempts: 2
```

**Step 9:** The conditional edge reads the state again. The score is eight or more, so the path goes to `send`, and the graph stops there.

Here, we can notice one beautiful thing. The system found its own mistake and corrected it, and still it never went out of our control, because we had written every path ourselves.

This was all about one single run of our graph. Now, let's see how we can make our graph faster.

## Parallel branches: doing many things at the same time

Sometimes two steps have nothing to do with each other. Searching our internal documents and searching the public web are completely independent. Running them one after another only wastes time.

In a graph, we can send one node to two nodes at the same time.

```python
graph.add_edge("understand", "search_docs")
graph.add_edge("understand", "search_web")
graph.add_edge("search_docs", "merge")
graph.add_edge("search_web", "merge")
```

Here, we can see two things. First, `understand` has two outgoing edges, so both the searches start together. This is called fan-out. Second, both the searches point to the same `merge` node, so the graph waits for both of them to finish and then continues. This is called fan-in.

The `merge` node joins the two results.

```python
def merge(state):
    state["documents"] = state["doc_results"] + state["web_results"]
    return state
```

Here, we have simply joined both the lists into the `documents` key, and the rest of our graph does not even need to know that two searches happened.

Fan-out and fan-in are two of the common patterns that we use to coordinate many steps together. We have a detailed blog on [AI Orchestration](https://outcomeschool.com/blog/ai-orchestration) that covers these patterns end to end.

**Note:** When two nodes run at the same time, they must write into different keys of the state. If both write into the same key, one will silently overwrite the other, and we will spend hours finding that bug.

## Checkpoints: pause and resume the graph

A long graph takes time. It calls models, it calls tools, and it waits for slow services. Now, what happens if our server restarts in the middle of a run? In a simple loop, everything is lost, and the user has to start again from zero.

Here comes **checkpointing** into the picture.

After every node finishes, the graph saves the state. This saved state is called a checkpoint. If something breaks, we load the last checkpoint and continue from that exact node.

```python
graph = Graph(state, checkpointer=Database())
final_state = graph.run(state, thread_id="user-123")
```

Here, we have given a storage to the graph, and we have given an id to this particular run. After every node, the state is saved against this id. If this run breaks after the `search` node, we call `run` again with the same `thread_id`, and the graph starts from `write` instead of starting from `understand`.

This is possible only because the whole progress of our system lives inside one plain state object. This is one more reason why keeping a clean state is so valuable.

Till now, we have learned how a graph runs on its own. Now, it's time to learn about the place where a human joins the graph.

## Human in the loop

Some steps must never happen without a human saying yes. Sending an email to a customer. Issuing a refund. Deleting a record. Pushing code to the live app.

Because our work is divided into nodes, we can simply stop the graph before such a node.

```python
graph.add_node("send_email", send_email, interrupt_before=True)
```

Here, we have marked one node as a stopping point. When the graph reaches `send_email`, it saves the state and pauses. Nothing is sent yet.

Now, a human opens the pending work, reads the draft, and takes a call.

```python
if human_says_yes:
    graph.resume(thread_id="user-123")
else:
    graph.update_state(thread_id="user-123", changes={"answer": edited_answer})
    graph.resume(thread_id="user-123")
```

Here, we can see that the human can either allow the graph to continue, or first correct the answer inside the state and then allow it to continue. The graph does not even know that a human touched it. It just reads the state and moves ahead.

This is how we get the speed of automation with the safety of human review.

## Handling errors inside a graph

Tools fail. Networks fail. Models return broken output. In one big prompt, a failure kills everything. In a graph, a failure is just one node behaving badly, and we can keep it inside the state like any other information.

```python
def search(state):
    try:
        state["documents"] = db.search(state["intent"])
        state["error"] = None
    except Exception:
        state["error"] = "search service is down"
    return state
```

Here, we have caught the failure and written it into the state instead of letting the whole graph crash.

Then, we write a routing function that reads that error and decides what to do.

```python
def route_after_search(state):
    if state["error"]:
        return "search_web"
    if not state["documents"]:
        return "ask_human"
    return "write"
```

Then, we replace the normal edge coming out of `search` with a conditional edge as below:

```python
graph.add_conditional_edge("search", route_after_search)
```

Here, we can notice that a failure is now just a normal path in our graph. When our own search is down, we fall back to the web search. When there is nothing at all to answer from, we ask a human. Nothing crashes, and the user always gets some response.

This is how we build a system that keeps working even on a bad day.

Now that we have learned about the complete graph, it's time to compare it with the other popular way of building AI systems.

## Graph Engineering vs Loop Engineering

[Loop Engineering](https://outcomeschool.com/blog/what-is-loop-engineering) is about one agent thinking in a loop, deciding its own next action, and stopping when it feels that the work is done. Graph Engineering is about many small steps, with the paths between them written down by us.

Let me tabulate the differences between Loop Engineering and Graph Engineering for your better understanding.

| Point | Loop Engineering | Graph Engineering |
| --- | --- | --- |
| Who decides the next step | The model decides | Our code decides, using the model's output |
| Structure | One loop of think and act | Many nodes joined by edges |
| Path on every run | Different every time | Same path for the same situation |
| Testing | Hard, because the path keeps changing | Easy, we can test one node at a time |
| Finding a bug | We read one long history of everything the model did | We look at the one node that failed |
| Freedom for the model | Very high | Only where we allow it |
| Best for | Open ended and unknown tasks | Known work with clear stages |

## Where Graph Engineering works well

- **Work with clear stages.** Support tickets, refund handling, document review, and report writing all have a natural shape of stages.
- **Work that needs approval.** Because we can pause at any node, human review fits in very naturally.
- **Work that must be repeatable.** The same input takes the same path, so we can test it and trust it.
- **Long running work.** Checkpoints let a graph survive restarts and continue for hours or even days.
- **Work with independent parts.** Parallel branches finish many searches or many checks together.
- **Work that must be explained.** We can show the exact path that was taken, node by node. In banking, healthcare, and legal work, this matters a lot.

## Where Graph Engineering fails

- **Truly open ended work.** If we cannot even name the stages, then drawing a graph is only guesswork. A loop is a better fit there.
- **Very simple work.** If one model call answers the question, a graph only adds work with no benefit.
- **Graphs that grow without care.** A graph with sixty nodes and edges going everywhere is worse than a big prompt, because now the mess is spread across many files.
- **A messy state.** When every node adds a few keys and nobody removes anything, the state becomes a junkyard, and no node can be understood on its own.
- **Hidden dependencies.** If a node silently needs a key that only some earlier node writes, then moving the nodes around will break the graph in a way that is very hard to find.
- **Cycles without limits.** One missing stop condition, and our graph keeps running in circles all night, and we pay for every round.

## Best practices in Graph Engineering

**Keep every node small.** One node, one job. If we cannot describe a node in one short sentence, then it must be split into two nodes.

**Design the state first.** Write down every key, what it holds, and which node fills it. Do this before writing a single node.

**Keep the decisions in code, not in prose.** Let the model give the score, the label, or the choice. Let our own code read that value and pick the path. This one habit gives us most of the control.

**Put a limit on every cycle.** Count the attempts inside the state, and always have an exit path for the case when the count is over.

**Always have an exit.** Every path in the graph must reach an end, even the sad paths. A path that goes nowhere is a hung system.

**Turn failures into paths.** Write the error into the state, and route on it. Do not let one bad tool call kill the whole run.

**Draw the graph on paper.** If we cannot draw it, then our teammates and our users will never understand it. A graph that cannot be drawn is too complex.

**Log every node.** Save which node ran, what came in, and what went out. When something goes wrong, this log takes us straight to the guilty node. This is what gives us real [observability](https://outcomeschool.com/blog/ai-agent-observability) into our system.

**Test node by node.** Every node is just a function from state to state, so we can test it alone with a fixed state and no model at all. This is a huge advantage over one big prompt.

**Start with a straight line.** Build the simplest working path first. Add branches, cycles, and parallel work only when a real problem asks for them.

## Conclusion

Graph Engineering is a simple idea. Break the work into small steps, write down the paths between those steps, and keep all the progress inside one shared state.

When we do this, our AI system stops being a black box that sometimes works. It becomes a system that we can see, test, pause, resume, correct, and explain to anyone.

The model still does the thinking. The graph decides where that thinking goes.

Now we must have understood Graph Engineering, and we can start drawing our own graph for the work that we are building.

## Frequently Asked Questions

### Is Graph Engineering the same as prompt chaining?

No. Prompt chaining breaks the work into separate calls that run one after another, but a chain always moves forward in a straight line and never comes back. Graph Engineering keeps those small steps and adds the ability to go back, branch, and take decisions, with the paths between steps written down by us.

### Does the model choose the next step in Graph Engineering?

No. The model can give a score, a label, or a choice, but our own code reads that value from the state and picks the path. We let the model do the thinking, and we keep the control of the flow with ourselves. This is the heart of Graph Engineering.

### Does every node in a graph need to call an AI model?

No. A node is just a function that takes the current state, does one small job, and returns the updated state. A node can call a model, call a tool, hit a database, or run plain code with no model at all. This is also why we can test each node alone.

### Is LangGraph the same thing as Graph Engineering?

No. Graph Engineering is the practice of designing an AI system as nodes, edges, and state. LangGraph is the most popular library built for this work. Such libraries give us the same three ideas of node, edge, and state, only with slightly different names.

### What happens if two parallel nodes write to the same state key?

One will silently overwrite the other. When two nodes run at the same time in parallel branches, they must write into different keys of the state. A merge node can then join the results, so the rest of the graph does not need to know that two branches ran together.
