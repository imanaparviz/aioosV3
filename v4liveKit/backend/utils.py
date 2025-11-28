import re

def clean_text_for_speech(text: str) -> str:
    """
    Clean text for TTS - remove markdown, special characters, emojis
    This prevents TTS from saying "stern stern" or "hashtag" etc.
    """
    if not text:
        return ""

    # Remove markdown formatting
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold** -> bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic* -> italic
    text = re.sub(r'__([^_]+)__', r'\1', text)      # __bold__ -> bold
    text = re.sub(r'_([^_]+)_', r'\1', text)        # _italic_ -> italic
    text = re.sub(r'~~([^~]+)~~', r'\1', text)      # ~~strike~~ -> strike

    # Remove code blocks
    text = re.sub(r'```[^`]*```', '', text)         # ```code``` -> (removed)
    text = re.sub(r'`([^`]+)`', r'\1', text)        # `code` -> code

    # Remove markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # Remove headers (##, ###, etc.)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

    # Remove list markers (-, *, +, 1., 2., etc.)
    text = re.sub(r'^[\*\-\+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)

    # Remove special characters that TTS reads weirdly
    # Keep: letters, numbers, basic punctuation (.,!?;:)
    # Remove: #, *, +, /, \, |, @, $, %, ^, &, =, <, >, ~, etc.
    text = re.sub(r'[#\*\+/\\|@\$%\^&=<>~`]', '', text)

    # Remove emojis (Unicode range for common emojis)
    text = re.sub(r'[\U0001F600-\U0001F64F]', '', text)  # Emoticons
    text = re.sub(r'[\U0001F300-\U0001F5FF]', '', text)  # Symbols & pictographs
    text = re.sub(r'[\U0001F680-\U0001F6FF]', '', text)  # Transport & map
    text = re.sub(r'[\U0001F1E0-\U0001F1FF]', '', text)  # Flags
    text = re.sub(r'[\U00002600-\U000027BF]', '', text)  # Misc symbols
    text = re.sub(r'[\U0001F900-\U0001F9FF]', '', text)  # Supplemental symbols

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text
