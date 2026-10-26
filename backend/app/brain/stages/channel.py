"""Stage 2: who is on the other side. Tenants paying rent, deposits, people, paper checks."""

import re

from app.brain.state import RowState
from app.domain.enums import AccountType, Category, Direction, Flag

DEPOSIT_RE = re.compile(r"\b(SECURITY|SEC DEP|DEPOSIT)\b")
DEPOSIT_RETURN_RE = re.compile(
    r"\b(DEPOSIT|SEC DEP)\b.*\b(RETURN|REFUND)|\b(RETURN|REFUND)\b.*\bDEPOSIT\b"
)
RENT_RE = re.compile(r"\bRENT\b")
RENT_EXTRA_RE = re.compile(r"\b(LATE FEE|PET (FEE|RENT)|PARKING FEE)\b")
BUSINESS_TOKENS = frozenset(
    {
        "LLC",
        "INC",
        "CO",
        "CORP",
        "LTD",
        "LP",
        "COMPANY",
        "SERVICES",
        "SERVICE",
        "GROUP",
        "PLUMBING",
        "ROOFING",
        "HVAC",
        "ELECTRIC",
        "CLEANING",
        "LANDSCAPING",
        "MGMT",
        "MANAGEMENT",
        "REALTY",
        "PROPERTIES",
        "HOA",
        "ASSOCIATION",
        "BANK",
        "INSURANCE",
        "CONSTRUCTION",
        "CONTRACTORS",
        "REPAIR",
        "REPAIRS",
        "LAW",
        "CPA",
    }
)


def looks_like_person(name: str | None) -> bool:
    if not name:
        return False
    tokens = name.split()
    return (
        2 <= len(tokens) <= 4
        and all(t.isalpha() for t in tokens)
        and not any(t in BUSINESS_TOKENS for t in tokens)
    )


def apply(state: RowState) -> None:
    txn = state.txn
    text = state.text

    if txn.channel == "CHECK" and txn.direction is Direction.OUTFLOW:
        state.flags.add(Flag.CHECK_NO_PAYEE)
        return

    if not state.is_p2p or not looks_like_person(txn.counterparty):
        return

    who = (txn.counterparty or "").title()
    if txn.direction is Direction.INFLOW and txn.account_type is AccountType.CHECKING:
        if DEPOSIT_RE.search(text) and not RENT_RE.search(text):
            state.add(
                Category.SECURITY_DEPOSIT_RECEIVED,
                0.92,
                "channel",
                "ch.deposit_in",
                f"Payment from {who} mentions a deposit. Deposits are held for the tenant, "
                "not income.",
            )
            state.add(Category.RENT, 0.30, "channel", "ch.rent_weak", f"Payment from {who}.")
        elif RENT_RE.search(text) or RENT_EXTRA_RE.search(text):
            state.add(
                Category.RENT,
                0.92,
                "channel",
                "ch.rent_memo",
                f"Payment from {who} with a rent-related memo.",
            )
        else:
            state.add(
                Category.RENT,
                0.70,
                "channel",
                "ch.rent_person",
                f"Payment from a person ({who}). Often rent, but there's no memo.",
            )
    elif txn.direction is Direction.OUTFLOW:
        if DEPOSIT_RETURN_RE.search(text):
            state.add(
                Category.SECURITY_DEPOSIT_RETURNED,
                0.92,
                "channel",
                "ch.deposit_out",
                f"Deposit returned to {who}. Not an expense.",
            )
        else:
            state.flags.add(Flag.PAYMENT_TO_INDIVIDUAL)
