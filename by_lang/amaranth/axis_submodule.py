# AXI-Stream submodule test

from amaranth import Module, Signal
from amaranth.lib.wiring import In, Out, Component
from amaranth.sim import Simulator, Period

class AxisStorage(Component):
    """Sample AXI-Stream module. Very simple, just stores one data (overrides
    it if necessary) based on a write-enable signal and outputs it through an
    AXI-Stream interface."""

    def __init__(self, width) -> None:
        self.width = width
        super().__init__({
            "wr_en_in": In(1),
            "data_in": In(width),
            "ovalid_out": Out(1),
            "odata_out": Out(width),
            "oready_in": In(1),
        })

    def elaborate(self, _platform) -> Module:
        m = Module()

        width = self.width
        wr_en_in = self.wr_en_in
        data_in = self.data_in
        ovalid_out = self.ovalid_out
        odata_out = self.odata_out
        oready_in = self.oready_in

        self.data = data = Signal(width)
        self.has_data = has_data = Signal(1)

        # AXI-Stream transaction indicator
        trans = oready_in & has_data

        with m.If(wr_en_in):
            m.d.sync += has_data.eq(wr_en_in)
        with m.Elif(trans):
            m.d.sync += has_data.eq(0)

        with m.If(wr_en_in):
            m.d.sync += data.eq(data_in)

        m.d.comb += ovalid_out.eq(has_data)
        m.d.comb += odata_out.eq(data)

        return m

def main() -> None:
    width = 8
    uut = AxisStorage(width)

    # from amaranth.back import verilog
    # v_out = verilog.convert(uut, ports=[], emit_src=False)
    # help(verilog.convert)

    async def bench(ctx):
        assert ctx.get(uut.ovalid_out) == 0
        ctx.set(uut.wr_en_in, 0)
        ctx.set(uut.oready_in, 0)
        await ctx.tick()

        for v in [10, 100, 80, 31]:
            print(f"SENDING {v}")
            ctx.set(uut.oready_in, 0)
            ctx.set(uut.data_in, v)
            ctx.set(uut.wr_en_in, 1)
            await ctx.tick()

            assert ctx.get(uut.ovalid_out) == 1
            ctx.set(uut.wr_en_in, 0)
            await ctx.tick()

            print(f"{ctx.get(uut.has_data)} {ctx.get(uut.ovalid_out)=}")
            assert ctx.get(uut.ovalid_out) == 1
            assert ctx.get(uut.odata_out) == v
            ctx.set(uut.oready_in, 1)
            await ctx.tick()

            assert ctx.get(uut.ovalid_out) == 0

    sim = Simulator(uut)
    sim.add_clock(Period(MHz=1))
    sim.add_testbench(bench)
    sim.run()

if __name__ == "__main__":
    main()
