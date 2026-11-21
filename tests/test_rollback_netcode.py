import pytest
import math
from gameplay import rollback_netcode as mod

CASES = [
    ("frames", 'm.rollback_frames(2, 1) == 3'),
    ("hash", 'm.state_hash(1, 2) == 1020'),
    ("delay", 'm.input_delay(32, 2) == 4'),
    ("proj", 'm.projectile_state(5) == 5'),
    ("reconnect", 'm.reconnect_predict(3) == 0'),
    ("spectator", 'm.spectator_offset(2) == 2'),
    ("advantage", 'm.frame_advantage(2, 10) == 8'),
    ("step", 'm.fixed_step(1 / 60) == 1'),
    ("buffer", 'm.buffer_size(40) == 40'),
    ("rand", 'm.deterministic_rand(7) == 7'),
    ("clamp", 'm.clamp_rollback(5, 3) == 3'),
    ("sync", 'm.sync_state(1, 2) == 2'),
    ("tick", 'm.tick_from_time(1) == 60'),
    ("key", 'm.rollback_key(3, 2) == "3:2"'),
    ("desync", 'm.is_desync(1, 2) is True')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx, "math": math})
