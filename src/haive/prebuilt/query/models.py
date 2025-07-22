from pydantic import BaseModel, Field


class QueryModel(BaseModel):
    """A model for a quer."""

    query: str = Field(..., descriptio="The query to be decomposed.")

    def __str__(self):
        return self.query

    def __repr__(self):
        return self.query
