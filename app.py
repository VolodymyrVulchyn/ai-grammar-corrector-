
import os
import gradio as gr
from groq import Groq

MODEL_NAME = "openai/gpt-oss-20b"

def correct_grammar(text):
    if not text.strip():
        return "Please enter some text."

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "API key is not configured."

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an English grammar corrector. "
                    "Correct grammar, spelling and punctuation mistakes. "
                    "Preserve the original meaning of the text. "
                    "Return only the corrected text without explanations "
                    "or introductory phrases."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.1,
        max_completion_tokens=300
    )

    return response.choices[0].message.content.strip()

with gr.Blocks(title="AI Grammar Corrector") as demo:
    gr.Markdown("# AI Grammar Corrector")
    gr.Markdown(
        "Enter your English text and correct grammar, "
        "spelling and punctuation using AI."
    )

    input_text = gr.Textbox(
        label="Your English Text",
        placeholder="Enter text with grammar mistakes...",
        lines=5
    )

    correct_button = gr.Button(
        "Correct Grammar",
        variant="primary"
    )

    output_text = gr.Textbox(
        label="Corrected Text",
        lines=5,
        interactive=False
    )

    correct_button.click(
        fn=correct_grammar,
        inputs=input_text,
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 10000)))
