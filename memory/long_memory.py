import os
import json
import logging


logger = logging.getLogger(__name__)


class LongTermMemory:

    def __init__(self, path="memory/experiences.json"):

        self.path = path

        # Create memory directory
        os.makedirs(
            os.path.dirname(self.path),
            exist_ok=True
        )

        # Create memory file if it doesn't exist
        if not os.path.exists(self.path):

            self._create_empty_memory()


    # ==================================================
    # CREATE EMPTY MEMORY
    # ==================================================

    def _create_empty_memory(self):

        try:

            with open(
                self.path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    [],
                    f,
                    indent=4
                )

        except Exception as e:

            logger.error(
                "Could not create memory file: %s",
                e
            )


    # ==================================================
    # LOAD MEMORY
    # ==================================================

    def load(self):

        try:

            # File doesn't exist
            if not os.path.exists(self.path):

                self._create_empty_memory()

                return []


            # File is empty
            if os.path.getsize(self.path) == 0:

                logger.warning(
                    "Memory file is empty. Resetting."
                )

                self._create_empty_memory()

                return []


            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)


            # JSON must be a list
            if not isinstance(data, list):

                logger.warning(
                    "Memory JSON is not a list. Resetting."
                )

                self._create_empty_memory()

                return []


            return data


        except json.JSONDecodeError:

            logger.warning(
                "Invalid JSON memory file. Resetting."
            )

            self._create_empty_memory()

            return []


        except Exception as e:

            logger.error(
                "Memory loading failed: %s",
                e
            )

            return []


    # ==================================================
    # SAVE MEMORY
    # ==================================================

    def save(self, experiences):

        try:

            with open(
                self.path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    experiences,
                    f,
                    indent=4,
                    ensure_ascii=False,
                    default=str
                )

            logger.info(
                "Memory saved successfully."
            )

            return True


        except Exception as e:

            logger.error(
                "Memory saving failed: %s",
                e
            )

            return False


    # ==================================================
    # ADD EXPERIENCE
    # ==================================================

    def add(self, experience):

        experiences = self.load()

        experiences.append(
            experience
        )

        return self.save(
            experiences
        )


    # ==================================================
    # CLEAR MEMORY
    # ==================================================

    def clear(self):

        return self.save([])


    # ==================================================
    # GET ALL EXPERIENCES
    # ==================================================

    def get_all(self):

        return self.load()