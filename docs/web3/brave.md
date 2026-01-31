# Brave Browser Integration

Brave Wallet typically exposes an EIP-1193 provider:
- `window.ethereum`

Frontend expectations (Gems):
- detect provider
- request accounts
- build SIWE message
- sign via `personal_sign` / `eth_signTypedData_v4` depending on SIWE lib

Backend expectations (Qwen):
- verify EIP-191 signature (SIWE)
- map recovered address to identity id

Do not assume Brave-only.
Treat Brave as a first-class target, but keep EIP-1193 compatible.
