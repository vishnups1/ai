# Overview of Session, State & Runner

## Session (Stateful Message History)

A session inside of an ADK is nothing more than two major pieces of information.

- State is where you store all sort of information in a dictionary where you will have keys and values.
- Events is the message history between us and the agents. There is a tool calling and agent responses.

Sessions has few additional piece of information.

As you try to build larger agent workflows eventually we want to lookup sessions.

**Example:**

For user bob we want to see all the conversaions between him and the agent. You can look up using app_name and user_id.

- `id` 
- `app_name`
- `user_id`
- `last_update_time`

### Types Of Sessions

- InMemorySessionService
- DatabaseSessionService
- VertexAISessionService

## A runner is nothing more a collection of 2 pieces of information

- Agents  - The runner everytime it gets a request it knows what agents avaliable to handle the request.
- Session - Stores message history and state


```console
            +------------------------------------+                           +-----+
            |               Runner               |                    +----> | LLM |
            |  +-----------+     +-----------+   |      +-------+     |      +-----+
[USER] -->  |  | 2. Agents |     | 3. Session|   | -->  | Agent | --> |
            |  +-----------+     +-----------+   |      +-------+     |      +----------+
            |                                    |                    +----> | ToolCall |
            +------------------------------------+                           +----------+
```

Flow (Example: FAQ Agent)

1. [USER] hey, what the return policy for the product x?
2. [RUNNER] okay, you are user 'x', let me check the session I see you have a userID of '123' let me pick the message history and the state. It will provide all the context to the agent.
4. Runner handles the context to the appropriate agent.
3. [AGENT] okay, I can see use 'x' purchases these products etc..
4. Agent then call LLM or ToolCall and provides response.
5. Runner updates the event history and returns the response to the user.
