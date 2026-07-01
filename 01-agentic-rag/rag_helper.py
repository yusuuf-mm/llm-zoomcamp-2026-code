"""
RAG pipeline helper module.

This module provides a reusable, dependency-injected class for
Retrieval-Augmented Generation. It encapsulates the search, prompt-building,
and LLM-calling logic so that notebooks and applications can instantiate
multiple RAG assistants with different backends without rewriting code.

Constants:
    INSTRUCTIONS: Default system-level instructions for the LLM.
    USER_PROMPT_TEMPLATE: Default template for formatting the user prompt.

Classes:
    RAGBase: The main orchestrator class that wires search, prompt, and LLM.
"""

INSTRUCTIONS = """
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
"""

USER_PROMPT_TEMPLATE = """
Question:
{question}

Context:
{context}
"""


class RAGBase:
    """
    Modular RAG orchestrator that uses dependency injection.

    Instead of hard-coding a specific search index or LLM client inside
    the methods, both are passed in at construction time. This makes the
    class:
      - Testable: you can inject fake indexes/clients for unit tests.
      - Swappable: swap minsearch for sqlitesearch without changing pipeline logic.
      - Reusable: instantiate multiple assistants for different courses/models.

    Attributes:
        index: A search backend that implements .search(query, ...).
        llm_client: An OpenAI-compatible client with .responses.create(...).
        instructions (str): System-level behavior for the LLM.
        prompt_template (str): Template string with {question} and {context}.
        course (str): Default course filter applied during search.
        model (str): Default model identifier for LLM calls.
    """

    def __init__(
        self,
        index,
        llm_client,
        instructions=INSTRUCTIONS,
        prompt_template=USER_PROMPT_TEMPLATE,
        course="llm-zoomcamp",
        model="nvidia/nemotron-3-ultra-550b-a55b:free"
    ):
        """
        Initialize the RAG assistant with its dependencies.

        Args:
            index: Search index object (minsearch, sqlitesearch, etc.).
            llm_client: OpenAI-compatible API client.
            instructions: System prompt telling the LLM how to behave.
            prompt_template: Reusable template for the user prompt.
            course: Course slug used to filter search results.
            model: Model name/ID passed to the LLM provider.
        """
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.course = course
        self.prompt_template = prompt_template
        self.model = model

    def search(self, query, num_results=5):
        """
        Retrieve the most relevant documents for a user query.

        This method delegates to the injected search index, applying
        field boosting and course filtering. The exact backend (minsearch,
        sqlitesearch, Elasticsearch, etc.) is hidden behind the index
        interface, so it can be swapped without touching this method.

        Args:
            query (str): The user's raw question.
            num_results (int): Maximum number of documents to return.

        Returns:
            list[dict]: Ranked search results, each containing at least
            section, question, answer, and course fields.
        """
        boost_dict = {"question": 3.0, "section": 0.5}
        filter_dict = {"course": self.course}

        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
            filter_dict=filter_dict
        )

    def build_context(self, search_results):
        """
        Convert search results into a single context string for the LLM.

        The LLM cannot read raw Python dictionaries, so we serialize the
        top-k documents into a readable text block. Each document is
        formatted with its section, question, and answer.

        Args:
            search_results (list[dict]): Output from self.search().

        Returns:
            str: A single string containing all retrieved documents,
            separated by blank lines.
        """
        lines = []

        for doc in search_results:
            lines.append(doc["section"])
            lines.append("Q: " + doc["question"])
            lines.append("A: " + doc["answer"])
            lines.append("")

        return "\n".join(lines).strip()

    def build_prompt(self, query, search_results):
        """
        Assemble the final user prompt from the query and search results.

        This is the literal bridge between retrieval and generation. It
        formats the evidence (context) and the question into a prompt
        the LLM can act on.

        Args:
            query (str): The user's question.
            search_results (list[dict]): Output from self.search().

        Returns:
            str: The interpolated user prompt ready for the LLM.
        """
        context = self.build_context(search_results)
        return self.prompt_template.format(
            question=query, context=context
        )

    def llm(self, prompt):
        """
        Send the composed prompt to the LLM provider and return the answer.

        The request uses the Responses API with a two-message history:
        - A developer message (system instructions)
        - A user message (question + retrieved context)

        Args:
            prompt (str): The fully assembled user prompt.

        Returns:
            str: The generated answer text from the LLM.
        """
        input_messages = [
            {"role": "developer", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]

        response = self.llm_client.responses.create(
            model=self.model,
            input=input_messages,
            max_output_tokens=1000
        )

        return response.output_text

    def rag(self, query):
        """
        Run the full RAG pipeline for a single user query.

        This is the main entry point. It chains search, prompt building,
        and LLM generation into one call. External code (notebooks, APIs,
        agents) only needs to call this method.

        Args:
            query (str): The user's question.

        Returns:
            str: The grounded answer generated by the LLM.
        """
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        answer = self.llm(prompt)
        return answer