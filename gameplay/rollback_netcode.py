import math

def rollback_frames(delay, local_frames):
    """回滚帧数。"""
    raise NotImplementedError("TODO: rollback_frames")

def state_hash(x, y):
    """状态哈希。"""
    raise NotImplementedError("TODO: state_hash")

def input_delay(rtt_ms, base):
    """输入延迟。"""
    raise NotImplementedError("TODO: input_delay")

def projectile_state(state):
    """投射物状态。"""
    raise NotImplementedError("TODO: projectile_state")

def reconnect_predict(pending):
    """重连清预测。"""
    raise NotImplementedError("TODO: reconnect_predict")

def spectator_offset(delay):
    """观战偏移。"""
    raise NotImplementedError("TODO: spectator_offset")

def frame_advantage(rollback, total):
    """帧优势。"""
    raise NotImplementedError("TODO: frame_advantage")

def fixed_step(dt):
    """定点步长。"""
    raise NotImplementedError("TODO: fixed_step")

def buffer_size(longest_combo):
    """回滚缓冲。"""
    raise NotImplementedError("TODO: buffer_size")

def deterministic_rand(seed):
    """确定性随机。"""
    raise NotImplementedError("TODO: deterministic_rand")

def clamp_rollback(frames, maximum):
    """回滚钳制。"""
    raise NotImplementedError("TODO: clamp_rollback")

def sync_state(local_state, server_state):
    """状态同步。"""
    raise NotImplementedError("TODO: sync_state")

def tick_from_time(seconds):
    """时间转 tick。"""
    raise NotImplementedError("TODO: tick_from_time")

def rollback_key(seed, index):
    """回滚键。"""
    raise NotImplementedError("TODO: rollback_key")

def is_desync(hash_a, hash_b):
    """失同步判定。"""
    raise NotImplementedError("TODO: is_desync")
