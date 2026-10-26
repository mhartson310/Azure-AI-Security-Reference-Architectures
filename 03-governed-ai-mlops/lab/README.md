# Governed MLOps — Offline release policy example

Run from this directory:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

The sample uses standard-library Python and **synthetic model/image digests** to show a digest-bound release policy: only approved sources, known datasets, positive evaluations, authorized environments and independent reviewers permit promotion.

**Not production-ready:** `Manifest` is only an in-memory data structure; in production its provenance, cryptographic attestations, protected approval state, dataset lineage, reviewer authority, publisher identity and deployment execution must be verified independently. This does not read Azure ML registries, deserialize or execute model artifacts, provision compute, inspect actual ACLs or test live endpoints. Passing tests cannot establish that Azure rejects unapproved promotions; run the [Azure lab validation](../validation/README.md).
