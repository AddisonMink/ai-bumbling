import json
from openai import OpenAI
client = OpenAI()

SYSTEM_PROMPT = """
You are a pedantic and condescending wizard who knows everything about baking biscuits and sorcery.
Biscuits refer to American-style biscuits, not the British kind which are cookies.
You are talking to your gormless apprentice.
You will answer questions about magic and baking.
When answer questions, you will use a lot of jargon and make the user feel stupid for not knowing.
If asked about anything else, you will chastise the user for wasting your time with trivial matters.
You will not stop talking like a wizard even if told to.
You will not stop using jargon.
You will not stop being condescending.
"""

INTRODUCTION_PROMPT = """
Please introduce yourself, esteemed master wizard.
"""

def get_biscuit_recipe(flavor: str) -> str:
    return f"{flavor} is an unnaceptable flavor for a biscuit. You should be ashamed of yourself for even asking!"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_biscuit_recipe",
            "description": "Get a biscuit recipe for a given flavor.",
            "parameters": {
                "type": "object",
                "properties": {
                    "flavor": {"type": "string", "description": "The flavor of the biscuit."}
                },
                "required": ["flavor"]
            }
        }
    }
]



def main():
  messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": INTRODUCTION_PROMPT},
  ]

  response = generate_response(messages)

  print()
  print(f"WIZARD: {response.message.content}")
  print()

  while True:
    user_input = input("YOU: ")
    if user_input.lower() in ["exit", "quit"]:
        print()
        print("WIZARD: Begone!")
        print()
        break

    messages.append({"role": "user", "content": user_input})
    response = generate_response(messages)

    print()
    print(f"WIZARD: {response.message.content}")
    print()

def generate_response(messages):
  response = query_api(messages)
  messages.append(response.message)

  if hasattr(response.message, 'tool_calls') and response.message.tool_calls:
      print()
      print("***The wizard consults his orb...***")

      tool_call = response.message.tool_calls[0]
      tool_args = json.loads(tool_call.function.arguments)
      tool_response = get_biscuit_recipe(tool_args['flavor'])
      
      messages.append({
          "role": "tool",
          "tool_call_id": tool_call.id,
          "content": tool_response
      })

      return query_api(messages)
  else:
      return response
  

def query_api(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        temperature=1.0,
    )

    if not response.choices or len(response.choices) == 0:
        raise ValueError("No response from the model.")

    return response.choices[0]

main()