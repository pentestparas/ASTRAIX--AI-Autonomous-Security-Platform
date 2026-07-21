"""Add multi-tenant models

Revision ID: 001_add_multi_tenant
Revises: 
Create Date: 2024-07-10

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_add_multi_tenant'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- Organizations ---
    op.create_table(
        'organizations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False, unique=True),
        sa.Column('description', sa.Text()),
        sa.Column('logo_url', sa.String(500)),
        sa.Column('settings', postgresql.JSONB(astext_type=sa.Text()), default={}, nullable=False),
        sa.Column('subscription_tier', sa.String(50), default='free', nullable=False),
        sa.Column('subscription_expires_at', sa.DateTime(timezone=True)),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index('ix_organizations_slug', 'organizations', ['slug'], unique=True)

    # --- Users ---
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255)),
        sa.Column('full_name', sa.String(255)),
        sa.Column('avatar_url', sa.String(500)),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('is_superuser', sa.Boolean(), default=False, nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True)),
        sa.Column('mfa_enabled', sa.Boolean(), default=False, nullable=False),
        sa.Column('mfa_secret', sa.String(255)),
        sa.Column('preferences', postgresql.JSONB(astext_type=sa.Text()), default={}, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index('ix_users_email_active', 'users', ['email', 'is_active'])

    # --- Projects ---
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False, index=True),
        sa.Column('description', sa.Text()),
        sa.Column('settings', postgresql.JSONB(astext_type=sa.Text()), default={}, nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_unique_constraint('uq_project_org_slug', 'projects', ['organization_id', 'slug'])
    op.create_index('ix_projects_org_active', 'projects', ['organization_id', 'is_active'])

    # --- Memberships ---
    op.create_table(
        'memberships',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=True, index=True),
        sa.Column('role', sa.String(50), nullable=False, default='viewer'),
        sa.Column('is_default', sa.Boolean(), default=False, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_unique_constraint('uq_membership_org_user', 'memberships', ['organization_id', 'user_id'])
    op.create_unique_constraint('uq_membership_project_user', 'memberships', ['project_id', 'user_id'])
    op.create_index('ix_memberships_org_user', 'memberships', ['organization_id', 'user_id'])
    op.create_index('ix_memberships_project_user', 'memberships', ['project_id', 'user_id'])

    # --- API Keys ---
    op.create_table(
        'api_keys',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('key_hash', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('key_prefix', sa.String(20), nullable=False),
        sa.Column('scopes', postgresql.JSONB(astext_type=sa.Text()), default=[], nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True)),
        sa.Column('last_used_at', sa.DateTime(timezone=True)),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index('ix_api_keys_org_active', 'api_keys', ['organization_id', 'is_active'])
    op.create_index('ix_api_keys_prefix', 'api_keys', ['key_prefix'])

    # --- Assets (updated) ---
    op.create_table(
        'assets',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.String(50), nullable=False, index=True),
        sa.Column('identifier', sa.String(255), nullable=False, index=True),
        sa.Column('criticality', sa.String(50), default='medium', nullable=False),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), default=[], nullable=False),
        sa.Column('metadata_json', postgresql.JSONB(astext_type=sa.Text()), default={}, nullable=False),
        sa.Column('last_scanned', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index('ix_assets_org_project_identifier', 'assets', ['organization_id', 'project_id', 'identifier', 'type'], unique=True)
    op.create_index('ix_assets_org_type', 'assets', ['organization_id', 'type'])

    # --- Assessments (updated) ---
    op.create_table(
        'assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('asset_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assets.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('status', sa.String(50), default='pending', nullable=False, index=True),
        sa.Column('type', sa.String(50), nullable=False, index=True),
        sa.Column('config', postgresql.JSONB(astext_type=sa.Text()), default={}, nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True)),
        sa.Column('completed_at', sa.DateTime(timezone=True)),
        sa.Column('findings_count', sa.Integer(), default=0, nullable=False),
        sa.Column('error', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index('ix_assessments_org_project_status', 'assessments', ['organization_id', 'project_id', 'status'])
    op.create_index('ix_assessments_org_asset', 'assessments', ['organization_id', 'asset_id'])

    # --- Findings (updated) ---
    op.create_table(
        'findings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('asset_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assets.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessments.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('plugin_id', sa.String(255), nullable=False, index=True),
        sa.Column('severity', sa.String(50), nullable=False, index=True),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), default={}, nullable=False),
        sa.Column('cvss_score', sa.Float()),
        sa.Column('remediation', sa.Text()),
        sa.Column('reference', sa.Text()),
        sa.Column('fingerprint', sa.String(64), nullable=False, unique=True, index=True),
        sa.Column('status', sa.String(50), default='open', nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index('ix_findings_asset_severity', 'findings', ['asset_id', 'severity'])
    op.create_index('ix_findings_assessment_fingerprint', 'findings', ['assessment_id', 'fingerprint'])
    op.create_index('ix_findings_org_project_status', 'findings', ['organization_id', 'project_id', 'status'])
    op.create_index('ix_findings_org_severity_status', 'findings', ['organization_id', 'severity', 'status'])

    # --- Audit Logs ---
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('action', sa.String(100), nullable=False, index=True),
        sa.Column('resource_type', sa.String(100), nullable=False, index=True),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column('changes', postgresql.JSONB(astext_type=sa.Text())),
        sa.Column('ip_address', sa.String(45)),
        sa.Column('user_agent', sa.Text()),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), default={}, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_audit_logs_org_action', 'audit_logs', ['organization_id', 'action'])
    op.create_index('ix_audit_logs_org_resource', 'audit_logs', ['organization_id', 'resource_type', 'resource_id'])
    op.create_index('ix_audit_logs_user', 'audit_logs', ['user_id'])


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('findings')
    op.drop_table('assessments')
    op.drop_table('assets')
    op.drop_table('api_keys')
    op.drop_table('memberships')
    op.drop_table('projects')
    op.drop_table('users')
    op.drop_table('organizations')