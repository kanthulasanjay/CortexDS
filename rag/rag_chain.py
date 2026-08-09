from core.llm import llm

from rag.retriever import Retriever


class RAGChain:

    def ask(self, question):

        retriever = Retriever()

        docs = retriever.search(question)

        context = "\n\n".join(

            d.page_content

            for d in docs

        )

        prompt = f"""

Answer the question using ONLY the context.

Context

{context}

Question

{question}

"""

        return llm.invoke(prompt).content