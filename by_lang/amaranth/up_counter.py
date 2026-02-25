from amaranth import Module, Signal
from amaranth.lib.wiring import In, Out, Component
from amaranth.sim import Simulator, Period

class UpCounter(Component):
    """A 16-bit up counter for the range [0, `limit`]."""

    en: In(1)
    val: Out(16)

    def __init__(self, limit: int) -> None:
        super().__init__()

        assert limit < 2**16
        self.limit = limit
        self.count = Signal(16)

    def elaborate(self, _platform) -> Module:
        m = Module()

        count = self.count
        limit = self.limit

        m.d.comb += self.val.eq(count)

        with m.If(self.en):
            with m.If(count == limit):
                m.d.sync += count.eq(0)
            with m.Else():
                m.d.sync += count.eq(count + 1)

        return m

def main() -> None:
    limit = 15
    uut = UpCounter(limit)

    async def bench(ctx):
        ctx.set(uut.en, 0)
        assert ctx.get(uut.val) == 0

        ctx.set(uut.en, 1)
        for i in range(limit+1):
            assert ctx.get(uut.val) == i
            await ctx.tick()

        assert ctx.get(uut.val) == 0

    sim = Simulator(uut)
    sim.add_clock(Period(MHz=1))
    sim.add_testbench(bench)
    sim.run()

if __name__ == "__main__":
    main()
