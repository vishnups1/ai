# Tool use with the Agent Developer Kit

Leveraging tools effectively is what truly distinguishes intelligent agents from basic models. A tool is a block of code, like a function or a method, that executes specific actions such as interacting with databases, making API requests, or invoking other external services.

Tools empower agents to interact with other systems and perform actions beyond their core reasoning and generation capabilities. It's crucial to note that these tools operate independently of the agent's LLM, meaning that tools do not automatically possess their own reasoning abilities.

Agent Development Kit provides developers with a diverse range of tool options:

- Pre-built Tools: Ready-to-use functionalities such as Google Search, Code Execution, and Retrieval-Augmented Generation (RAG) tools.
- Third-Party Tools: Seamless integration of tools from external libraries like LangChain
- Custom Tools: The ability to create custom tools tailored to specific requirements, by using language specific constructs and Agents-as-Tools. The SDK also provides asynchronous capabilities through Long Running Function Tools.

# Available Pre-Built Tools from Google

Google Search (google_search): Allows the agent to perform web searches using Google Search. You simply add google_search to the agent's tools.

Code Execution (built_in_code_execution): This tool allows the agent to execute code, to perform calculations, data manipulation, or interact with other systems programmatically. You can use the pre-built VertexCodeInterpreter or any code executor that implements the BaseCodeExecutor interface.

Retrieval (retrieval): A package of tools designed to fetch information from various sources.

Vertex AI Search Tool (VertexAiSearchTool): This tool integrates with Google Cloud's Vertex AI Search service to allow the agent to search through your AI Applications data stores.

```
adk_tools/
├── callback_logging.py
├── function_tool_agent
│   ├── agent.py
│   └── __init__.py
├── langchain_tool_agent
│   ├── agent.py
│   └── __init__.py
├── requirements.txt
└── vertexai_search_tool_agent
    ├── agent.py
    ├── __init__.py
    └── tools.py
```

# Use a Third-Party Tool from the LangChain Community

ADK allows you to use tools available from third-party AI frameworks like LangChain. The LangChain community has created a large number of tool integrations to access many sources of data, integrate with various web products, and accomplish many things. Using community tools within ADK can save you rewriting a tool that someone has already created.

```bash
cd ~/adk_tools
cat << EOF > langchain_tool_agent/.env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-03-036cba9ceb47
GOOGLE_CLOUD_LOCATION=global
MODEL=gemini-2.5-flash
EOF
```

# Use a function as a custom tool

When pre-built tools don't fully meet specific requirements, you can create your own tools. This allows for tailored functionality, such as connecting to proprietary databases or implementing unique algorithms.

The most straightforward way to create a new tool is to write a standard Python function with a docstring written in a standard format and pass it to your model as a tool. This approach offers flexibility and quick integration.


When writing a function to be used as a tool, there are a few important things to keep in mind:

- Parameters: Your function can accept any number of parameters, each of which can be of any JSON-serializable type (e.g., string, integer, list, dictionary). It's important to avoid setting default values for parameters, as the large language model (LLM) does not currently support interpreting them.

- Return type: The preferred return type for a Python Function Tool is a dictionary. This allows you to structure the response with key-value pairs, providing context and clarity to the LLM. For example, instead of returning a numeric error code, return a dictionary with an "error_message" key containing a human-readable explanation. As a best practice, include a "status" key in your return dictionary to indicate the overall outcome (e.g., "success", "error", "pending"), providing the LLM with a clear signal about the operation's state.

- Docstring: The docstring of your function serves as the tool's description and is sent to the LLM. Therefore, a well-written and comprehensive docstring is crucial for the LLM to understand how to use the tool effectively. Clearly explain the purpose of the function, the meaning of its parameters, and the expected return values.


## Best practices for writing functions to be used as tools include

- Fewer Parameters are Better: Minimize the number of parameters to reduce complexity.

- Use Simple Data Types: Favor primitive data types like str and int over custom classes when possible.

- Use Meaningful Names: The function's name and parameter names significantly influence how the LLM interprets and utilizes the tool. Choose names that clearly reflect the function's purpose and the meaning of its inputs.

- Break Down Complex Functions: Instead of a single update_profile(profile: Profile) function, create separate functions like update_name(name: str), update_age(age: int), etc.

- Return status: Include a "status" key in your return dictionary to indicate the overall outcome (e.g., "success", "error", "pending") to provide the LLM a clear signal about the operation's state.

# Use Vertex AI Search as a tool to ground on your own data

In this task, you will discover how easy it is to deploy a RAG application using an Agent Development Kit agent with the built-in Vertex AI Search tool from Google and the AI Applications data store you created earlier.

## Using AgentTool to integrate search tools with other tools

Search tools come with an implementation limitation in that you cannot mix search tools and non-search tools in the same agent. To get around this, you can wrap an agent with a search tool with an AgentTool, and then use that agent-as-a-tool to conduct searches alongside other tools.


```python
vertexai_search_agent = Agent(
    name="vertexai_search_agent",
    model=Gemini(model=os.getenv("MODEL"), retry_options=retry_options),
    instruction="Use your search tool to look up facts.",
    tools=[vertexai_search_tool]
)
```

```python
root_agent = Agent(
    # A unique name for the agent.
    name="root_agent",
    # The Large Language Model (LLM) that agent will use.
    model=Gemini(model=os.getenv("MODEL"), retry_options=retry_options),
    # A short description of the agent's purpose, so other agents
    # in a multi-agent system know when to call it.
    description="Answer questions using your data store access.",
    # Instructions to set the agent's behavior.
    instruction="You analyze new planet discoveries and engage with the scientific community on them.",
    # Callbacks to log the request to the agent and its response.
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    # Add the tools instructed below
    tools=[
        AgentTool(vertexai_search_agent, skip_summarization=False),
        get_date
    ]
)
```

https://github.com/google/adk-samples/tree/main/python/agents/agent-skills-tutorial