import time
import threading


class SnowflakeGenerator:
    def __init__(self, datacenter_id, worker_id, epoch) -> None:
        self.dc_id = datacenter_id & 0x1F
        self.worker_id = worker_id & 0x1F
        self.sequence = 0
        self.last_ts = 0
        self._lock = threading.Lock()
        self.epoch = epoch

    def _current_timestamp(self) -> int:
        return int(time.time() * 1000)
     
    def _wait_next_millis(self, last_ts) -> int:
        ts = self._current_timestamp()
        while ts <= last_ts:
            ts = self._current_timestamp()
        return ts

    def next_id(self):
        with self._lock:
            ts = self._current_timestamp()
            if ts == self.last_ts:
                self.sequence = (self.sequence + 1) & 0xFFF
                if self.sequence == 0:
                    ts = self._wait_next_millis(self.last_ts)
            else:
                self.sequence = 0
                self.last_ts = ts
        snowflake = ((ts - self.epoch) << 22) | self.dc_id << 17 | self.worker_id << 12 | self.sequence
        return snowflake
