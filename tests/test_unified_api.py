import json

from pygorpmrustinfo import (
    get_go_build_info,
    get_go_mod,
    get_go_sum,
    get_rpm_db_info,
    get_rust_audit,
)


def test_unified_api_returns_error_dicts_for_missing_inputs():
    assert isinstance(get_rpm_db_info("/tmp/does-not-exist"), dict)
    assert isinstance(get_rust_audit("/tmp/does-not-exist"), dict)
    assert isinstance(get_go_build_info("/tmp/does-not-exist"), dict)
    assert isinstance(get_go_mod("/tmp/does-not-exist"), dict)
    assert isinstance(get_go_sum("/tmp/does-not-exist"), dict)


def test_go_sum_handles_invalid_go_sum_file():
    result = get_go_sum("/tmp/does-not-exist")
    assert result["error"] == "not a valid go sum file"


def test_go_mod_returns_json_serializable_output():
    payload = json.dumps(get_go_mod("/tmp/does-not-exist"))
    assert isinstance(payload, str)
