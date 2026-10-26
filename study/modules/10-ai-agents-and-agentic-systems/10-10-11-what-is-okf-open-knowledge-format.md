---
title: What is OKF (Open Knowledge Format)?
module: 10
module_title: AI Agents and Agentic Systems
lesson: '10.11'
source: https://outcomeschool.com/blog/what-is-okf-open-knowledge-format
published: July 26, 2026
tags:
- ai-agent
- llm
- ai
- system-design
videos: []
fetched: '2026-10-24'
words: 3812
reading_time: 19
status: full
---
# What is OKF (Open Knowledge Format)?

> **Module 10 · Lesson 10.11**  
> Source: [Outcome School](https://outcomeschool.com/blog/what-is-okf-open-knowledge-format) · Published: July 26, 2026 · Reading time: ~19 min · Tags: `ai-agent`, `llm`, `ai`, `system-design`

---

![What is OKF (Open Knowledge Format)?](../../assets/images/10-10-11-what-is-okf-open-knowledge-format/what-is-okf-open-knowledge-format.png)

OKF (Open Knowledge Format) is an open standard for writing down what an organization knows about its data and systems, as a folder of plain markdown files, so that any AI agent or any tool can read that knowledge.

In this blog, we will learn about OKF (Open Knowledge Format). We will also see why the knowledge about our data stays scattered across many places, how OKF writes that knowledge down as a folder of plain markdown files which any AI agent or any tool can read, and where it fits along with [MCP](https://outcomeschool.com/blog/what-is-mcp-model-context-protocol) and [Agent Skills](https://outcomeschool.com/blog/what-are-agent-skills) in the real world.

We will cover the following:

- The problem: our knowledge is scattered
- What is OKF?
- OKF = Open + Knowledge + Format
- What is inside an OKF bundle?
- The frontmatter and the one required field
- Cross-links turn files into a graph
- Why plain markdown files?
- How an agent actually uses it
- OKF, MCP, and Agent Skills
- What ships with OKF today
- Summary

Let's get started.

## The problem: our knowledge is scattered

Before jumping into OKF, we must understand the problem it solves.

Let's say we work at a company that sells things online. All of our business data sits in tables, and one of those tables is called `orders`.

Now, a new person joins our team. They are a good engineer and they know how to query a table. After a couple of weeks, they are given a simple job.

"Tell me how many sales we made last week."

It sounds easy. The table is right there, and it is not hidden from anybody. It has a `status` column, an `amount` column, and a `country` column, and the tool that lists our tables shows us those names and stops there.

But before that number is correct, there are five separate rules that have to be known, and each one of them was written down in a different place.

```
   only completed orders count        ->  one senior engineer knows this
   test orders must be removed        ->  a wiki page from two years ago
   a refund is a row with a minus     ->  a comment inside the code
   one country is counted twice       ->  a spreadsheet made last year
   data before March is not usable    ->  the same senior engineer
```

Here, we can see the problem. Every one of these rules is real, every one of them changes the final number, and no single place holds all five. The knowledge exists, but it is scattered, and nobody wrote it down in one place because each rule was learned on a different day by a different person. So the new person walks around asking people, and even then they only learn the rules somebody remembers to mention.

Now, this was always annoying. But something has changed that makes it much worse.

Today we have AI agents. An [AI agent](https://outcomeschool.com/blog/ai-agent) is an AI that takes actions step by step to finish a job for us. We ask an agent to build a sales report, and it goes looking at the `orders` table.

The agent faces the exact same problem as the new person, and it is in a worse position, because it cannot walk over to the senior engineer's desk and ask. It sees column names and nothing more. So it guesses. And a confident guess about what our data means is exactly how we end up with a report full of wrong numbers. We have a detailed blog on [Context Engineering](https://outcomeschool.com/blog/context-engineering) that explains how we give an agent the right context to work with.

Now, we can think the answer is simple. Let's just write all of it down properly in one tool.

But, here is the catch. Every tool stores this knowledge in its own private shape, behind its own way of asking for it. So if we write everything into tool A, then tool B cannot read it, and our agent has to be taught tool A's private language first. Move to a different tool next year, and the whole thing has to be redone.

So, we need one common shape for writing down what we know, which every tool and every agent can read without special treatment.

We needed a solution for that. So, here comes OKF to the rescue.

## What is OKF?

**OKF, which stands for Open Knowledge Format, is an open standard for writing down what an organization knows about its data and systems, as a folder of plain markdown files, so that any AI agent or any tool can read that knowledge without custom work.**

It was published by the Google Cloud Data Cloud team on 13 June 2026, as version 0.1.

In simple words, OKF is an agreed way of writing our company's knowledge into ordinary text files, so that both people and machines can read the same file.

Now, this idea did not appear out of nowhere. For a while, teams had already been keeping a folder of notes written specially for their AI to read, and people started calling this an "LLM wiki". The habit worked well, but every team invented its own arrangement, so one team's notes could not be shared with anybody else. OKF takes that habit and writes down the rules for it, so that the notes one team keeps can be read by another team's agent.

Let's be clear about the most important design choice, because it explains everything else.

> OKF is just markdown. Just files. Just YAML frontmatter.

There is no software to install. There is no server to run. There is no special program needed to read it. We will understand what each of those words means as we go.

Let's see the change it brings.

```
   Without a common format:
     Catalog tool   ->  shape A  ->  needs a reader built only for shape A
     Company wiki   ->  shape B  ->  needs a reader built only for shape B
     Code comment   ->  shape C  ->  needs a reader built only for shape C
     3 sources, 3 different shapes, 3 readers to build and maintain
   With OKF:
     Catalog tool   --+
     Company wiki   --+-->  the same OKF files  ->  one reader for all of them
     Code comment   --+
     3 sources, 1 shape, 0 readers to build
```

In this diagram, "shape" means the arrangement each tool uses to store the knowledge, and a "reader" is the extra code our agent needs so it can understand that one arrangement.

Here, we can see the whole point of a standard. In the first case, adding one more source means building one more reader, so the work keeps growing forever. In the second case, everybody writes the same shape once, and a single reader understands all of them, including the sources we add next year. The people writing the knowledge and the tools reading it no longer need to know about each other at all.

## OKF = Open + Knowledge + Format

The name is doing exactly what it says, so let's break it down.

> OKF = Open + Knowledge + Format

- **Open** means the rules are published for everybody. Anyone can write these files, and anyone can read them.
- **Knowledge** means the part that is not the data itself. Not the rows in the table, but what the table means, why it exists, what its columns are for, and what to watch out for.
- **Format** means an agreed shape for writing it down, so that everybody writes it the same way.

Means, OKF is an agreed and openly published shape for writing down what we know.

Now, let's be very clear about that middle word, because it is the part people misread. OKF does not store our data. It stores the understanding that sits around our data.

Let's see the difference side by side.

```
   THE DATA lives in the table:
     order_id | amount | status    | country
     ---------+--------+-----------+--------
     1001     | 250    | complete  | IN
     1002     | 90     | cancelled | IN
     1003     | 410    | complete  | US
     ...      | ...    | ...       | ...       (a million more rows)
   THE KNOWLEDGE lives in the OKF file:
     "One row per order. Only completed ones count as a sale."
```

Here, we can see it clearly. The table holds a million rows and never explains itself. The OKF file holds one short sentence, and that sentence is what tells us the cancelled row must not be counted. The data is the what. The knowledge is the meaning.

## What is inside an OKF bundle?

Now, let's open one up. A collection of OKF files is called a **bundle**, and a bundle is simply a folder on a computer.

Let's look at a real one.

```
   sales/
   ├── index.md
   ├── datasets/
   │   ├── index.md
   │   └── orders_db.md
   ├── tables/
   │   ├── index.md
   │   ├── orders.md
   │   └── customers.md
   └── metrics/
       ├── index.md
       └── weekly_active_users.md
```

Here, we can see the whole idea at a glance. It is folders and files, exactly like the folders on our own laptop. Nothing more.

The rule is simple. **One file per concept.** The `orders` table gets one file. The `customers` table gets its own file. The "weekly active users" measurement gets its own file too.

Every file ends in `.md`, which means it is a **markdown** file. Markdown is simply plain text with very light formatting, the kind we already use for a README file. We can open it in any text editor.

There is one more clever detail here. The location of the file is the name of the concept. The `orders` table is at `tables/orders.md`, so its identity is that path. Nobody needs to invent a separate identification system, because the folder structure already provides one.

**Note:** Those `index.md` files are optional. They act like the front page of each folder, giving a short overview so that a reader can understand the folder without opening every file in it. There is also an optional `log.md`, which keeps a dated history of what changed.

## The frontmatter and the one required field

Now, let's look inside a single file. Each file has two parts.

The top part sits between two lines of dashes, and it is called the **frontmatter**. It holds the labeled facts about this concept. It is written in a style called YAML, which is simply "label: value" on each line.

The bottom part is the body, which is ordinary markdown, where we explain things in normal sentences.

Let's see a whole file at once, so the two parts are clear.

```
   tables/orders.md
   +----------------------------------------------------+
   |  ---                                               |
   |  type: BigQuery Table                              |   <- frontmatter
   |  title: Orders                                     |      (labeled facts,
   |  description: One row per order ...                |       read by machines)
   |  ---                                               |
   |                                                    |
   |  # Orders                                          |   <- body
   |                                                    |      (plain sentences,
   |  This table is loaded every night at 2 AM.         |       read by people)
   |  Cancelled orders are never counted as sales.      |
   +----------------------------------------------------+
```

Here, we can see both halves in one place. The top half holds short labeled facts, which a machine can sort and filter on. The bottom half holds everything a person would say out loud, the kind of detail that never fits into a label. Both live in the same file, so they can never drift apart.

Now, let's look closely at the top of a real file.

```yaml
---
type: BigQuery Table
title: Orders
description: One row per order. Only completed ones count as a sale.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders
tags: [sales, revenue]
timestamp: 2026-05-28T14:30:00Z
---
```

Here, we can read every line without knowing anything technical.

- `type` says what kind of thing this is. Here it is a table inside BigQuery, which is Google's service for storing very large amounts of data.
- `title` is the human name.
- `description` is the one-line explanation. Notice how much this single line solves. The first rule our new person had to hunt for, that only completed orders count as sales, is answered right here.
- `resource` is a link to the actual thing, so we can go and look at it.
- `tags` are labels for grouping, written as a list.
- `timestamp` records when this was last true, written in a standard date style.

Now, here is the part that surprises people. **Out of all of these, only `type` is required.** Everything else is optional.

Why would a standard ask for so little? Because a standard that demands twenty fields is a standard nobody fills in. By asking for almost nothing, OKF makes it easy to start with a single line and add more later. The other fields are simply the agreed names to use when we do want them, so that everybody uses the same word instead of one team writing `description` and another writing `desc`.

And the types themselves are deliberately loose. `BigQuery Table` is just an example. A `Dataset`, a `Metric`, an `API`, a `Runbook`, a `Playbook`, all of these are fine. OKF does not hand us a fixed list to pick from.

## Cross-links turn files into a graph

Now, let's learn the part that makes a bundle more than a pile of files.

Concepts in the real world point at each other. The `orders` table has a column that refers to a customer, and customers live in a different table. So how do we record that connection?

We use an ordinary markdown link, exactly the kind we would write in any document.

```markdown
| `customer_id` | STRING | FK to [customers](/tables/customers.md). |
```

Here, we can see a row from a table description inside the `orders.md` file. It says there is a column called `customer_id`, and it holds text. Then `FK` is short for foreign key, which simply means the value in this column identifies a row sitting in a different table. And notice how that connection is recorded. It is a plain clickable link to the other file.

Now, why does this matter so much? Because once every file can link to other files, the whole bundle stops being a flat list and becomes a **graph**, which simply means a set of things joined by connections.

```
   orders.md  ---- points to ---->  customers.md
       |
       +---------- points to ---->  orders_db.md
```

Here, we can see what that gives an agent. It starts at the `orders` file, discovers that customers matter, and follows the link to go and read about them. It can walk through our knowledge the same way we walk through linked pages, one step at a time, learning only what it needs.

## Why plain markdown files?

Now, the following question arises. Why did they choose something as plain as text files, when far more powerful options exist?

The plainness is the whole point. Let's see what we get for free because of it.

- **Humans can read it.** The same file that the agent reads is the file we read. There is no separate version for people, so the two can never drift apart.
- **It renders anywhere.** Put the bundle in a code repository, and it displays as neat formatted pages. Search tools can index it.
- **It travels easily.** It is a folder, so we can zip it up, share it, or copy it onto a machine.
- **It versions with our code.** Because these are files, we can keep them beside our code and track every change over time, exactly as we do with code.
- **Nothing needs installing.** No program to buy, no service to keep running, no library to add to our project.

## How an agent actually uses it

Now, let's follow one real request from start to finish, so the whole thing becomes concrete.

Suppose we ask our AI agent the same job we gave the new person at the start, "how many sales did we make last week?"

**Step 1:** Before touching any data, the agent looks in the OKF bundle. It reads `index.md` to see what exists.

**Step 2:** It sees a `tables` folder and opens `tables/orders.md`.

**Step 3:** It reads the frontmatter and learns the important sentence straight away. One row is one order, and only the **completed** ones count as a sale. So it now knows it must not count orders that were cancelled or still in progress.

**Step 4:** It reads the body, sees the `customer_id` column, and follows the link to `customers.md` if it needs to.

**Step 5:** It uses the `resource` link to find where the real table actually lives.

**Step 6:** Only now does it go and do the actual work, and it produces the right number.

We can picture the whole flow as below:

```
   our question
        |
        v
   read the OKF bundle FIRST        <-  this is the new step
        |
        v
   learn the rule: "completed orders only"
        |
        v
   now go to the real table
        |
        v
   the right answer
```

Here, we can see that only one step was added, and it was added at the front. Everything after it stays the same. That one step is the difference between an answer and a guess.

Here, we can notice the most important point. The agent did not become smarter. It simply stopped guessing. All the knowledge it needed was written down once, by somebody who knew, in a file that the agent could read.

This way we can use OKF to solve the interesting problem of giving an agent our own context, without teaching it any special tool.

## OKF, MCP, and Agent Skills

Now, there are two other open standards that come up in the same conversation, and it helps a lot to see how the three differ. They are not competing. Each answers a different question.

- **MCP**, which stands for Model Context Protocol, connects an agent to outside tools and data. It answers "what can the agent reach?"
- **Agent Skills** are folders of instructions that teach an agent our way of doing a job. They answer "how should the agent do this?"
- **OKF** records what our data and systems actually mean. It answers "what is this thing?"

Agent Skills are already in use today. A coding agent picks up our team's way of working from a plain markdown file kept inside the project, exactly like this. We have a detailed blog on [How does Claude Code work?](https://outcomeschool.com/blog/how-does-claude-code-work) that explains this step by step.

Let me tabulate the differences between the three for your better understanding so that you can decide which one to use based on your use case.

| Point | OKF | Agent Skills | MCP |
| --- | --- | --- | --- |
| What it carries | Knowledge about our things | Know-how, our steps and format | Reach, a live connection |
| Question it answers | What is this thing? | How should this be done? | What can the agent reach? |
| What it is made of | A folder of markdown files | A folder of markdown files | A running program |
| Needs something running | No | No | Yes |
| Best for | Data meaning, definitions, context | Procedures, checklists, style | Databases, apps, live actions |

They solve different problems. In real work they fit together. MCP connects the agent to our database, OKF tells it what the tables in that database mean, and a Skill tells it how our team wants the report written.

**Note:** We can notice from the table that OKF and Agent Skills are built almost the same way, as a folder of markdown files with frontmatter at the top.

## What ships with OKF today

Now, a standard on its own is only a document. So let's see what was actually released alongside it.

**An enrichment agent.** This walks through a company's existing data, and drafts the OKF files automatically. This matters more than it sounds, because writing hundreds of files by hand is the reason such efforts usually die. Here, a first draft is generated for us, and people then correct and improve it.

**A visualizer.** This turns any bundle into a single web page showing the graph of concepts and their links, so we can look at our knowledge instead of reading folders.

## Summary

Let's quickly recap what we have learned.

- Knowledge about our data is scattered across catalogs, wikis, code comments, and people's heads, and an AI agent cannot go and ask a person.
- Every tool stores this knowledge in its own private shape, so it cannot be shared or moved.
- OKF is an open standard for writing that knowledge down, published by the Google Cloud Data Cloud team on 13 June 2026 as version 0.1.
- It formalizes a habit teams already had, of keeping a folder of notes for their AI, which people called an LLM wiki, and gives it rules so the notes can be shared.
- OKF = Open + Knowledge + Format. It records what our data means, and never the data itself.
- A bundle is a plain folder of markdown files, with one file per concept, and the file path is the concept's identity.
- Each file has YAML frontmatter at the top, where `type` is the only required field, and `title`, `description`, `resource`, `tags`, and `timestamp` are the agreed optional ones.
- Files link to each other with ordinary markdown links, which turns the bundle into a graph an agent can walk through.
- It is deliberately plain, so it needs no software, reads the same for people and machines, and versions alongside our code.
- An agent reads the bundle before doing real work, so it stops guessing what our data means.
- MCP gives reach, Agent Skills give know-how, and OKF gives knowledge. They work together.

This is what OKF is, one plain and open way to write down what we know, so that our agents finally understand our data instead of guessing at it.

## Frequently Asked Questions

### Who created OKF?

OKF was published by the Google Cloud Data Cloud team on 13 June 2026, as version 0.1. It is an open standard, which means the rules are published for everybody. Anyone can write OKF files, and any AI agent or tool can read them without custom work.

### Does OKF store our data?

No. OKF does not store our data. It stores the understanding that sits around our data, like what a table means, what its columns are for, and what to watch out for. The rows stay in the table, while the OKF file holds the meaning, such as which orders count as a sale.

### Is OKF the same as an LLM wiki?

Not exactly. An LLM wiki is a folder of notes that teams kept specially for their AI to read, but every team invented its own arrangement, so the notes could not be shared. OKF takes that habit and writes down the rules for it, so the notes one team keeps can be read by another team's agent.

### Is OKF only for describing database tables?

No. The types in OKF are deliberately loose, and there is no fixed list to pick from. A Dataset, a Metric, an API, a Runbook, or a Playbook are all fine types. Only the `type` field is required, and everything else is optional.

### Does OKF replace MCP?

No. OKF and MCP answer different questions and work together. MCP connects the agent to outside tools and data, like our database, so it gives reach. OKF records what our data and systems actually mean, so it tells the agent what the tables in that database mean.
