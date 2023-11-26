# генератор уникального id
import uuid


class UniqueGenerator:

    def generate_unique_id(self) -> str:
        return str(uuid.uuid4())

    def generate_unique_id_with_str(self, value: str) -> str:
        return (f"{self.generate_unique_id()}{value}")


def unique_hash(self) -> str:
    return UniqueGenerator.generate_unique_id()


def unique_thread_name(value: str) -> str:
    return UniqueGenerator.generate_unique_id_with_str(value=value)
