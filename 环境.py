import sys

def create_globals():

    def local_str(x):
        return str(x)

    def local_print(*objs, sep=' ', end='', file=sys.stdout, flush=False):
        """Prints thy values to a stream, or to stdout by default."""
        for obj in objs:
            file.write(local_str(obj))
            if obj != objs[(-1)]:
                file.write(sep)

        file.write(end)
        if flush:
            file.flush()

    return {'print':local_print}