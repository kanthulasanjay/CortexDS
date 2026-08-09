from langchain_chroma import Chroma

from rag.embeddings import embedding_model


class Retriever:

    def search(

        self,

        query,

        k=5

    ):

        db = Chroma(

            persist_directory="vector_db",

            embedding_function=embedding_model()

        )

        docs = db.similarity_search(

            query,

            k=k

        )

        return docs