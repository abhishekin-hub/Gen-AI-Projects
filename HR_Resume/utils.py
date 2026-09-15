import glob
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
# from langchain.vectorstore import Pinecone


load_dotenv()

#Constants
MODEL_NAME = "gpt-5-mini"
TEMPERATURE = 0.2
MAX_TOKEN = 4096

LLM = ChatOpenAI(
    model_name=MODEL_NAME,
    temperature=TEMPERATURE,
    max_tokens = MAX_TOKEN
)

TEMPLATE = """You are an HR assistant. You match resumes for the job requirements provided by the HR.
You prioritize on matching skills and project experience.
You respond with the best matchs for the number of job openings : {Quantity}.

Note: If the match is not found, just reply resume profiles don't match.

Job Requirements: {Requirements}

Candidate Resumes:
{Context}

Answer:
"""

prompt = PromptTemplate(
    template = TEMPLATE,
    input_variables = ["Requirements", "Quantity", "Context"]
)

def get_pdf_text(pdf_file):
    text_extracted = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text_extracted += page.extract_text()
    return text_extracted

def create_docs(folder_path=None, uploaded_files=None):
    docs = []
    if folder_path:
        for filename in glob.glob(os.path.join(folder_path, "*.pdf")):
            texts = get_pdf_text(filename)
            # Adding it into our docs list and further adding some metadata for reference
            docs.append(Document(
                page_content=texts,
                metadata={"name":os.path.basename(filename), "id":None, "type":"pdf", "size":os.path.getsize(filename)}
            ))
    if uploaded_files:
        for file in uploaded_files:
            texts = get_pdf_text(file)
            docs.append(Document(
                page_content=texts,
                metadata={"name":file.name, "id":file.file_id, "type":file.type, "size":file.size}
            ))

    return docs

def create_chunks(docs):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    text_chunks = text_splitter.split_documents(docs)
    return text_chunks

def create_embeddings() :
    embeddings = OpenAIEmbeddings() # Seems outdated on June 2026, Need to check
    return embeddings

def vectorstore(docs):
    db = Chroma.from_documents(documents=create_chunks(docs), embedding=create_embeddings())
    return db

def process(resume_folder, uploaded_files,job_description,no_of_jobs):
    text = create_docs(resume_folder, uploaded_files)
    db = vectorstore(text)

    relevant_docs = db.similarity_search_with_score(job_description, k=no_of_jobs)
    
    # Flatten retrieved (Document, score) tuples into plain text for the prompt
    context_text = "\n\n".join(
        f"Resume: {doc.metadata.get('name')}\n{doc.page_content}"
        for doc, score in relevant_docs
    )

    chain = prompt | LLM
    response = chain.invoke({
        "Requirements": job_description,
        "Quantity": no_of_jobs,
        "Context": context_text
        #Context="\n".join([doc.page_content for doc, _ in relevant_docs])
    })
    
    return response.content
    
