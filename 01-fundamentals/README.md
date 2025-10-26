## [Fundamentals](https://www.youtube.com/watch?v=ZaPbP9DwBOE)

### 1. Context Window

```bash
+++++++    ++++++++++++++++++ => Nano, Mini, Flash (low latency, fast responses, 2-4K tokens)
| LLM | => | Context Window | 
+++++++    ++++++++++++++++++ => GPT-4, Gemini Pro (1M tokens, ~750K words)
```

**Context Buffer (Conversation Memory)**

Applications or API clients maintain the full conversation history (user inputs and AI outputs) in memory, outside the model. For each API call, the client constructs a prompt using this stored data.

**Context Window Capacity (Token Limit)**

This is a fixed property of the model, determined by its architecture and training. It defines the maximum number of tokens the model can process at once, including:

- Input tokens (chat history)
- Output tokens (AI response)

Exceeding this limit results in a "Context length exceeded" error.

### 2. Embeddings & Vector Representations

```bash
++++++++++++++++++++++++    +++++++++++++++++++++++    ++++++++++++++++++++++++++
| LLM (Gemini Pro)     | => | Context Window (1M) | => | 500 GB (Internal Data) |
++++++++++++++++++++++++    +++++++++++++++++++++++    ++++++++++++++++++++++++++
```

Challenge: How can an LLM handle 500GB of company data when only a small portion fits within its context window?

Embeddings solve this problem by converting text into numerical vectors that capture semantic meaning. Instead of storing words, embeddings represent text as lists of numbers (typically around 1,536 values), reflecting relationships and similarities between concepts.

For example, "vacation" and "holiday" would have vectors close to each other, indicating similar meanings.

### 3. Langchain

With embeddings and LLMs understood, the next step is combining these elements into a working system.

```bash
                  ++++++++++++++++
Company Policy => |              | <= Conversation History
                  |              |
Product Info   => |   CHATBOT    | <= Company Knowledge
                  |              |
Support Issues => |              | <= Multistep Interaction
                  ++++++++++++++++
```

Langchain is a framework that connects data sources—like company policies, product info, and support issues—to the chatbot. It manages conversation history, retrieves relevant knowledge, and supports complex interactions, enabling context-aware responses.

Langchain provides key abstractions for building AI applications, such as:

- APIs for LLM interaction
- Memory management for conversations
- Interfaces for vector databases
- Embedding pipelines for semantic search
- Tool routing and orchestration
- State management

It also integrates with external tools, allowing connections to web search, file systems, databases, and more.

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

### 4. First API Call

**OpenAI Models**

Different models = Different AI brains. You must specify which one to pick.

- GPT-4: Most advanced, but costly
- GPT-4.1 Mini: Fast and affordable
- GPT-3.5: Older, simpler model

The openAI library provides access to these models, handling:

- API key authentication
- Sending queries to AI servers
- Receiving responses

**What is an API Client?**

The client manages connections to OpenAI, handling networking so you can focus on asking questions.

**What are chat completions?**

Chat completions are OpenAI's conversational API. You send messages and receive AI responses, similar to texting. This is done using the `client.chat.completions.create()` function.

**The three roles in the conversation**

| Role          | Description                           |
|---------------|---------------------------------------|
| **system**    | Instructions for how AI should behave |
| **user**      | That's you asking the question        |
| **assistant** | The Model response                    |

**Understanding API response object**

`response.choices[0].message.content`

| Component    | Description                                            |
|--------------|--------------------------------------------------------|
| **response** | The entire object from openAI                          |
| **choices**  | Array of possible responses (AI can generate multiple) |
| **[0]**      | Get the first choice (You do this 99% of the time)     |
| **message**  | The message object containing role and content         |
| **content**  | The actual text of the AI response                     |

### 5. Understanding AI Tokens and Economics

Tokens are the fundamental units that AI models use to process and understand text.

**Token Breakdown:**
- Simple words: 1 token (e.g., "cat", "run")
- Complex words: multiple tokens (e.g., "unbelievable" ≈ 3 tokens)
- General rule: 1 token ≈ 4 characters or 0.75 words

**Three Token Types:**

| Token Type            | Description                                  |
|-----------------------|----------------------------------------------|
| **Prompt tokens**     | The input text you send to the AI            |
| **Completion tokens** | The AI's response text                       |
| **Total tokens**      | Combined count of prompt + completion tokens |

**Pricing Structure (GPT-4o mini example):**

| Token Type    | Cost per Million | Cost per 1K |
|---------------|------------------|-------------|
| Input tokens  | $0.80            | $0.0008     |
| Output tokens | $3.20            | $0.0032     |

**Key Insight:** Output tokens cost 4x more than input tokens, making concise responses a cost-effective strategy.