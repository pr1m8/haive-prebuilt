import importlib
import re
import unicodedata

from pydantic import BaseModel, ValidationError, validate_call
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
from spellchecker import SpellChecker


# ==================== Pydantic Models ====================
class SecurityAnalysis(BaseModel):
    non_latin: bool
    zero_width: bool
    bidi_chars: bool
    control_chars: bool
    numeric_encoding: list[str]
    scattered_text: bool
    suspicious_newlines: bool
    markdown_injection: bool
    substitution_rules: list[tuple[str, str]]
    mixed_case_evasion: bool


class SpellCheckResult(BaseModel):
    misspelled: list[str]
    suggestions: dict[str, list[str]]


class LanguageDetectionResult(BaseModel):
    detected_language: str
    confidence: float | None = None
    method: str


class ContentAnalysisResult(BaseModel):
    content: str
    language: LanguageDetectionResult
    security: SecurityAnalysis
    programming_language: str | None = None
    spell_check: SpellCheckResult
    is_profane: bool


# ==================== Implementation ====================
class LanguageDetector:
    ZERO_WIDTH_REGEX = re.compile(r"[\u200B-\u200D\uFEFF]")
    BIDI_REGEX = re.compile(r"[\u202A-\u202E]")
    CONTROL_CHAR_REGEX = re.compile(r"[\x00-\x1F\x7F-\x9F]")
    NUMERIC_ENCODING_REGEX = re.compile(r"\b\d{2,3}(?: \d{2,3})+\b")

    def __init__(self):
        """  Init  .
"""
        self.spell = SpellChecker()
        self.spell.word_frequency.load_words(["pydantic", "pygments"])

    @validate_call
    def detect_language(self, text: str, method: str) -> LanguageDetectionResult:
        """Detect Language.

Args:
    text: [TODO: Add description]
    method: [TODO: Add description]

Returns:
    [TODO: Add return description]
"""
        try:
            if method == "cld3":
                gcld3 = importlib.import_module("gcld3")
                detector = gcld3.NNetLanguageIdentifier(
                    min_num_bytes=0, max_num_bytes=1000
                )
                result = detector.FindLanguage(text)
                return LanguageDetectionResult(
                    detected_language=result.language,
                    confidence=result.probability,
                    method=method,
                )
            if method == "langid":
                langid = importlib.import_module("langid")
                lang, confidence = langid.classify(text)
                return LanguageDetectionResult(
                    detected_language=lang, confidence=confidence, method=method
                )
            if method == "langdetect":
                langdetect = importlib.import_module("langdetect")
                lang = langdetect.detect(text)
                return LanguageDetectionResult(detected_language=lang, method=method)
            raise ValueError(f"Unsupported detection method: {method}")
        except ImportError as e:
            raise RuntimeError(f"Missing dependency for {method}: {e!s}")

    @validate_call
    def analyze_security(self, text: str) -> SecurityAnalysis:
        """Analyze Security.

Args:
    text: [TODO: Add description]

Returns:
    [TODO: Add return description]
"""
        return SecurityAnalysis(
            non_latin=self._contains_non_latin(text),
            zero_width=bool(self.ZERO_WIDTH_REGEX.search(text)),
            bidi_chars=bool(self.BIDI_REGEX.search(text)),
            control_chars=bool(self.CONTROL_CHAR_REGEX.search(text)),
            numeric_encoding=self._detect_numeric_encoding(text),
            scattered_text=self._detect_scattered_text(text),
            suspicious_newlines=text.count("\n") > 10,
            markdown_injection=bool(re.search(r"``````", text, re.DOTALL)),
            substitution_rules=re.findall(r"(\b\b)\s*=\s*(\b\b)", text, re.IGNORECASE),
            mixed_case_evasion=self._detect_mixed_case(text),
        )

    @validate_call
    def detect_programming_language(self, text: str) -> str | None:
        """Detect Programming Language.

Args:
    text: [TODO: Add description]

Returns:
    [TODO: Add return description]
"""
        try:
            return guess_lexer(text).name
        except ClassNotFound:
            return None

    @validate_call
    def check_profanity(self, text: str) -> bool:
        """Check Profanity.

Args:
    text: [TODO: Add description]

Returns:
    [TODO: Add return description]
"""
        for module in ["profanity_check", "better_profanity"]:
            try:
                checker = importlib.import_module(module)
                if hasattr(checker, "predict"):
                    return bool(checker.predict([text])[0])
                if hasattr(checker, "contains_profanity"):
                    return checker.contains_profanity(text)
            except ImportError:
                continue
        return False

    def _contains_non_latin(self, text: str) -> bool:
        for char in text:
            if char.isalpha() and not unicodedata.name(char).startswith("LATIN"):
                return True
        return False

    def _detect_numeric_encoding(self, text: str) -> list[str]:
        return [
            self._decode_numbers(m) for m in self.NUMERIC_ENCODING_REGEX.findall(text)
        ]

    def _detect_scattered_text(self, text: str) -> bool:
        return any(len(line.strip()) == 1 for line in text.split("\n"))

    def _detect_mixed_case(self, text: str) -> bool:
        return any(c.islower() and c.upper() in text for c in text) or any(
            c.isupper() and c.lower() in text for c in text
        )

    @staticmethod
    def _decode_numbers(number_str: str) -> str:
        try:
            return "".join(chr(int(n)) for n in number_str.split())
        except ValueError:
            return number_str


class ContentAnalyzer:
    def __init__(self):
        """  Init  .
"""
        self.detector = LanguageDetector()

    @validate_call
    def full_analysis(
        self, text: str, lang_method: str = "cld3"
    ) -> ContentAnalysisResult:
        """Full Analysis.

Args:
    text: [TODO: Add description]
    lang_method: [TODO: Add description]

Returns:
    [TODO: Add return description]
"""
        lang_result = self.detector.detect_language(text, lang_method)
        misspelled = list(self.detector.spell.unknown(text.split()))

        suggestions = {
            w: (
                list(self.detector.spell.candidates(w))
                if self.detector.spell.candidates(w) is not None
                else []
            )
            for w in misspelled
        }

        return ContentAnalysisResult(
            content=text,
            language=lang_result,
            security=self.detector.analyze_security(text),
            programming_language=self.detector.detect_programming_language(text),
            spell_check=SpellCheckResult(
                misspelled=misspelled, suggestions=suggestions
            ),
            is_profane=self.detector.check_profanity(text),
        )


# ==================== Usage Example ====================
if __name__ == "__main__":
    analyzer = ContentAnalyzer()

    sample_text = """Hello world.
    \u200b print("Hidden message")
    72 101 108 108 111
    """

    try:
        results = analyzer.full_analysis(sample_text, "cld3")
        print(results.model_dump())
    except ValidationError as e:
        print(f"Validation error: {e}")
