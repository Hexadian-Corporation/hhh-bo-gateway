import os

# WHY: prime auth env vars so any import-time Settings() construction in tests succeeds.
os.environ.setdefault("HHH_BO_GATEWAY_AUTH_JWKS_URL", "http://test-jwks.local/.well-known/jwks.json")
os.environ.setdefault("HHH_BO_GATEWAY_AUTH_ISSUER", "https://auth.test.hexadian.com")
os.environ.setdefault("HHH_BO_GATEWAY_AUTH_AUDIENCES", '["hexadian-hhh","hexadian-hhh-admin"]')
