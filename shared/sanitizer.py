"""
WebGarden HTML Sanitizer
Sanitize HTML content from rich text editors to prevent XSS attacks.
"""

import bleach
from bleach.css_sanitizer import CSSSanitizer


# Allowed HTML tags for blog content
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 's', 'sub', 'sup',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote', 'code', 'pre',
    'ul', 'ol', 'li',
    'a', 'img',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'div', 'span',
    'hr',
]

# Allowed HTML attributes
ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id'],
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height', 'style'],
    'div': ['style'],
    'span': ['style'],
    'p': ['style'],
    'td': ['colspan', 'rowspan', 'style'],
    'th': ['colspan', 'rowspan', 'style'],
}

# Allowed CSS properties
ALLOWED_STYLES = [
    'color', 'background-color',
    'font-family', 'font-size', 'font-weight', 'font-style',
    'text-align', 'text-decoration',
    'width', 'height', 'max-width', 'max-height',
    'margin', 'margin-top', 'margin-right', 'margin-bottom', 'margin-left',
    'padding', 'padding-top', 'padding-right', 'padding-bottom', 'padding-left',
    'border', 'border-width', 'border-color', 'border-style',
]

# Allowed protocols for links
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto', 'tel']


def sanitize_html(html_content):
    """
    Sanitize HTML content to prevent XSS attacks while preserving formatting.

    Args:
        html_content: Raw HTML string from rich text editor

    Returns:
        Sanitized HTML string safe for rendering
    """
    if not html_content:
        return ''

    # Create CSS sanitizer
    css_sanitizer = CSSSanitizer(allowed_css_properties=ALLOWED_STYLES)

    # Clean the HTML
    clean_html = bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        css_sanitizer=css_sanitizer,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,  # Strip disallowed tags instead of escaping
    )

    # Linkify URLs in plain text (optional)
    clean_html = bleach.linkify(
        clean_html,
        parse_email=True,
        callbacks=[],
    )

    return clean_html


def strip_html(html_content):
    """
    Strip all HTML tags from content, leaving only text.
    Useful for creating excerpts or meta descriptions.

    Args:
        html_content: HTML string

    Returns:
        Plain text string
    """
    if not html_content:
        return ''

    return bleach.clean(html_content, tags=[], strip=True)


def create_excerpt(html_content, max_length=150):
    """
    Create a plain text excerpt from HTML content.

    Args:
        html_content: HTML string
        max_length: Maximum length of excerpt

    Returns:
        Plain text excerpt with ellipsis if truncated
    """
    if not html_content:
        return ''

    # Strip HTML tags
    plain_text = strip_html(html_content)

    # Remove extra whitespace
    plain_text = ' '.join(plain_text.split())

    # Truncate if needed
    if len(plain_text) > max_length:
        # Try to break at a word boundary
        excerpt = plain_text[:max_length].rsplit(' ', 1)[0]
        return excerpt + '...'

    return plain_text
