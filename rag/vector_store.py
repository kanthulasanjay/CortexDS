from langchain_chroma import Chroma

from rag.embeddings import embedding_model


class VectorDatabase:

    def build(self, chunks):

        db = Chroma.from_documents(

            chunks,

            embedding_model(),

            persist_directory="vector_db"

        )

        return db