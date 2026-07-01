Here is a comprehensive context summary of everything we have covered, designed specifically for you to feed directly into your coding assistant to generate a flawless, highly detailed Markdown note for **Module 1 (Agentic RAG Setup)**.

---

# Technical Knowledge Context: Transitioning from Scripting to Object-Oriented RAG Design

## 1. The Architectural Shift (System Design Goal)

* **The Problem:** In initial Jupyter notebooks or linear scripts, RAG components (loading data, querying indices, parsing templates, and initiating LLM clients) run sequentially utilizing **global variables** (e.g., global `index` and global `openai_client`). This makes the codebase fragile, hard to test, and messy. If you want to change the course context or swap models, you have to rewrite or duplicate massive chunks of code.
* **The Solution:** Encapsulating the RAG logic inside a unified class structure (`RAGBase`). This implements **Dependency Injection**. Instead of hardcoding *how* it searches or *which* LLM client it connects to, we pass those objects as dependencies into the class constructor.
* **Agentic Future:** This clean separation of concerns provides a modular foundational class. Later in the course, when building fully autonomous **AI Agents** (which must decide when to search and when to reply), the agent can simply interact with these decoupled methods seamlessly.

---

## 2. The Core OOP Mental Model (The Smartphone Analogy)

To understand how a class architecture functions, we use a strict sequential relationship model:

1. **Class (The Blueprint):** The factory design plan. It does not exist as a physical item in memory yet; it simply dictates the parameters every instance *will* have and the actions it *will* be capable of executing.
2. **Attributes (The Specifications):** The data points, properties, or variables attached to the body of the object. It gives the object a long-term "memory" (e.g., a phone's `color`, `storage_gb`, or current `battery_level`).
3. **Methods (The Buttons / Actions):** Functions defined inside the class block that allow the object to *do* something. They use the special `self` keyword as their first parameter, giving them a backstage pass to read and alter the object's internal attributes (e.g., pressing the `send_text()` button on a phone drains its `battery_level` attribute).
4. **Parameters (The Placeholders):** The empty text fields or inputs defined in a method's signature. The capability to execute the action exists, but the method needs these specific slot placeholders filled before it can complete the request (e.g., the `contact_name` and `message_text` blanks in a text-messaging app).
5. **Arguments (The Real-World Data):** The actual live strings, integers, or objects typed into those empty placeholders when you execute the method at runtime (e.g., passing `"Alice"` and `"Hey there!"` into the text app).

---

## 3. Code Mapping: OOP Concepts in the `RAGBase` Class

### A. The Class Block

The master blueprint encapsulating the system.

```python
class RAGBase:
    # Everything indented inside here defines the blueprint

```

### B. The Constructor & Attributes (System State Setup)

The `__init__` method runs automatically the moment an object is created. This is where parameters are stored into long-term object attributes via `self.`.

```python
def __init__(self, index, llm_client, course="llm-zoomcamp", model="gpt-5.4-mini"):
    self.index = index            # Attribute: Injected Search Index object
    self.llm_client = llm_client  # Attribute: Injected LLM API provider client
    self.course = course          # Attribute: Course filter string (Default: "llm-zoomcamp")
    self.model = model            # Attribute: String name of target model

```

* **Positional Parameters (`index`, `llm_client`):** Mandatory configurations that must be provided at instantiation.
* **Default Parameters (`course=...`, `model=...`):** Optional placeholders. If the user doesn't pass arguments for them, Python automatically assigns these default values.

### C. Methods & Dynamic Parameters (Isolated Pipeline Actions)

Regular instance methods handle isolated tasks, combining incoming dynamic parameters with saved object memory (attributes).

```python
def search(self, query, num_results=5):
    # 'query' and 'num_results' are dynamic Parameters
    # 'self.course' and 'self.index' are permanent Attributes retrieved from memory
    filter_dict = {"course": self.course}
    return self.index.search(query, num_results=num_results, filter_dict=filter_dict)

```

* `query` changes every single time a user asks a new question, making it a parameter.
* `self.course` remains constant in the object's configuration unless explicitly altered, making it an attribute.

---

## 4. The Critical Gotcha: Scope & The Execution Environment

A major concept point to document is the difference between **Internal Scope (`self`)** and **External Scope (Instance Variable)**.

* **Inside the Class Definition:** You *must* use `self` to refer to the object (e.g., `self.model = "gpt-4o"`). `self` is a variable placeholder representing "this specific instance currently running the code."
* **Outside the Class (In your Notebook/Application layer):** The word `self` does not exist globally. If you try to run `self.model = "gpt-4o"` in a notebook cell, Python will crash with a `NameError`. Instead, you must target the specific variable name given to your instantiated object.

```python
# --- IN YOUR NOTEBOOK ---

# 1. Instantiate the object (The Argument creates the Object)
assistant = RAGBase(index=index, llm_client=openai_client)

# 2. Reading an attribute from the outside using its external name
print(assistant.model)  # Output: gpt-5.4-mini

# 3. Correct way to modify an attribute from the outside:
assistant.model = "gpt-4o"  # Overwrites the attribute directly on this instance

# 4. Executing the Orchestrator Method:
# "Can I join now?" is the Argument filling the 'query' Parameter placeholder
answer = assistant.rag("Can I join now?")

```

---

## 5. Why This Design Matters for System Architecture

1. **State Isolation:** You can create two assistants simultaneously in the same notebook without them conflicting or leaking data:
```python
zoomcamp_bot = RAGBase(index=idx, llm_client=cli, course="llm-zoomcamp")
mlops_bot = RAGBase(index=idx, llm_client=cli, course="mlops-zoomcamp")

```


2. **Modularity and Swappability:** Because `search` and `llm` are isolated methods that depend entirely on `self.index` and `self.llm_client`, you can easily replace standard `minsearch` with a production Vector database or replace OpenAI with OpenRouter without touching the core orchestration logic inside `.rag()`.
3. **Subclass Extensibility:** This architecture allows developers to use inheritance later. For instance, to test a totally different embedding or prompting strategy, you can create a child class (`class AdvancedAgent(RAGBase)`) and simply override the `build_prompt` method while preserving the indexing, searching, and model querying routines perfectly intact.
Below is a **note-ready** version of the mental model for Module 1, Part 1, especially the RAG flow, `lesson 7`, `ingest.py`, and `RAGBase`. The module is built from scratch in plain Python so you can understand the full system, not just use a framework. [youtube](https://www.youtube.com/watch?v=KHePGkeFn54)

## What RAG means

RAG means **Retrieval-Augmented Generation**. In simple words, it is a way to make an LLM answer using your own knowledge base: first find relevant information, then give that information to the model so it can generate a grounded answer. [youtube](https://www.youtube.com/watch?v=JktYwBIDErk&list=PL3MmuxUbc_hLZFNgSad56pDBKK8KO0XIv)

The key idea is that the LLM is not expected to know everything by memory. Instead, the system helps it by fetching the right context from your documents before it answers. [youtube](https://www.youtube.com/watch?v=Mx6EqvzVDz0)

## Why RAG exists

A plain LLM can sound confident even when it is missing your specific data. That is why the course builds a RAG system for the course FAQ: the system should answer from the actual course materials, not from vague general memory. [youtube](https://www.youtube.com/watch?v=Mx6EqvzVDz0)

So the purpose of RAG is not “make the model smarter” in a general sense. The purpose is to make the answer more relevant, more accurate, and tied to your own data. [youtube](https://www.youtube.com/watch?v=KHePGkeFn54)

## Mental model

The best mental model is:

1. User asks a question.
2. The system searches the knowledge base.
3. The system collects the most relevant text.
4. The LLM reads that text.
5. The LLM writes the final answer. [youtube](https://www.youtube.com/watch?v=JktYwBIDErk&list=PL3MmuxUbc_hLZFNgSad56pDBKK8KO0XIv)

A simple analogy is a student answering an exam with notes open. The search step finds the notes, and the generation step turns them into a clear answer. [youtube](https://www.youtube.com/watch?v=JktYwBIDErk&list=PL3MmuxUbc_hLZFNgSad56pDBKK8KO0XIv)

## Lesson 7 idea

In lesson 7, the pipeline becomes a working RAG system by wiring search, prompt building, and the LLM call together. The lesson also shows how to inspect the response object and track token usage and cost. [youtube](https://www.youtube.com/watch?v=KHePGkeFn54)

This is important because it turns the lesson from “concept” into “system”: not just what RAG is, but how the pieces cooperate in code. [youtube](https://www.youtube.com/watch?v=KHePGkeFn54)

## What `ingest.py` does

`ingest.py` is the preparation step. Its job is to take the FAQ data, load it, and build an index so the search step can find relevant chunks later. [youtube](https://www.youtube.com/watch?v=JxaC6Hrym6c)

Think of it as library organization. It does not answer questions; it prepares the books so they can be searched quickly and consistently. [youtube](https://www.youtube.com/watch?v=JxaC6Hrym6c)

## What `rag_helper.py` does

`rag_helper.py` contains the reusable RAG logic. It wraps the search, prompt, and LLM call into a helper class so the same workflow can be reused in different places. [youtube](https://www.youtube.com/watch?v=JxaC6Hrym6c)

This is where the actual answer pipeline lives. The class is meant to make the code clean, reusable, and easier to customize. [youtube](https://www.youtube.com/watch?v=JxaC6Hrym6c)

## Why `RAGBase` exists

`RAGBase` exists because the earlier version used global variables like `index` and `openai_client`, and that makes code harder to reuse. The lesson explicitly says the class is used because globals break when the logic is moved into separate files. [youtube](https://www.youtube.com/watch?v=JxaC6Hrym6c)

By putting `index` and the LLM client into the constructor, the class becomes flexible. You can pass in a different search engine or a different model client without rewriting the whole pipeline. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/161106857/77f78d11-62a5-4554-949c-a1ad5b1ae2cb/selected_image_1964466531463269028.jpg?AWSAccessKeyId=ASIA2F3EMEYE5EIVM2P4&Signature=Ky5MtbtjWazqolvVdxz1hm6ZkZs%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEBUaCXVzLWVhc3QtMSJHMEUCIQDLAbZNiAYf5%2FJH38XeGUwaqfQcfDy1ebluGttrAzVdkwIgHrj6R3NLzbXU%2FbGs7TX4wq8rbCXimZ6yRFsV%2BcGgzcEq%2FAQI3f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDH5cSpvO%2BnaAUhE1%2FSrQBNnNT42h8Nj0ew%2BBLDue%2B9jq70qSTnQmrNIufFu1yWXN8q1tSRitVUIuej4HB3i%2BOEl7tE1IS69YszlJ4STneI%2F5v40H8Zz35WPr8KbqVXD3t1syiJjI3jsoNPfJk5ZvLEC%2BvvbGMlaGD9AQQkzjvxU05oOitpXpC753TzspstDDmWCaVSe6beT6iu4cxt6OrugItWa1tBae1MmTqIOHDibKcXjyKurziT%2BZgjrzUmrXfuemBzA3cYMU73BWMi5tLtGHZ8Ub7KWuMM%2BHqXkm3xW2w0aWD2qG4WUa385hCCBWDSyqagL71v5Bk%2BgeMepswAt5h1GLMzSxWviHH6dYjyf5PNe4hHhtfqGqTqMdZEcenk09waRE4CAKHf%2B17VR2v8zfAUkyGsI6nNKCRnYMcsZgTI%2BO69YO4MST8oDvfPPvWjVSD6jyGTiGOOGX0sigvzsnb54%2F4JkkNb9a%2BekOGBD1%2FXGVEaWbX0etSss9jP%2F0%2BZdjG7uacfzzSDt4leZ5BAvxFYGsw1pDqfUG8JyC%2FpcrO%2B5nqTTJd1FeYzubpNDOsEpFFcs1%2FYjDyFGMcDdbM7Xa%2FL85UvtXEzBLjwD8KTwfcmwTHWjPVss%2Fd%2FZBeBWlkVcXAcNRYzf%2B6RP5IRTR7xOn7EF%2F8TKPzDyFkr67Wzf4OmVcbZtwtzzOmj1UWyKUO9DCSwlJ9Ws0v6CLh7ek%2Fdx4U4u90y1cIMfSn5odXcSMSh6FJB8386xL2ESmTQW6ALIVZHYgmgAd3beekBe%2BnUIxoHRVWJkr%2Beefl1PHYrIw7oWU0gY6mAHhbbt8UHgeKlDn5QVsKx%2Baq%2B5Tt8Wsd5ZYsUadbeygtnocOjuHWF6%2FcULe9UhEq5xRNp%2FW%2FccfL7TZlqpwvesvTGnBxx12nC19LvqvTFVFz7NaZ%2FT5zTdfWu%2B1jMSOYxNfDHorXt3EeBDZk5%2F4%2BbN%2BJ43uvtWYiOC36kCT%2ByduF1Qo3N6EhmxarKQJ6sl2Odv1%2FHx4s4Pfjw%3D%3D&Expires=1782911169)

## Constructor arguments

When the lesson says the index and LLM client become constructor arguments, it means they are passed into the class when creating the object. In Python, the constructor is usually `__init__`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/161106857/77f78d11-62a5-4554-949c-a1ad5b1ae2cb/selected_image_1964466531463269028.jpg?AWSAccessKeyId=ASIA2F3EMEYE5EIVM2P4&Signature=Ky5MtbtjWazqolvVdxz1hm6ZkZs%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEBUaCXVzLWVhc3QtMSJHMEUCIQDLAbZNiAYf5%2FJH38XeGUwaqfQcfDy1ebluGttrAzVdkwIgHrj6R3NLzbXU%2FbGs7TX4wq8rbCXimZ6yRFsV%2BcGgzcEq%2FAQI3f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDH5cSpvO%2BnaAUhE1%2FSrQBNnNT42h8Nj0ew%2BBLDue%2B9jq70qSTnQmrNIufFu1yWXN8q1tSRitVUIuej4HB3i%2BOEl7tE1IS69YszlJ4STneI%2F5v40H8Zz35WPr8KbqVXD3t1syiJjI3jsoNPfJk5ZvLEC%2BvvbGMlaGD9AQQkzjvxU05oOitpXpC753TzspstDDmWCaVSe6beT6iu4cxt6OrugItWa1tBae1MmTqIOHDibKcXjyKurziT%2BZgjrzUmrXfuemBzA3cYMU73BWMi5tLtGHZ8Ub7KWuMM%2BHqXkm3xW2w0aWD2qG4WUa385hCCBWDSyqagL71v5Bk%2BgeMepswAt5h1GLMzSxWviHH6dYjyf5PNe4hHhtfqGqTqMdZEcenk09waRE4CAKHf%2B17VR2v8zfAUkyGsI6nNKCRnYMcsZgTI%2BO69YO4MST8oDvfPPvWjVSD6jyGTiGOOGX0sigvzsnb54%2F4JkkNb9a%2BekOGBD1%2FXGVEaWbX0etSss9jP%2F0%2BZdjG7uacfzzSDt4leZ5BAvxFYGsw1pDqfUG8JyC%2FpcrO%2B5nqTTJd1FeYzubpNDOsEpFFcs1%2FYjDyFGMcDdbM7Xa%2FL85UvtXEzBLjwD8KTwfcmwTHWjPVss%2Fd%2FZBeBWlkVcXAcNRYzf%2B6RP5IRTR7xOn7EF%2F8TKPzDyFkr67Wzf4OmVcbZtwtzzOmj1UWyKUO9DCSwlJ9Ws0v6CLh7ek%2Fdx4U4u90y1cIMfSn5odXcSMSh6FJB8386xL2ESmTQW6ALIVZHYgmgAd3beekBe%2BnUIxoHRVWJkr%2Beefl1PHYrIw7oWU0gY6mAHhbbt8UHgeKlDn5QVsKx%2Baq%2B5Tt8Wsd5ZYsUadbeygtnocOjuHWF6%2FcULe9UhEq5xRNp%2FW%2FccfL7TZlqpwvesvTGnBxx12nC19LvqvTFVFz7NaZ%2FT5zTdfWu%2B1jMSOYxNfDHorXt3EeBDZk5%2F4%2BbN%2BJ43uvtWYiOC36kCT%2ByduF1Qo3N6EhmxarKQJ6sl2Odv1%2FHx4s4Pfjw%3D%3D&Expires=1782911169)

So instead of hard-coding one index and one model inside the class, you give the class what it needs from the outside. That is what makes the helper reusable. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/161106857/77f78d11-62a5-4554-949c-a1ad5b1ae2cb/selected_image_1964466531463269028.jpg?AWSAccessKeyId=ASIA2F3EMEYE5EIVM2P4&Signature=Ky5MtbtjWazqolvVdxz1hm6ZkZs%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEBUaCXVzLWVhc3QtMSJHMEUCIQDLAbZNiAYf5%2FJH38XeGUwaqfQcfDy1ebluGttrAzVdkwIgHrj6R3NLzbXU%2FbGs7TX4wq8rbCXimZ6yRFsV%2BcGgzcEq%2FAQI3f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDH5cSpvO%2BnaAUhE1%2FSrQBNnNT42h8Nj0ew%2BBLDue%2B9jq70qSTnQmrNIufFu1yWXN8q1tSRitVUIuej4HB3i%2BOEl7tE1IS69YszlJ4STneI%2F5v40H8Zz35WPr8KbqVXD3t1syiJjI3jsoNPfJk5ZvLEC%2BvvbGMlaGD9AQQkzjvxU05oOitpXpC753TzspstDDmWCaVSe6beT6iu4cxt6OrugItWa1tBae1MmTqIOHDibKcXjyKurziT%2BZgjrzUmrXfuemBzA3cYMU73BWMi5tLtGHZ8Ub7KWuMM%2BHqXkm3xW2w0aWD2qG4WUa385hCCBWDSyqagL71v5Bk%2BgeMepswAt5h1GLMzSxWviHH6dYjyf5PNe4hHhtfqGqTqMdZEcenk09waRE4CAKHf%2B17VR2v8zfAUkyGsI6nNKCRnYMcsZgTI%2BO69YO4MST8oDvfPPvWjVSD6jyGTiGOOGX0sigvzsnb54%2F4JkkNb9a%2BekOGBD1%2FXGVEaWbX0etSss9jP%2F0%2BZdjG7uacfzzSDt4leZ5BAvxFYGsw1pDqfUG8JyC%2FpcrO%2B5nqTTJd1FeYzubpNDOsEpFFcs1%2FYjDyFGMcDdbM7Xa%2FL85UvtXEzBLjwD8KTwfcmwTHWjPVss%2Fd%2FZBeBWlkVcXAcNRYzf%2B6RP5IRTR7xOn7EF%2F8TKPzDyFkr67Wzf4OmVcbZtwtzzOmj1UWyKUO9DCSwlJ9Ws0v6CLh7ek%2Fdx4U4u90y1cIMfSn5odXcSMSh6FJB8386xL2ESmTQW6ALIVZHYgmgAd3beekBe%2BnUIxoHRVWJkr%2Beefl1PHYrIw7oWU0gY6mAHhbbt8UHgeKlDn5QVsKx%2Baq%2B5Tt8Wsd5ZYsUadbeygtnocOjuHWF6%2FcULe9UhEq5xRNp%2FW%2FccfL7TZlqpwvesvTGnBxx12nC19LvqvTFVFz7NaZ%2FT5zTdfWu%2B1jMSOYxNfDHorXt3EeBDZk5%2F4%2BbN%2BJ43uvtWYiOC36kCT%2ByduF1Qo3N6EhmxarKQJ6sl2Odv1%2FHx4s4Pfjw%3D%3D&Expires=1782911169)

## Class and subclass

A class is a blueprint. A subclass is a new class that inherits from the base class and can reuse or override parts of it. [youtube](https://www.youtube.com/watch?v=JxaC6Hrym6c)

In this lesson:

- `RAGBase` gives the shared workflow.
- A subclass can change search or model behavior.
- The rest of the workflow stays the same. [youtube](https://www.youtube.com/watch?v=JxaC6Hrym6c)

That means the code is designed around **shared structure, customizable parts**. [youtube](https://www.youtube.com/watch?v=JxaC6Hrym6c)

## Why this design matters

This design lets you swap components without changing the overall logic. For example, the search backend could be Elasticsearch or Qdrant, and the model client could be OpenAI, Anthropic, OpenRouter, NVIDIA NIM, or a local model, as long as the object provides the methods the helper expects. [docs.nvidia](https://docs.nvidia.com/nemo/agent-toolkit/1.1/workflows/using-local-llms.html)

The important idea is not “anything works automatically.” The important idea is “the pipeline stays stable while the implementation behind each part can change.” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/161106857/77f78d11-62a5-4554-949c-a1ad5b1ae2cb/selected_image_1964466531463269028.jpg?AWSAccessKeyId=ASIA2F3EMEYE5EIVM2P4&Signature=Ky5MtbtjWazqolvVdxz1hm6ZkZs%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEBUaCXVzLWVhc3QtMSJHMEUCIQDLAbZNiAYf5%2FJH38XeGUwaqfQcfDy1ebluGttrAzVdkwIgHrj6R3NLzbXU%2FbGs7TX4wq8rbCXimZ6yRFsV%2BcGgzcEq%2FAQI3f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDH5cSpvO%2BnaAUhE1%2FSrQBNnNT42h8Nj0ew%2BBLDue%2B9jq70qSTnQmrNIufFu1yWXN8q1tSRitVUIuej4HB3i%2BOEl7tE1IS69YszlJ4STneI%2F5v40H8Zz35WPr8KbqVXD3t1syiJjI3jsoNPfJk5ZvLEC%2BvvbGMlaGD9AQQkzjvxU05oOitpXpC753TzspstDDmWCaVSe6beT6iu4cxt6OrugItWa1tBae1MmTqIOHDibKcXjyKurziT%2BZgjrzUmrXfuemBzA3cYMU73BWMi5tLtGHZ8Ub7KWuMM%2BHqXkm3xW2w0aWD2qG4WUa385hCCBWDSyqagL71v5Bk%2BgeMepswAt5h1GLMzSxWviHH6dYjyf5PNe4hHhtfqGqTqMdZEcenk09waRE4CAKHf%2B17VR2v8zfAUkyGsI6nNKCRnYMcsZgTI%2BO69YO4MST8oDvfPPvWjVSD6jyGTiGOOGX0sigvzsnb54%2F4JkkNb9a%2BekOGBD1%2FXGVEaWbX0etSss9jP%2F0%2BZdjG7uacfzzSDt4leZ5BAvxFYGsw1pDqfUG8JyC%2FpcrO%2B5nqTTJd1FeYzubpNDOsEpFFcs1%2FYjDyFGMcDdbM7Xa%2FL85UvtXEzBLjwD8KTwfcmwTHWjPVss%2Fd%2FZBeBWlkVcXAcNRYzf%2B6RP5IRTR7xOn7EF%2F8TKPzDyFkr67Wzf4OmVcbZtwtzzOmj1UWyKUO9DCSwlJ9Ws0v6CLh7ek%2Fdx4U4u90y1cIMfSn5odXcSMSh6FJB8386xL2ESmTQW6ALIVZHYgmgAd3beekBe%2BnUIxoHRVWJkr%2Beefl1PHYrIw7oWU0gY6mAHhbbt8UHgeKlDn5QVsKx%2Baq%2B5Tt8Wsd5ZYsUadbeygtnocOjuHWF6%2FcULe9UhEq5xRNp%2FW%2FccfL7TZlqpwvesvTGnBxx12nC19LvqvTFVFz7NaZ%2FT5zTdfWu%2B1jMSOYxNfDHorXt3EeBDZk5%2F4%2BbN%2BJ43uvtWYiOC36kCT%2ByduF1Qo3N6EhmxarKQJ6sl2Odv1%2FHx4s4Pfjw%3D%3D&Expires=1782911169)

## What the module is teaching

This part of the module is teaching more than RAG. It is teaching how to think like a systems builder:

- separate data preparation from answering,
- keep your pipeline modular,
- inject dependencies instead of hard-coding them,
- make code reusable,
- design for later extension. [youtube](https://www.youtube.com/watch?v=KHePGkeFn54)

That is the real learning intent behind the module. It is not only about using an LLM; it is about building a maintainable AI system. [github](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/lessons/01-intro.md)

## Note wording you can use

You can write this in your note:

> In Module 1, I learned that RAG is a pattern for answering questions using external knowledge. The system first retrieves relevant text from my data, then gives that text to the LLM so it can generate a grounded answer. The course builds this from scratch in Python so I can understand the full pipeline, not just use a framework. `ingest.py` prepares and indexes the data, while `rag_helper.py` contains reusable logic for searching, building prompts, and calling the model. `RAGBase` exists to remove reliance on globals and make the system flexible, so the search backend and LLM client can be passed in as constructor arguments and later swapped or extended. [github](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/lessons/01-intro.md)

## Study questions

These are strong questions to include in your own note or revision:

- What problem is RAG solving?
- Why does the model need retrieval instead of only generation?
- What is the role of `ingest.py`?
- What is the role of `RAGBase`?
- Why are constructor arguments better than globals?
- What parts can be swapped later?
- What is the difference between the pipeline and the backend implementation? [youtube](https://www.youtube.com/watch?v=KHePGkeFn54)

I can turn this into a **clean study note format** next, with headings, concise bullets, and a final summary you can paste directly into your workspace.