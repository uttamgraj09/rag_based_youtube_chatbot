from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled


def fetch_transcript(video_id: str, languages=None) -> str:
    """
    Fetch transcript for a YouTube video in given languages.
    Returns full transcript as a single string.
    """
    if languages is None:
        languages = ["en", "hi"]

    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.fetch(video_id, languages=languages)
        transcript_text = " ".join(chunk.text for chunk in transcript_list)
        return transcript_text

    except TranscriptsDisabled:
        raise RuntimeError("Transcript is disabled for this video")

