"""update transactions schema

Revision ID: f6358566be6a
Revises: 1a15ca6fe2ad
Create Date: 2026-02-04 18:29:35.773127
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f6358566be6a"
down_revision: Union[str, Sequence[str], None] = "1a15ca6fe2ad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- remove symbol ---
    op.drop_index("ix_transactions_symbol", table_name="transactions")
    op.drop_column("transactions", "symbol")

    # --- fix constraints ---
    op.drop_constraint(
        "check_quantity_non_negative",
        "transactions",
        type_="check",
    )
    op.drop_constraint(
        "check_price_non_negative",
        "transactions",
        type_="check",
    )

    op.create_check_constraint(
        "check_quantity_positive",
        "transactions",
        "quantity > 0",
    )
    op.create_check_constraint(
        "check_price_positive",
        "transactions",
        "price > 0",
    )

    # --- timestamp default ---
    op.alter_column(
        "transactions",
        "timestamp",
        server_default=sa.text("now()")
    
    )


def downgrade() -> None:
    # --- revert timestamp default ---
    op.alter_column(
        "transactions",
        "timestamp",
        server_default=None,
    )

    # --- revert constraints ---
    op.drop_constraint(
        "check_quantity_positive",
        "transactions",
        type_="check",
    )
    op.drop_constraint(
        "check_price_positive",
        "transactions",
        type_="check",
    )

    op.create_check_constraint(
        "check_quantity_non_negative",
        "transactions",
        "quantity >= 0",
    )
    op.create_check_constraint(
        "check_price_non_negative",
        "transactions",
        "price >= 0",
    )

    # --- restore symbol ---
    op.add_column(
        "transactions",
        sa.Column("symbol", sa.VARCHAR(), nullable=True),
    )
    op.create_index(
        "ix_transactions_symbol",
        "transactions",
        ["symbol"],
        unique=False,
    )
