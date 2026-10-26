import unittest
from dataclasses import replace
from release_policy import Manifest, can_promote

GOOD="a"*64
IMAGE="b"*64

class TestRelease(unittest.TestCase):
    def setUp(self):
        self.m = Manifest(GOOD, IMAGE, "trusted-repo", "dataset-v1",
                          True, "builder", "reviewer", "prod", GOOD, True)
    def test_approved_release(self):
        self.assertTrue(can_promote(self.m))
    def test_tampered_model_digest(self):
        self.assertFalse(can_promote(replace(self.m,model_digest="c"*64)))
    def test_bad_model_hash(self):
        self.assertFalse(can_promote(replace(self.m,model_digest="not-a-hash")))
    def test_bad_image_hash(self):
        self.assertFalse(can_promote(replace(self.m,image_digest="image:latest")))
    def test_untrusted_source(self):
        self.assertFalse(can_promote(replace(self.m,source="unknown")))
    def test_missing_dataset_version(self):
        self.assertFalse(can_promote(replace(self.m,dataset_version="")))
    def test_evaluation_failure(self):
        self.assertFalse(can_promote(replace(self.m,evaluation_passed=False)))
    def test_self_approval(self):
        self.assertFalse(can_promote(replace(self.m,reviewer="builder")))
    def test_no_reviewer(self):
        self.assertFalse(can_promote(replace(self.m,reviewer="")))
    def test_target_scope(self):
        self.assertFalse(can_promote(replace(self.m,target="other-prod")))
    def test_approval_revoked(self):
        self.assertFalse(can_promote(replace(self.m,approval_active=False)))
    def test_unapproved_model_digest(self):
        self.assertFalse(can_promote(replace(self.m,approved_model_digest="c"*64)))

if __name__=="__main__":unittest.main()
