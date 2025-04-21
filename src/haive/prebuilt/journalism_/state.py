
from pydantic import BaseModel


class JournalismReviewState(BaseModel):
    current_query: str
    article_text: str
    chunks: list[str]
    actions: list[str]
    summary_result: str | None
    # need to check
    fact_check_result: list[FactCheckResult] | None
    tone_analysis_result: str | None
    quote_extraction_result: str | None
    grammar_and_bias_review_result: str | None
    review_result: str | None
