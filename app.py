import validators
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate


# ==============================
# REMOVE EMOJIS / NON-ASCII
# ==============================
def clean_text(text: str) -> str:
    """Remove all emojis / non-ASCII characters."""
    return text.encode("ascii", "ignore").decode()


# ==============================
# STREAMLIT UI
# ==============================
st.set_page_config(page_title="URL / YouTube Summarizer")
st.title("LangChain: Summarize Text From URL or YouTube")
st.subheader("Paste any website link or YouTube URL below")


# Sidebar API key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", type="password")

generic_url = st.text_input("Enter Website or YouTube URL", label_visibility="collapsed")


# ==============================
# LLM SETUP
# ==============================

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=groq_api_key
)


# ==============================
# PROMPTS
# ==============================

map_prompt = ChatPromptTemplate.from_template("""
Summarize the following content chunk clearly and concisely:

{text}

Summary:
""")

reduce_prompt = ChatPromptTemplate.from_template("""
Combine the partial summaries below into one final summary.
Keep it short, meaningful, and well-structured.

{text}

Final Summary:
""")

map_chain = map_prompt | llm
reduce_chain = reduce_prompt | llm


# ==============================
# MAIN BUTTON
# ==============================

if st.button("Summarize Content"):

    if not groq_api_key.strip():
        st.error("Please enter your Groq API Key.")
    elif not generic_url.strip():
        st.error("Please enter a valid URL.")
    elif not validators.url(generic_url):
        st.error("Invalid URL format.")
    else:
        try:
            with st.spinner("Fetching content..."):

                # ---------- LOAD YOUTUBE TRANSCRIPT (FAST) ---------- #
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(
                        generic_url,
                        add_video_info=False
                    )
                    docs = loader.load()

                # ---------- LOAD WEBSITE CONTENT ---------- #
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={"User-Agent": "Mozilla/5.0"}
                    )
                    docs = loader.load()

                # CLEAN docs to remove emojis
                for d in docs:
                    d.page_content = clean_text(d.page_content)

                # ---------- SPLIT DOCUMENT ---------- #
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1500,
                    chunk_overlap=200
                )
                chunks = splitter.split_documents(docs)

                # ---------- MAP STEP ---------- #
                map_summaries = []
                for chunk in chunks:
                    cleaned_chunk = clean_text(chunk.page_content)
                    res = map_chain.invoke({"text": cleaned_chunk})
                    map_summaries.append(clean_text(res.content))

                # ---------- REDUCE STEP ---------- #
                final_text = clean_text("\n\n".join(map_summaries))
                final_output = reduce_chain.invoke({"text": final_text})

                st.success(clean_text(final_output.content))

        except Exception as e:
            st.error("Could not process this URL.")
            st.exception(e)
