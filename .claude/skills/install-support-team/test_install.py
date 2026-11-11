"""Offline tests for install.py. Run from the kit root: python3 -m unittest discover -s .claude/skills/install-support-team -p 'test_*.py'"""
import importlib.util
import pathlib
import unittest
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("install", HERE / "install.py")
install = importlib.util.module_from_spec(spec)
spec.loader.exec_module(install)


class CmdTestPartialInstall(unittest.TestCase):
    """Video 2 of the course installs only Verify Caller, then runs `test`."""

    def test_skips_functions_that_are_not_installed(self):
        names = None  # test_fn and clear_test_row are stubbed
        installed = {"verify_code"}

        def fake_test_fn(_names, fname, _args):
            if fname not in installed:
                return {"function": fname, "ok": False, "result": "not installed"}
            return {"function": fname, "ok": False, "webhook_ok": True, "ms": 1,
                    "result": {"verified": False, "error": "no_code_sent"}}

        with mock.patch.object(install, "test_fn", fake_test_fn), \
                mock.patch.object(install, "clear_test_row", lambda _n: None), \
                mock.patch.object(install, "say", lambda _m: None):
            results = install.cmd_test(None, names)

        self.assertEqual([r["function"] for r in results], ["verify_code"])
        self.assertTrue(results[0]["ok"])


class GateLine(unittest.TestCase):
    def test_explains_a_missing_rentals_desk(self):
        line = install.gate_line("gate before", {"result": "not installed"})
        self.assertNotIn('"not installed"', line)
        self.assertIn("rentals desk", line)

    def test_shows_the_real_answer_when_installed(self):
        line = install.gate_line("gate after", {"result": {"error": "verify_first"}})
        self.assertIn("verify_first", line)


class KeepUserTools(unittest.TestCase):
    """Video 6 adds transfer_call by hand; re-running the installer must not drop it."""

    def test_keeps_a_tool_the_user_added(self):
        got = install.keep_user_tools(["end_call", "transfer_to_agent"],
                                      ["end_call", "transfer_to_agent", "transfer_call"])
        self.assertIn("transfer_call", got)

    def test_still_drops_managed_tools_it_no_longer_wants(self):
        got = install.keep_user_tools(["end_call"], ["end_call", "transfer_to_agent"])
        self.assertNotIn("transfer_to_agent", got)


class OutboundSettings(unittest.TestCase):
    """Video 7 makes Jim Bob outbound and writes each desk's outbound greeting."""

    cfg = {"company": "Granite Peak Equipment Rental", "first_name": "Dan"}

    def payload(self, piece):
        names = install.Names("GP Test - ", True)
        with mock.patch.object(install, "render_prompt", lambda *a: "prompt"):
            return install.agent_payload(piece, names, self.cfg, list(install.DESKS), True, {})

    def test_each_desk_greets_outbound_as_itself(self):
        for piece, d in install.DESKS.items():
            got = self.payload(piece)["greeting_outbound"]
            self.assertIn(d["short"], got)
            if piece != "rentals":
                self.assertNotIn("Joanne", got)

    def test_rerun_keeps_outbound_mode_and_a_custom_greeting(self):
        body = self.payload("maintenance")
        current = {"agent_mode": "both", "greeting_outbound": "Howdy, it's Jim Bob, following up."}
        install.keep_user_outbound(body, current)
        self.assertEqual(body["agent_mode"], "both")
        self.assertEqual(body["greeting_outbound"], "Howdy, it's Jim Bob, following up.")

    def test_rerun_replaces_the_old_wrong_greeting(self):
        body = self.payload("maintenance")
        old = "Hey there, it's Joanne at Granite Peak Equipment Rental, giving you a ring. What can I do for you, sugar?"
        install.keep_user_outbound(body, {"agent_mode": "inbound", "greeting_outbound": old})
        self.assertEqual(body["agent_mode"], "inbound")
        self.assertNotIn("Joanne", body["greeting_outbound"])


if __name__ == "__main__":
    unittest.main()
