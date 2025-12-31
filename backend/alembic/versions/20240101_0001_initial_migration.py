"""Initial migration - Create all tables

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, default=False),
        sa.Column('role', sa.Enum('admin', 'analyst', 'viewer', name='userrole'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create data_sources table
    op.create_table(
        'data_sources',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('platform', sa.Enum('twitter', 'instagram', 'telegram', 'linkedin', 'youtube', 'news', 'forum', 'custom', name='sourceplatform'), nullable=False),
        sa.Column('api_endpoint', sa.String(length=500), nullable=True),
        sa.Column('credentials', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('collection_config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('last_sync_at', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_data_sources_platform'), 'data_sources', ['platform'], unique=False)
    op.create_index(op.f('ix_data_sources_id'), 'data_sources', ['id'], unique=False)

    # Create authors table
    op.create_table(
        'authors',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('platform_id', sa.String(length=255), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=True),
        sa.Column('display_name', sa.String(length=255), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('profile_url', sa.String(length=500), nullable=True),
        sa.Column('avatar_url', sa.String(length=500), nullable=True),
        sa.Column('followers_count', sa.Integer(), default=0),
        sa.Column('following_count', sa.Integer(), default=0),
        sa.Column('posts_count', sa.Integer(), default=0),
        sa.Column('influence_score', sa.Float(), nullable=True),
        sa.Column('pagerank_score', sa.Float(), nullable=True),
        sa.Column('extra_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),  # CHANGED
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_authors_platform_id'), 'authors', ['platform_id'], unique=False)
    op.create_index(op.f('ix_authors_platform'), 'authors', ['platform'], unique=False)
    op.create_index(op.f('ix_authors_username'), 'authors', ['username'], unique=False)
    op.create_index(op.f('ix_authors_id'), 'authors', ['id'], unique=False)

    # Create posts table
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('platform_id', sa.String(length=255), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('content_normalized', sa.Text(), nullable=True),
        sa.Column('language', sa.String(length=10), default='fa'),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('media_urls', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('likes_count', sa.Integer(), default=0),
        sa.Column('comments_count', sa.Integer(), default=0),
        sa.Column('shares_count', sa.Integer(), default=0),
        sa.Column('views_count', sa.Integer(), default=0),
        sa.Column('posted_at', sa.DateTime(), nullable=True),
        sa.Column('hashtags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('mentions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_processed', sa.Boolean(), default=False),
        sa.Column('processing_error', sa.Text(), nullable=True),
        sa.Column('data_source_id', sa.Integer(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
        sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_platform_id'), 'posts', ['platform_id'], unique=True)
    op.create_index(op.f('ix_posts_platform'), 'posts', ['platform'], unique=False)
    op.create_index(op.f('ix_posts_language'), 'posts', ['language'], unique=False)
    op.create_index(op.f('ix_posts_posted_at'), 'posts', ['posted_at'], unique=False)
    op.create_index(op.f('ix_posts_is_processed'), 'posts', ['is_processed'], unique=False)
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)

    # Create analyses table
    op.create_table(
        'analyses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('analysis_type', sa.Enum('sentiment', 'emotion', 'summarization', 'topic_modeling', 'keyword_extraction', 'entity_recognition', 'trend_detection', 'graph_analysis', 'full', name='analysistype'), nullable=False),
        sa.Column('config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('query_filters', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('post_count', sa.Integer(), default=0),
        sa.Column('status', sa.Enum('pending', 'queued', 'processing', 'completed', 'failed', 'cancelled', name='analysisstatus'), nullable=False),
        sa.Column('progress', sa.Float(), default=0.0),
        sa.Column('summary', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('started_at', sa.String(length=50), nullable=True),
        sa.Column('completed_at', sa.String(length=50), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analyses_analysis_type'), 'analyses', ['analysis_type'], unique=False)
    op.create_index(op.f('ix_analyses_status'), 'analyses', ['status'], unique=False)
    op.create_index(op.f('ix_analyses_id'), 'analyses', ['id'], unique=False)

    # Create analysis_results table
    op.create_table(
        'analysis_results',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('sentiment_label', sa.String(length=20), nullable=True),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('sentiment_confidence', sa.Float(), nullable=True),
        sa.Column('emotions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('dominant_emotion', sa.String(length=50), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('keywords', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('topics', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('entities', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('node_degree', sa.Integer(), nullable=True),
        sa.Column('centrality_score', sa.Float(), nullable=True),
        sa.Column('community_id', sa.Integer(), nullable=True),
        sa.Column('raw_results', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('analysis_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
        sa.ForeignKeyConstraint(['analysis_id'], ['analyses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analysis_results_post_id'), 'analysis_results', ['post_id'], unique=False)
    op.create_index(op.f('ix_analysis_results_analysis_id'), 'analysis_results', ['analysis_id'], unique=False)
    op.create_index(op.f('ix_analysis_results_id'), 'analysis_results', ['id'], unique=False)

    # Create trends table
    op.create_table(
        'trends',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('volume', sa.Integer(), default=0),
        sa.Column('growth_rate', sa.Float(), nullable=True),
        sa.Column('velocity', sa.Float(), nullable=True),
        sa.Column('peak_time', sa.DateTime(), nullable=True),
        sa.Column('keywords', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('hashtags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('sentiment_distribution', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('time_series', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('geo_distribution', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('top_authors', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('top_posts', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.String(length=10), default='active'),
        sa.Column('analysis_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['analyses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trends_name'), 'trends', ['name'], unique=False)
    op.create_index(op.f('ix_trends_id'), 'trends', ['id'], unique=False)

    # Create graph_nodes table
    op.create_table(
        'graph_nodes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('node_id', sa.String(length=255), nullable=False),
        sa.Column('node_type', sa.String(length=50), nullable=False),
        sa.Column('label', sa.String(length=255), nullable=True),
        sa.Column('attributes', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('degree', sa.Integer(), default=0),
        sa.Column('in_degree', sa.Integer(), default=0),
        sa.Column('out_degree', sa.Integer(), default=0),
        sa.Column('pagerank', sa.Float(), nullable=True),
        sa.Column('betweenness_centrality', sa.Float(), nullable=True),
        sa.Column('closeness_centrality', sa.Float(), nullable=True),
        sa.Column('eigenvector_centrality', sa.Float(), nullable=True),
        sa.Column('community_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_graph_nodes_node_id'), 'graph_nodes', ['node_id'], unique=True)
    op.create_index(op.f('ix_graph_nodes_node_type'), 'graph_nodes', ['node_type'], unique=False)
    op.create_index(op.f('ix_graph_nodes_community_id'), 'graph_nodes', ['community_id'], unique=False)
    op.create_index(op.f('ix_graph_nodes_id'), 'graph_nodes', ['id'], unique=False)

    # Create graph_edges table
    op.create_table(
        'graph_edges',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('edge_type', sa.String(length=50), nullable=False),
        sa.Column('weight', sa.Float(), default=1.0),
        sa.Column('attributes', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('first_seen', sa.String(length=50), nullable=True),
        sa.Column('last_seen', sa.String(length=50), nullable=True),
        sa.Column('occurrence_count', sa.Integer(), default=1),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('target_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['source_id'], ['graph_nodes.id'], ),
        sa.ForeignKeyConstraint(['target_id'], ['graph_nodes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_graph_edges_edge_type'), 'graph_edges', ['edge_type'], unique=False)
    op.create_index(op.f('ix_graph_edges_source_id'), 'graph_edges', ['source_id'], unique=False)
    op.create_index(op.f('ix_graph_edges_target_id'), 'graph_edges', ['target_id'], unique=False)
    op.create_index(op.f('ix_graph_edges_id'), 'graph_edges', ['id'], unique=False)

    # Create dashboards table
    op.create_table(
        'dashboards',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('layout', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('widgets', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('filters', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('refresh_interval', sa.Integer(), default=300),
        sa.Column('is_default', sa.Boolean(), default=False),
        sa.Column('is_public', sa.Boolean(), default=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dashboards_id'), 'dashboards', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_dashboards_id'), table_name='dashboards')
    op.drop_table('dashboards')
    
    op.drop_index(op.f('ix_graph_edges_id'), table_name='graph_edges')
    op.drop_index(op.f('ix_graph_edges_target_id'), table_name='graph_edges')
    op.drop_index(op.f('ix_graph_edges_source_id'), table_name='graph_edges')
    op.drop_index(op.f('ix_graph_edges_edge_type'), table_name='graph_edges')
    op.drop_table('graph_edges')
    
    op.drop_index(op.f('ix_graph_nodes_id'), table_name='graph_nodes')
    op.drop_index(op.f('ix_graph_nodes_community_id'), table_name='graph_nodes')
    op.drop_index(op.f('ix_graph_nodes_node_type'), table_name='graph_nodes')
    op.drop_index(op.f('ix_graph_nodes_node_id'), table_name='graph_nodes')
    op.drop_table('graph_nodes')
    
    op.drop_index(op.f('ix_trends_id'), table_name='trends')
    op.drop_index(op.f('ix_trends_name'), table_name='trends')
    op.drop_table('trends')
    
    op.drop_index(op.f('ix_analysis_results_id'), table_name='analysis_results')
    op.drop_index(op.f('ix_analysis_results_analysis_id'), table_name='analysis_results')
    op.drop_index(op.f('ix_analysis_results_post_id'), table_name='analysis_results')
    op.drop_table('analysis_results')
    
    op.drop_index(op.f('ix_analyses_id'), table_name='analyses')
    op.drop_index(op.f('ix_analyses_status'), table_name='analyses')
    op.drop_index(op.f('ix_analyses_analysis_type'), table_name='analyses')
    op.drop_table('analyses')
    
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_index(op.f('ix_posts_is_processed'), table_name='posts')
    op.drop_index(op.f('ix_posts_posted_at'), table_name='posts')
    op.drop_index(op.f('ix_posts_language'), table_name='posts')
    op.drop_index(op.f('ix_posts_platform'), table_name='posts')
    op.drop_index(op.f('ix_posts_platform_id'), table_name='posts')
    op.drop_table('posts')
    
    op.drop_index(op.f('ix_authors_id'), table_name='authors')
    op.drop_index(op.f('ix_authors_username'), table_name='authors')
    op.drop_index(op.f('ix_authors_platform'), table_name='authors')
    op.drop_index(op.f('ix_authors_platform_id'), table_name='authors')
    op.drop_table('authors')
    
    op.drop_index(op.f('ix_data_sources_id'), table_name='data_sources')
    op.drop_index(op.f('ix_data_sources_platform'), table_name='data_sources')
    op.drop_table('data_sources')
    
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS userrole')
    op.execute('DROP TYPE IF EXISTS sourceplatform')
    op.execute('DROP TYPE IF EXISTS analysistype')
    op.execute('DROP TYPE IF EXISTS analysisstatus')
