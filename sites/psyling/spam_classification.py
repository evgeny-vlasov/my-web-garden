"""Conservative, privacy-safe signals for Psyling contact submissions."""

from dataclasses import dataclass
from datetime import timedelta
import re


REPEAT_MESSAGE_LOOKBACK = timedelta(days=30)

_URL_PATTERN = re.compile(r"(?:https?://|www\.)[^\s<>()]+", re.IGNORECASE)
_COMMERCIAL_SOLICITATION_PATTERN = re.compile(
    r"\b(?:seo|backlinks?|guest posts?|web design|digital marketing|"
    r"google ranking|cryptocurrency|crypto|casino|gambling|forex|"
    r"investment returns?|loan offers?|lead generation)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ContactSpamDecision:
    """Categorical signals only; never retain or expose submitted text."""

    repeated_message: bool
    multiple_urls: bool
    commercial_solicitation: bool

    @property
    def strong_signal_count(self):
        return sum(
            (
                self.repeated_message,
                self.multiple_urls,
                self.commercial_solicitation,
            )
        )

    @property
    def should_quarantine(self):
        return self.strong_signal_count >= 2


def normalize_contact_message(message):
    """Normalize case and whitespace for exact repeat comparison."""
    return " ".join((message or "").split()).casefold()


def classify_contact_message(message, previous_messages=()):
    """Return a narrow decision from three independent strong signals."""
    normalized_message = normalize_contact_message(message)
    repeated_message = bool(normalized_message) and any(
        normalize_contact_message(previous) == normalized_message
        for previous in previous_messages
    )

    return ContactSpamDecision(
        repeated_message=repeated_message,
        multiple_urls=len(_URL_PATTERN.findall(message or "")) >= 2,
        commercial_solicitation=bool(
            _COMMERCIAL_SOLICITATION_PATTERN.search(message or "")
        ),
    )
