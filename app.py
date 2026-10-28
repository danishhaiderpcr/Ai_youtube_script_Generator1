import os
from datetime import datetime

import streamlit as st
from google import genai
from google.genai import types

APP_TITLE = "AI YouTube Script Generator"
DEFAULT_MODEL = "gemini-3.8-flash"

def get_api_key() -> str | None:
    """Read the Gemini key from Streamlit Secrets or an environment variable."""
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        secret_key = ""
    return secret_key or os.getenv("GEMINI_API_KEY", "")


def validate_inputs(topic: str, niche: str, audience: str) -> list[str]:
    """Return validation messages for required fields."""
    errors = []
    if not topic.strip():
        errors.append("Please enter a video topic.")
    if not niche.strip():
        errors.append("Please enter a channel niche.")
    if not audience.strip():
        errors.append("Please describe your target audience.")
    if len(topic.strip()) > 500:
        errors.append("Keep the topic under 500 characters.")
    if len(niche.strip()) > 150:
        errors.append("Keep the niche under 150 characters.")
    if len(audience.strip()) > 250:
        errors.append("Keep the audience description under 250 characters.")
    return errors


def build_prompt(
    topic: str,
    niche: str,
    audience: str,
    language: str,
    duration: str,
    tone: str,
    extra_instructions: str,
) -> str:
    """Create the instruction sent to Gemini."""
    extra = extra_instructions.strip() or "None"
    return f"""
You are a skilled YouTube scriptwriter and content strategist.
Create original content based on the following brief.

VIDEO BRIEF
- Topic: {topic.strip()}
- Channel niche: {niche.strip()}
- Target audience: {audience.strip()}
- Language: {language}
- Target duration: {duration}
- Tone: {tone}
- Additional instructions: {extra}

Return the result using these exact section headings:
1. VIDEO TITLE IDEAS
   - Give 5 distinct, accurate, catchy titles. Avoid misleading clickbait.
2. OPENING HOOKS
   - Give 3 short hooks designed for the first 5–15 seconds.
3. FULL VIDEO SCRIPT
   - Write an original, speakable script suitable for the target duration.
   - Include a strong opening, logically ordered main points, transitions, and a useful ending.
   - Add brief [VISUAL SUGGESTION: ...] cues only when helpful.
   - Do not claim invented facts or statistics are verified. Flag any fact that needs checking.
4. VIDEO DESCRIPTION
   - Write a useful YouTube description with a clear summary and a natural call to action.
5. HASHTAGS
   - Give 8–12 relevant hashtags, avoiding unrelated trending tags.
6. THUMBNAIL CONCEPTS
   - Give 3 concepts. For each, describe the visual, short overlay text (maximum 5 words), and the main focal point.
7. CALLS TO ACTION
   - Give 3 natural CTA options (for example, subscribe, comment, or watch another video).

Make the output well organized and ready for the creator to edit.
Do not promise views, virality, or ranking. Do not copy existing scripts or copyrighted passages.
""".strip()


def generate_content(api_key: str, model: str, prompt: str) -> str:
    """Call the Gemini API and return generated text."""
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,
            max_output_tokens=7000,
        ),
    )
    text = response.text
    if not text or not text.strip():
        raise ValueError(
            "Gemini returned an empty response. Try again or use a shorter topic."
        )
    return text.strip()


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🎬",
        layout="wide",
    )

    st.title("🎬 AI YouTube Script Generator")
    st.write(
        "Create original video scripts, title ideas, hooks, descriptions, "
        "hashtags, thumbnail concepts, and calls to action."
    )
    st.caption(
        "AI-generated content is a draft. Review facts, names, claims, and "
        "copyright considerations before publishing."
    )

    with st.sidebar:
        st.header("Generation settings")
        language = st.selectbox(
            "Output language",
            ["English", "Urdu", "Roman Urdu", "Spanish", "Arabic", "Hindi", "Other"],
        )
        duration = st.selectbox(
            "Target video duration",
            ["Short (under 60 seconds)", "3–5 minutes", "5–8 minutes", "8–12 minutes", "15+ minutes"],
            index=2,
        )
        tone = st.selectbox(
            "Video tone",
            ["Educational", "Friendly and conversational", "Funny", "Documentary", "Motivational", "Professional", "Storytelling"],
        )
        model = st.text_input(
            "Gemini model ID",
            value=DEFAULT_MODEL,
            help="Uses the current Gemini Flash alias by default. Change only if your API account supports another model ID.",
        ).strip() or DEFAULT_MODEL

    left, right = st.columns([1, 1])
    with left:
        topic = st.text_input(
            "Video topic *",
            placeholder="e.g., 7 useful English phrases for daily life",
            max_chars=500,
        )
        niche = st.text_input(
            "Channel niche *",
            placeholder="e.g., English learning, technology, travel",
            max_chars=150,
        )
    with right:
        audience = st.text_input(
            "Target audience *",
            placeholder="e.g., beginner English learners aged 15+",
            max_chars=250,
        )
        extra_instructions = st.text_area(
            "Extra instructions (optional)",
            placeholder="e.g., Include examples, keep the language simple, add scene cues.",
            height=100,
            max_chars=1500,
        )

    st.caption("* Required fields")

    if st.button("✨ Generate YouTube Content", type="primary", use_container_width=True):
        errors = validate_inputs(topic, niche, audience)
        if errors:
            for error in errors:
                st.error(error)
        else:
            api_key = get_api_key()
            if not api_key:
                st.error(
                    "Gemini API key not found. Add GEMINI_API_KEY to "
                    "Streamlit Secrets or your environment variables."
                )
                st.info(
                    "For local use, set GEMINI_API_KEY in your environment. "
                    "For deployment, add it in Streamlit Community Cloud → "
                    "App settings → Secrets."
                )
            else:
                prompt = build_prompt(
                    topic, niche, audience, language, duration, tone, extra_instructions
                )
                try:
                    with st.spinner("Creating your YouTube content..."):
                        result = generate_content(api_key, model, prompt)
                    st.session_state["generated_content"] = result
                    st.session_state["generated_topic"] = topic.strip()
                    st.success("Content generated. Review it before publishing.")
                except Exception as exc:
                    # Keep user-facing errors helpful without displaying credentials.
                    st.error(
                        "The content could not be generated. Check your internet "
                        "connection, API key, model ID, and Gemini API quota, then try again."
                    )
                    st.caption(f"Technical detail: {type(exc).__name__}: {exc}")

    generated_content = st.session_state.get("generated_content")
    if generated_content:
        st.divider()
        st.subheader("Your YouTube content")
        st.text_area(
            "Generated draft",
            value=generated_content,
            height=600,
            help="You can select and copy this text to edit it.",
        )
        safe_topic = "".join(
            char.lower() if char.isalnum() else "_" for char in st.session_state.get("generated_topic", "youtube_script")
        ).strip("_")[:50] or "youtube_script"
        filename = f"{safe_topic}_content.txt"
        st.download_button(
            label="⬇️ Download content as TXT",
            data=generated_content,
            file_name=filename,
            mime="text/plain",
            use_container_width=True,
        )
        st.caption(
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}. "
            "Please fact-check claims and adapt the script to your own voice."
        )


if __name__ == "__main__":
    main()
