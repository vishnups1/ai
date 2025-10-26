## [Fundamentals](https://www.youtube.com/watch?v=ZaPbP9DwBOE)

### 1. Context Window

```bash
+++++++    ++++++++++++++++++ => Nano, Mini, Flash (low latency, fast responses, 2-4K tokens)
| LLM | => | Context Window | 
+++++++    ++++++++++++++++++ => GPT-4, Gemini Pro (1M tokens, ~750K words)
```

**Context Buffer (Conversation Memory)**

The application or API client handles conversation storage. It keeps the complete chat history (user inputs + AI outputs) in memory outside the model. For each API request, the application builds a prompt that includes this stored conversation data.

**Context Window Capacity (Token Limit)**

A fixed model characteristic defined by its design and training process. It sets the maximum number of tokens the model can handle at once, including:

- Input tokens (chat history)
- Output tokens (AI response)

Going beyond this limit triggers a "Context length exceeded" error.

### 2. Embeddings & Vector Representations

```bash
++++++++++++++++++++++++    +++++++++++++++++++++++    ++++++++++++++++++++++++++
| LLM (Gemini Pro)     | => | Context Window (1M) | => | 500 GB (Internal Data) |
++++++++++++++++++++++++    +++++++++++++++++++++++    ++++++++++++++++++++++++++
```

Problem: How can an LLM process 500GB of company data when only a tiny portion fits within the context window constraints?

Embeddings provide the solution. They fundamentally change how we represent information. Rather than storing text as words, embeddings convert them into meaningful numerical vectors. This transformation captures semantic relationships and similarity between concepts.

An embedding model converts text into a numerical vector — typically a list of around 1,536 values — that captures the meaning of the text.

Example: the words "vacation" and "holiday" would be represented by vectors that are mathematically close to each other, since they have similar meanings.

### 3. Langchain

With an understanding of embeddings and LLMs, the next step is integrating these components into a cohesive system.

```bash
                  ++++++++++++++++
Company Policy => |              | <= Conversation History
                  |              |
Product Info   => |   CHATBOT    | <= Company Knowledge
                  |              |
Support Issues => |              | <= Multistep Interaction
                  ++++++++++++++++
```

Langchain acts as the framework that connects various data sources—such as company policies, product information, and support issues—with the chatbot. It manages conversation history, retrieves relevant knowledge, and enables complex, multistep interactions, allowing the chatbot to deliver informed and context-aware responses.

Langchain is a well established abstraction layer which helps you to build AI agents with minimal code.

Langchain provides essential abstractions for building AI applications, including:

- APIs for interacting with LLMs
- Memory management for conversation history
- Interfaces for vector databases
- Embedding pipelines for semantic search
- Tool routing and orchestration
- State management

Additionally, Langchain supports integration with external tools, enabling connections to web search, local file systems, databases, and more.

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

llm = ChatOpenAI(model="gpt-3.5-turbo")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
embedding = OpenAIEmbeddings()
db = Chroma(collection_name="techops_docs", embedding_function=embedding)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=db.as_retriever(),
    memory=memory
)

response = qa_chain.run("What's company's customer data policy?")
print(response)
```