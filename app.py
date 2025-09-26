import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader




from langchain_community.document_loaders import YoutubeLoader
import re
from langchain.schema import Document as documo

from youtube_transcript_api import YouTubeTranscriptApi


def _vid(url: str):
    m = re.search(r"(?:v=|youtu\.be/|/shorts/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else None

def load_youtube_safe(youtube_url: str):
    try:
        video_id = _vid(youtube_url)
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)

        # is iterable
        s=""
        for snippet in fetched_transcript:
            # print(snippet.text)
            s=s+" "+snippet.text

        # print("****")
        # print(len(s))

        # print(s)
        print(len(s))

        return [documo(page_content=s, metadata={"source": youtube_url, "status": "transcripts"})]


        


        loader = YoutubeLoader.from_youtube_url(
            youtube_url,
            add_video_info=False,   # skip pytube metadata
            language=["en", "en-US"]
        )
        docs= loader.load()       # returns [Document(...), ...]
        print(docs)
        return docs
    except Exception as e:
        from langchain.schema import Document
        msg = f"Unable to return the transcripts of the video because of this error: {e}"
        return [Document(page_content=msg, metadata={"source": youtube_url, "status": "error"})]




## sstreamlit APP
st.set_page_config(page_title="Summarize Text From a Website or Youtube Video", page_icon="📜")
st.title("Summarize Text From a Website or Youtube Video")
st.subheader('Summarize URL')

groq_api_key=""

## Get the Groq API Key and url(YT or website)to be summarized
with st.sidebar:
    groq_api_key=st.text_input("Groq API Key",value="",type="password")

if groq_api_key=="":
    st.info("Please add your Groq APPI key to continue")
    st.stop()    

generic_url=st.text_input("URL",label_visibility="collapsed")

## Gemma Model USsing Groq API
llm =ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)

prompt_template="""
Provide a summary of the following content in 300 words:
Content:{text}

"""
prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

if st.button("Summarize the Content from YT or Website"):
    ## Validate all the inputs
    if groq_api_key=="":
        st.error("Please provide the information to get started")
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid Url. It can may be a YT video utl or website url")

    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the website or yt video data
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    try:
                        # loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)
                        # docs= load_youtube_safe("https://www.youtube.com/watch?v=JcVHf4X_dqY")
                        docs= load_youtube_safe(generic_url)
                        # print(docs)
                    except Exception as e:
                        st.exception(f"Exception:{e}")
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                    docs=loader.load()

                # print(docs)

                #################

                from langchain.text_splitter import TokenTextSplitter

                # Combine all document contents
                full_text = " ".join([doc.page_content for doc in docs])

                # Define max tokens you want to allow
                MAX_TOKENS = 9000  

                # Initialize splitter
                token_splitter = TokenTextSplitter(chunk_size=MAX_TOKENS, chunk_overlap=0)

                # Split into token-based chunks
                chunks = token_splitter.split_text(full_text)

                # Keep only up to the max tokens worth of content
                trimmed_text = chunks[0]  # take the first chunk only

                # Count tokens
                num_tokens = len(token_splitter.split_text(trimmed_text))
                st.write(f"Document trimmed(max {MAX_TOKENS})")

                # Replace docs with trimmed one for summarization
                from langchain.schema import Document
                docs = [Document(page_content=trimmed_text)]

                #################

                

                ## Chain For Summarization
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception:{e}")
                    