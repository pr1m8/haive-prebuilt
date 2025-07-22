class AcademicPaperSearchInput(BaseModel):
    topic: str = Field(..., description="The topic to search for academic papers o")
    max_results: int = Field(2, description="Maximum number of results to retur")
