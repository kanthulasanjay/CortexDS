from memory.long_memory import LongMemory


class MemoryRetriever:

    def __init__(self):

        self.memory = LongMemory()


    def search(self, query=None):

        experiences = self.memory.load()

        if not experiences:
            return []

        if query is None:
            return experiences

        query = str(query).lower()

        results = []

        for experience in experiences:

            text = str(
                experience
            ).lower()

            if query in text:

                results.append(
                    experience
                )

        return results