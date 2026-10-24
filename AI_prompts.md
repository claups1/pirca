# AI Prompts Log

## Prompt 1

`Today we will be working in folder final project. Create AI_prompts.md at the start of the assignment and keep it updated as you work . This file is the log of what I typed to you`

## Prompt 2 — Project setup

`we are going to create`

```
MGT 409 final project: "Pirca", an AI agent app that helps small shop owners in Piura, Peru prepare their business for El Niño costero rains and floods.
Setup:

* Python only (no Node). FastAPI backend that also serves a plain HTML/CSS/JS frontend.
* Create a local .venv in this folder and a requirements.txt (fastapi, uvicorn, openai, python-dotenv, pydantic, pytest).
* Load .env from this folder first, then one level above it. Never print or log the key.
* Model: gpt-6-luna through Portkey, using PORTKEY_API_KEY, base_url https://api.portkey.ai/v1, header x-portkey-provider: openai. Put the model name in one config file.
* Make one tiny test call to confirm the key and model work, and print only "OK" plus the token usage.
* Add .gitignore (.env, .venv, pycache, plans/* except plans/examples/), a .env.example with PORTKEY_API_KEY= and no value, and git init.
* Folder layout: backend/ (agents, tools, prompts, API), frontend/, data/, plans/examples/, tests/, output/.
```

## Prompt 3 — Git safe directory

`Yes, add Final Project as a git safe.directory in my global config.`

## Prompt 4 — First commit

`Commit the working tree changes with a sensible message.`
