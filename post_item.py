from dataclasses import dataclass
from datetime import datetime

@dataclass
class PostItem:
    source_text: str
    post_text: str
    time_element: str
    post_link: str
    h_secret: str = " _69_ "

    def __str__(self):
        return f"{self.source_text}{self.h_secret}{self.post_text}{self.h_secret}{self.time_element}{self.h_secret}{self.post_link}"

    def __hash__(self):
        return hash((self.source_text, self.post_text, self.time_element, self.post_link))

    @classmethod
    def from_string(cls, string: str):
        parts = string.split(cls.h_secret)
        if len(parts) != 4:
            raise ValueError(f"Invalid string format. Expected 4 parts separated by '{cls.h_secret}'")
        return cls(
            source_text=parts[0],
            post_text=parts[1],
            time_element=parts[2],
            post_link=parts[3]
        )