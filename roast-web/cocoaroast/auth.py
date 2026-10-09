"""Validate CocoaCraft account tokens upstream, without database writes."""
import os
from urllib.parse import urlparse
from uuid import UUID
import httpx
from fastapi import Header, HTTPException


def require_account(authorization: str | None = Header(default=None)) -> UUID:
    if not authorization or not authorization.startswith('Bearer ') or not authorization[7:].strip():
        raise HTTPException(401, 'Sign in with your CocoaCraft account', headers={'WWW-Authenticate': 'Bearer'})
    url = os.environ.get('COCOACRAFT_SUPABASE_URL', '').rstrip('/')
    key = os.environ.get('COCOACRAFT_SUPABASE_PUBLISHABLE_KEY', '')
    if not key or urlparse(url).scheme != 'https' or not urlparse(url).hostname:
        raise HTTPException(503, 'CocoaCraft account verification is not configured')
    try:
        with httpx.Client(timeout=5, follow_redirects=False) as client:
            response = client.get(url + '/auth/v1/user', headers={'apikey': key, 'Authorization': authorization})
        if response.status_code in (401, 403):
            raise HTTPException(401, 'CocoaCraft sign-in has expired', headers={'WWW-Authenticate': 'Bearer'})
        if response.status_code != 200:
            raise HTTPException(503, 'Account verification temporarily unavailable')
        user = response.json()
        if user.get('is_anonymous') is True:
            raise HTTPException(401, 'A CocoaCraft account is required')
        return UUID(user['id'])
    except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
        raise HTTPException(503, 'Account verification temporarily unavailable') from exc
