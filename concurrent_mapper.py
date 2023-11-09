import concurrent.futures as cf
import logging
logger = logging.getLogger(__name__)

class PseudoFuture():
    def __init__(self, aresult):
        self.aresult = aresult
    def done(self):
        return True
    def result(self, timeout=None):
        return self.aresult
    def cancel(self):
        return False
    def cancelled(self):
        return False
    def running(self):
        return False

class PseudoPoolExecutor(cf.Executor):
    def __init__(self, max_workers) -> None:
        super().__init__()

    def submit(self, __fn, *args, **kwargs):
        return PseudoFuture(__fn(*args, **kwargs))

def iterator_split(an_iterable, chunk_size = 0):
    if chunk_size <= 0:
        yield an_iterable
        return 
    chunk = []
    for i, item in enumerate(an_iterable, 1):
        chunk.append(item)
        if i % chunk_size == 0:
            yield chunk
            chunk = []
    if len(chunk) > 0:
        yield chunk

def concurrent_submit(*, fn, tasks, other_args=tuple(), kwargs=dict(), nproc = 4, chunk_size = 0, mode = 'mt'):
    # make sure the config make sense
    if nproc <= 1:
        chunk_size=0
        nproc = 1
        mode = 'seq'
    if mode == 'seq':
        nproc = 1
        chunk_size = 0
    if nproc < chunk_size:
        logger.warning(f'chunk size {chunk_size} is less then nproc {nproc}, may affect performance')
    # make the correct pool
    if mode.lower() == 'seq':
        pool_cls =    PseudoPoolExecutor
    elif mode.lower() == 'mt':
        pool_cls = cf.ThreadPoolExecutor
    elif mode.lower() == 'mp':
        pool_cls = cf.ProcessPoolExecutor
    else:
        raise ValueError(f'Please set mode to "mp", "mt", or "seq"')
    tasks_chunks = iterator_split(tasks, chunk_size)
    for tasks_chunk in tasks_chunks:
        pool = pool_cls(max_workers=nproc)
        futures_queue = []
        for task in tasks_chunk:
            task_with_initial_args = (task,) + other_args
            if len(futures_queue) < nproc:
                futures_queue.append(pool.submit(fn, *task_with_initial_args, **kwargs))
            else:
                yield futures_queue.pop(0).result()
                futures_queue.append(pool.submit(fn, *task_with_initial_args, **kwargs))
            while len(futures_queue) > 0 and futures_queue[0].done():
                yield futures_queue.pop(0).result()
        for future in futures_queue:
            yield future.result()
        pool.shutdown()
