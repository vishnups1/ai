# Agent Development Kit

https://github.com/bhancockio/agent-development-kit-crash-course/tree/main

1. Create & Activate the virtual environment

```console
uv venv .venv/adk
```

```console
source .venv/adk/bin/activate
```

2. Install packages

```
uv pip install google-adk
uv pip install litellm
uv pip install python-dotenv
uv pip install google-generativeai
```

3. Environment Variables

```console
cd ~/adk_project
cat << EOF > my_google_search_agent/.env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=YOUR_GCP_PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
MODEL=gemini_flash_model_id
EOF
```