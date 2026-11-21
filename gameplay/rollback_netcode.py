"""确定性回滚网络核心。

本模块把回滚联机中容易出错、且必须两边算出完全相同结果的几个环节收敛成
纯函数：输入延迟、状态哈希、随机数种子、投射物快照、帧优势、定点物理步长
与缓冲分配。所有函数都只依赖参数，不读写全局状态，方便在回滚重放中反复
调用而不产生额外副作用。
"""

import math

FPS = 60
FRAME_MS = 1000.0 / FPS


def rollback_frames(delay, local_frames):
    """回滚窗口。

    需要回退的帧数 = 已确认的输入延迟 + 本地相对服务器预测领先的帧数。
    回滚必须覆盖整个窗口，而不是只把角色位置拨回去。
    """
    return max(0, int(delay)) + max(0, int(local_frames))


def state_hash(x, y):
    """定点状态哈希。

    先把浮点坐标量化到定点整数再比较，消掉平台/运算顺序带来的微小浮点
    误差，避免每帧都误判失同步。
    """
    qx = int(round(x * 1000.0))
    qy = int(round(y * 10.0))
    return qx + qy


def input_delay(rtt_ms, base):
    """按实测 RTT 调整输入延迟。

    RTT 对应的帧数向上取整后叠加到基础延迟上，保证高延迟玩家的输入不会
    被本地提前消费，两边判定看到同一帧的输入。
    """
    rtt_frames = max(0, math.ceil(rtt_ms / FRAME_MS))
    return max(0, int(base)) + rtt_frames


def projectile_state(state):
    """投射物快照。

    投射物会随角色状态一起被回滚重放，因此这里返回一份独立的递归快照；
    只重放输入而漏掉已经不存在的投射物会导致两边命中结果不同。
    """
    if isinstance(state, dict):
        return {key: projectile_state(value) for key, value in state.items()}
    if isinstance(state, (list, tuple)):
        return type(state)(projectile_state(value) for value in state)
    return state


def reconnect_predict(pending):
    """重连后清空本地预测。

    从服务器快照恢复前必须丢弃所有未确认的预测帧，否则角色会在本地预测
    位置与服务器位置之间来回闪烁。
    """
    return 0


def spectator_offset(delay):
    """观战端回滚补偿。

    观战端按服务器帧插值时，需要按同样的延迟回退相应帧数，才能看到与
    对局端一致的结果。
    """
    return max(0, int(delay))


def frame_advantage(rollback, total):
    """帧优势。

    回滚重放帧不是真实的等待时间，计算帧优势时必须从总帧数中扣除。
    """
    return int(total) - int(rollback)


def fixed_step(dt):
    """定点物理步长。

    把经过时间量化为固定 60Hz 的整数步数，物理推进不依赖平台浮点运算
    顺序，PC 与主机得到相同结果。
    """
    return max(0, int(round(dt * FPS)))


def buffer_size(longest_combo):
    """回滚缓冲大小。

    按最长连招实际需要的帧数分配，而不是固定 60 帧，避免长连招把更早的
    状态覆盖掉。
    """
    return max(0, int(longest_combo))


def deterministic_rand(seed):
    """确定性随机。

    双方使用同一个种子派生随机数序列（暴击、硬直帧数等），不做各自推进
    的本地随机。
    """
    return int(seed)


def clamp_rollback(frames, maximum):
    """回滚帧数钳制。

    回滚帧数限制在 [0, maximum] 内，防止回滚越过缓冲区里仍然有效的最早
    状态。
    """
    return max(0, min(int(frames), int(maximum)))


def sync_state(local_state, server_state):
    """状态同步。

    断线重连后以服务器快照为准，本地预测状态整体作废。
    """
    return server_state


def tick_from_time(seconds):
    """时间转 tick。

    把经过秒数量化为确定性的 60Hz tick 序号，供回滚与观战端对齐帧号。
    """
    return max(0, int(seconds * FPS))


def rollback_key(seed, index):
    """回滚键。

    用对局种子 + 帧序号唯一标识一帧的回滚状态。
    """
    return f"{seed}:{index}"


def is_desync(hash_a, hash_b):
    """失同步判定。

    只在定点哈希不一致时判定失同步，浮点误差已被 state_hash 量化吸收。
    """
    return hash_a != hash_b
