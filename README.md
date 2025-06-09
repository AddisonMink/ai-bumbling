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
I use RAG based on vector embeddings to get GPT-3.5-Turbo-Instruct to generate decklists for the Netrunner card game.

1. Get the card data and embedding for whatever identity card you're using.
2. Fetch all cards from the identity's faction.
3. Fetch all cards from outside the identity's faction.
4. Get the top `n` most relevant non-faction cards based on the identity embedding.
5. Strip down all the card data to be as minimal possible.
6. Inject card data into a prompt and ask the LLM to create a netrunner deck.

### Results
The program doesn't always create legal netrunner decks, and the model doesn't have enough context to consider all relevant cards.

The big problems I ran into:
* There's a lot of cards to consider. Even using vector embeddings to filter for relevance doesn't allow me to fit all the necessary cards into the prompt.
* There's a lot of counting involved in making a legal netrunner deck. Maximum deck size, influence points, and per-card limits are difficult for the LLM to keep track of.

The positives:
* The model is able to create coherent (if not legal or good) decks and explain why it picked the cards it did.

I'm not sure GPT-3.5-Turbo-Instruct can do this task. With the context window as small as it is, I think the model itself would need fine-tuning. I don't know how to do that, so the experiment ends here for now.