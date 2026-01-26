# 03-litellm-agent

- Refer https://github.com/bhancockio/agent-development-kit-crash-course/blob/main/3-litellm-agent/README.md

- [OpenRouter](https://openrouter.ai/)

- [Litellm](https://www.litellm.ai/)

- https://docs.litellm.ai/docs/providers/openrouter


```python
model = LiteLlm(
    model="openrouter/openai/gpt-4.1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
```