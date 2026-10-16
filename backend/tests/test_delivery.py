from copy import deepcopy

import pytest

from scripts.practice_delivery import REQUIREMENTS, submission_filename, timestamp_seconds, validate_delivery


def complete():
    return {"group_number": 7, "estimated_student_hours": {"desarrollo": 10},
            "video": {"url": "https://www.youtube.com/watch?v=fictional", "duration_seconds": 780,
                      "width": 1920, "height": 1080, "format": "mp4", "access_checked_in_incognito": True,
                      "timestamps": {key: "05:00" for key in REQUIREMENTS}},
            "external_installation": {"completed": True, "tester_alias": "Tester ficticio", "date": "2026-10-13", "result": "Prueba ficticia unitaria"},
            "narrative_updated_for_submission": True,
            "student_pdf_reviewed": True, "repository_access_checked": True}


def test_complete_declared_metadata_is_accepted():
    assert validate_delivery(complete()) == []


def test_explicit_individual_submission_has_no_invented_group():
    data = complete()
    data.update(group_number=None, submission_mode="individual", author="Pablo Cortes")
    assert validate_delivery(data) == []
    assert submission_filename(data) == "P3_Pablo_Cortes_Memoria.pdf"
    assert submission_filename(complete()) == "P3_Grupo07_Memoria.pdf"


def test_individual_submission_still_requires_real_video_and_external_date():
    data = complete()
    data.update(group_number=None, submission_mode="individual", author="Pablo Cortes")
    data["video"]["url"] = None
    data["external_installation"]["date"] = None
    assert len(validate_delivery(data)) == 2


def test_individual_submission_does_not_accept_missing_author_or_invalid_group():
    data = complete()
    data.update(group_number=None, submission_mode="individual", author=" ")
    assert len(validate_delivery(data)) == 1
    with pytest.raises(ValueError):
        submission_filename(data)
    data.update(group_number=0, author="Pablo Cortes")
    assert len(validate_delivery(data)) == 1
    with pytest.raises(ValueError):
        submission_filename(data)


def test_missing_human_facts_are_not_inferred():
    data = complete()
    data["group_number"] = None
    data["external_installation"]["completed"] = False
    assert len(validate_delivery(data)) == 2


@pytest.mark.parametrize("value", ["05:60", "-1:00", "pendiente", None])
def test_invalid_video_time_is_rejected(value):
    with pytest.raises(ValueError):
        timestamp_seconds(value)


def test_video_short_private_unchecked_and_out_of_range_times():
    data = deepcopy(complete())
    data["video"].update(url="https://user:secret@example.org/video", duration_seconds=599,
                         height=480, access_checked_in_incognito=False)
    data["video"]["timestamps"]["RF-01"] = "20:00"
    assert len(validate_delivery(data)) == 5
