"""End-to-end through the HTTP API, with mock providers."""


def say(client, call_id, text, **extra):
    r = client.post(f"/calls/{call_id}/turns", json={"text": text, **extra})
    assert r.status_code == 200, r.text
    return r.json()


def test_requires_api_key(app):
    from fastapi.testclient import TestClient
    with TestClient(app) as anon:
        assert anon.get("/accounts").status_code == 401
        assert anon.get("/health").status_code == 200


def test_full_call_with_hardship_ends_in_affordable_plan(client):
    r = client.post("/calls", json={"account_id": "ACC-1001"})
    assert r.status_code == 201, r.text
    opening = r.json()
    call_id = opening["call_id"]
    assert opening["status"] == "in_progress"
    assert opening["agent_text"].startswith("Just so you know, I'm an automated assistant.")

    ask = say(client, call_id, "Yes, speaking.")
    assert "date of birth" in ask["agent_text"]

    offer = say(client, call_id, "It's 14/03/1990 and my postcode is LS6 1AB.")
    assert "VERIFIED" in offer["findings"]
    assert "2 payments of £120.00" in offer["agent_text"]

    # Hardship: the mock model still proposes 2 x £120; the offer guard corrects it.
    corrected = say(client, call_id, "I lost my job last month, I can't afford much.")
    assert "VULNERABILITY" in corrected["findings"]
    assert "UNAFFORDABLE" in corrected["findings"]
    assert "4 payments of £60.00" in corrected["agent_text"]

    booked = say(client, call_id, "Yes, that works.")
    assert booked["plan"]["instalments"] == 4
    assert booked["plan"]["instalment_amount"] == 60.0
    assert booked["plan"]["payment_link"].startswith("https://")

    detail = client.get(f"/calls/{call_id}").json()
    assert detail["audit"]["chain_valid"] is True
    assert detail["plan"]["instalments"] == 4
    customer_texts = [t["final_text"] for t in detail["turns"] if t["speaker"] == "customer"]
    assert "[verification details redacted]" in customer_texts
    assert not any("LS6" in (t or "") for t in customer_texts)


def test_crisis_escalates_and_closes_call(client):
    call_id = client.post("/calls", json={"account_id": "ACC-1001"}).json()["call_id"]
    result = say(client, call_id, "Honestly I don't want to live anymore.")
    assert result["action"] == "escalate"
    assert result["status"] == "escalated"
    assert "CRISIS" in result["findings"]
    assert client.post(f"/calls/{call_id}/turns", json={"text": "hello?"}).status_code == 409


def test_disputed_account_is_blocked_before_dialling(client):
    r = client.post("/calls", json={"account_id": "ACC-1003"}).json()
    assert r["status"] == "blocked"
    assert "ACCOUNT_FLAG" in r["findings"]


def test_low_confidence_speech_asks_to_repeat(client):
    call_id = client.post("/calls", json={"account_id": "ACC-1001"}).json()["call_id"]
    r = say(client, call_id, "fifty pounds", confidence=0.4)
    assert r["findings"] == ["LOW_ASR_CONFIDENCE"]
    assert "say that again" in r["agent_text"]


def test_policy_needs_a_second_approver(client):
    rules = client.get("/policies/active").json()["rules"]
    rules["max_instalments"] = 6
    assert client.post("/policies", json={"version": "policy-v19", "created_by": "alice", "rules": rules}).status_code == 201
    assert client.post("/policies/policy-v19/approve", json={"approved_by": "alice"}).status_code == 403
    assert client.post("/policies/policy-v19/approve", json={"approved_by": "bob"}).status_code == 200
    assert client.get("/policies/active").json()["version"] == "policy-v19"


def test_worker_pass_starts_and_blocks(app):
    from app.services import scheduler
    runtime = app.state.runtime
    with runtime.session_factory() as db:
        stats = scheduler.run_once(db, runtime.container)
    assert stats["started"] == 2   # ACC-1001 (GB), ACC-1002 (ES)
    assert stats["blocked"] == 1   # ACC-1003 is disputed
