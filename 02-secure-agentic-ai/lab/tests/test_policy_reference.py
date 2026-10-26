import unittest
from policy_reference import Principal, Action, authorize, fingerprint

class Tests(unittest.TestCase):
    def setUp(self):
        self.analyst = Principal("alice", "t-1", "analyst")
        self.editor = Principal("eve", "t-1", "editor")
        self.approver = Principal("bob", "t-1", "approver")
        self.read = Action("get_case", "t-1", "case-1")
        self.write = Action("update_case", "t-1", "case-1")

    def approval(self, user, action):
        return {"fingerprint":fingerprint(user,action),"expires_at":1100,
                "approved_by":"reviewer","used":False}

    def test_read_only_allowed(self):
        self.assertTrue(authorize(self.analyst,self.read))
    def test_analyst_write_denied(self):
        self.assertFalse(authorize(self.analyst,self.write,self.approval(self.analyst,self.write)))
    def test_approval_required(self):
        self.assertFalse(authorize(self.editor,self.write))
    def test_valid_approval_allows(self):
        self.assertTrue(authorize(self.editor,self.write,self.approval(self.editor,self.write)))
    def test_wrong_target_approval_denied(self):
        a=Action("update_case","t-1","case-2")
        self.assertFalse(authorize(self.editor,a,self.approval(self.editor,self.write)))
    def test_cross_tenant_denied(self):
        a=Action("get_case","t-2","case-1")
        self.assertFalse(authorize(self.analyst,a))
    def test_unknown_action_denied(self):
        self.assertFalse(authorize(self.approver,Action("delete_all","t-1","case-1")))
    def test_external_destination_denied(self):
        a=Action("export_case","t-1","case-1","https://unapproved.invalid")
        self.assertFalse(authorize(self.approver,a,self.approval(self.approver,a)))
    def test_expired_approval_denied(self):
        self.assertFalse(authorize(self.editor,self.write,self.approval(self.editor,self.write),1100))
    def test_replayed_approval_denied(self):
        ap=self.approval(self.editor,self.write);ap["used"]=True
        self.assertFalse(authorize(self.editor,self.write,ap))
    def test_self_approval_denied(self):
        ap=self.approval(self.editor,self.write);ap["approved_by"]="eve"
        self.assertFalse(authorize(self.editor,self.write,ap))
    def test_unrecognized_role_denied(self):
        self.assertFalse(authorize(Principal("sam","t-1","owner"),self.read))

if __name__=="__main__":unittest.main()
