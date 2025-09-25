import random, string, hashlib, time
from abc import ABC, abstractmethod


class ShortCodeGenerator(ABC):
    @abstractmethod
    def generate(self, length: int = 6) -> str:
        raise NotImplementedError


class RandomAlphaNumGenerator(ShortCodeGenerator):
    def generate(self, length: int = 6) -> str:
        chars = string.ascii_letters + string.digits
        return "".join(random.choices(chars, k=length))


class HexHashGenerator(ShortCodeGenerator):
    def generate(self, length: int = 6) -> str:
        s = f"{time.time_ns()}{random.random()}"
        h = hashlib.sha256(s.encode()).hexdigest()
        return h[:length]


class ShortCodeFactory:
    @staticmethod
    def create(generator_type: str = "random") -> ShortCodeGenerator:
        if generator_type == "random":
            return RandomAlphaNumGenerator()
        elif generator_type == "hex":
            return HexHashGenerator()
        return RandomAlphaNumGenerator()
