# AI Bumbling
In which I bumble around with AI apps.

# Environment Setup
I'm on MacOS and my python instance is externally managed by Homebrew, so a simple `pip install` won't work.

Here's how to get around it:
1. Use the VSCode command palette to create a new python environment.
2. Activate the environment with `source ./venv/bin/activate`.
3. Install openai package with `pip install openai`.

## Biscuit Wizard
A chat program in which a condescending wizard helps you with your biscuit baking. A combination of system prompts and tool calls make him less helpful and more judgemental than you might expect!

## Netrunner Card Generator
Generates netrunner deck lists! I use a structured prompt and inject card data to help the LLM along. Right now it doesn't engage with influence at all because bringing in cards from other factions exceeds gtp-3.5-turbo-instruct's context window.

TODO: Find a better way of compressing card data so that more cards can go in the prompt.