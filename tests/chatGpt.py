from openai import OpenAI
client = OpenAI(
    # This is the default and can be omitted
    api_key= "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",
)
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)