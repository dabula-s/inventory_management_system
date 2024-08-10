import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_connection(pg_session):
    result = await pg_session.execute(text('select 1'))
    assert result.first() is not None
