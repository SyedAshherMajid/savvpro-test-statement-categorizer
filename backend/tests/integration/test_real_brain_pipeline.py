"""End-to-end through the real brain (needs app.brain, which is built separately)."""

from fastapi.testclient import TestClient

from tests.conftest import upload
from tests.factories import OFX_V1, OFX_V2, bank_csv


def test_real_brain_csv_pipeline(real_client: TestClient) -> None:
    r = upload(real_client, bank_csv())
    assert r.status_code == 201, r.text
    sid = r.json()["id"]
    items = real_client.get(f"/api/v1/statements/{sid}/transactions").json()["items"]
    assert len(items) == 4
    assert all(
        i["status"] in {"auto", "needs_review", "user_confirmed", "duplicate"} for i in items
    )
    summary = real_client.get(f"/api/v1/statements/{sid}/summary")
    assert summary.status_code == 200


def test_real_brain_ofx_pipelines(real_client: TestClient) -> None:
    assert upload(real_client, OFX_V1, name="a.ofx").status_code == 201
    r = upload(real_client, OFX_V2, name="b.ofx", account_type="credit_card")
    assert r.status_code == 201, r.text
    assert r.json()["account_type"] == "credit_card"


def test_real_brain_second_upload_flags_overlap(real_client: TestClient) -> None:
    upload(real_client, bank_csv())
    r = upload(real_client, bank_csv([("02/10/2026", "SOMETHING NEW", "-9.99")]), name="b.csv")
    assert r.json()["counts"]["duplicate"] == 4
