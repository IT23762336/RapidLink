import sys
from pathlib import Path

import pytest
from fastapi import HTTPException


ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


from scripts.dm_gateway import (  # noqa: E402
    build_dm_conversation_id,
    extract_body_text,
    extract_sender,
    normalize_dm_identity,
    parse_dm_conversation_id,
    parse_message,
    validate_dm_sender,
)


def test_build_dm_conversation_id_normalizes_and_sorts():
    assert build_dm_conversation_id(" Orion ", "luna") == "dm:luna:orion"


def test_parse_dm_conversation_id_reads_two_people():
    assert parse_dm_conversation_id("dm:luna:orion") == ("luna", "orion")


def test_extract_sender_and_body_text():
    assert extract_sender("Luna: Meet me at 8") == "Luna"
    assert extract_body_text("Luna: Meet me at 8") == "Meet me at 8"


def test_parse_message_exposes_sender_and_body_text():
    parsed = parse_message("MSG dm:luna:orion msg1 0 1710000000.0 - - - Luna: Meet me at 8")
    assert parsed["sender"] == "Luna"
    assert parsed["body_text"] == "Meet me at 8"


def test_validate_dm_sender_allows_participants_only():
    validate_dm_sender("dm:luna:orion", "Luna")
    with pytest.raises(HTTPException):
        validate_dm_sender("dm:luna:orion", "Atlas")


def test_normalize_dm_identity_cleans_spacing():
    assert normalize_dm_identity("  Luna   Vega  ") == "luna vega"
