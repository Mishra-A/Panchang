from backend.app.core.rule_loader import load_rule


def test_load_kaal_rules():

    rules = load_rule(
        "kaal_rules.json"
    )

    assert rules["version"] == "0.1.0"

    assert (
        rules["rahu_kaal"]["segments"]["friday"]
        == 4
    )

    assert (
        rules["yamaganda"]["segments"]["monday"]
        == 5
    )

    assert (
        rules["gulika"]["segments"]["sunday"]
        == 0
    )
def test_load_muhurat_rules():

    rules = load_rule(
        "muhurat_rules.json"
    )

    vehicle = rules["activities"][
        "vehicle_purchase"
    ]

    assert "Shubh" in (
        vehicle["allowed_choghadiya"]
    )

    assert "Venus" in (
        vehicle["preferred_hora"]
    )

    assert "rahu_kaal" in (
        vehicle["blocked_periods"]
    )    