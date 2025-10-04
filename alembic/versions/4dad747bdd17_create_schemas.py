from alembic import op

# revision identifiers, used by Alembic.
revision = "4dad747bdd17_create_schemas"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS cars;")
    op.execute("CREATE SCHEMA IF NOT EXISTS participants;")
    op.execute("CREATE SCHEMA IF NOT EXISTS work_shop;")


def downgrade():
    op.execute("DROP SCHEMA IF EXISTS work_shop CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS participants CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS cars CASCADE;")
