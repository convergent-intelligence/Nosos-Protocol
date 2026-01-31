# Build

From the scaffold root:

```bash
./scripts/build-distro.sh
```

Output:
- `dist/agent-systems-framework-YYYYMMDD.tar.gz`

Notes:
- user data is intentionally excluded (blob store, sqlite db, inbox)
- keep `distro/MANIFEST.yaml` aligned with the script

Verify (manual Phase 0):

```bash
mkdir -p /tmp/asf-test
tar -xzf dist/agent-systems-framework-*.tar.gz -C /tmp/asf-test
cd /tmp/asf-test/agent-systems-framework
./scripts/validate.sh
```

Verify (script):

```bash
./scripts/verify-distro.sh
```
