from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader
)

def load_documents():

    loader = DirectoryLoader(

        "knowledge",

        glob="**/*",

        loader_cls=TextLoader,

        silent_errors=True

    )

    docs = loader.load()

    return docs