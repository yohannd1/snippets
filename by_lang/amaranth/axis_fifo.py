# AXI-Stream FIFO queue
#
# https://github.com/amaranth-lang/amaranth/issues/1523

from amaranth import Module, Signal, unsigned, Cat, C, Shape
from amaranth.lib.memory import Memory
from amaranth.lib.wiring import In, Out, Component
from amaranth.sim import Simulator, Period

class AxisFifo(Component):
    """AXI-Stream compatible FIFO queue."""

    def __init__(self, width, depth) -> None:
        assert depth > 0, "Queue depth/size must be positive"

        self.width = width
        self.depth = depth

        # TODO: experiment using a whole ass signal instead of just receiving the width
        super().__init__({
            # write interface
            "ivalid_in": In(1),
            "idata_in": In(width),
            "iready_out": In(width),

            # read interface
            "ovalid_out": Out(1),
            "odata_out": Out(width),
            "oready_in": In(1),
        })

    def elaborate(self, _platform) -> Module:
        m = Module()

        width = self.width
        depth = self.depth

        ivalid_in = self.ivalid_in
        idata_in = self.idata_in
        iready_out = self.iready_out
        ovalid_out = self.ovalid_out
        odata_out = self.odata_out
        oready_in = self.oready_in

        # https://amaranth-lang.org/docs/amaranth/latest/stdlib/memory.html
        m.submodules.memory = memory = Memory(
            shape=unsigned(width),
            depth=depth,
            init=[0 for _ in range(depth)],
        )

        Address = Shape.cast(range(depth))

        full = Signal(1, init=0)
        empty = Signal(1, init=1)

        iready = ~full
        ovalid = ~empty

        wr_addr = Signal(Address, init=0)
        wr_trans = ivalid_in & iready

        wr_port = memory.write_port()
        m.d.comb += wr_port.en.eq(wr_trans)
        m.d.comb += wr_port.addr.eq(wr_addr)
        m.d.comb += wr_port.data.eq(idata_in)

        rd_addr = Signal(Address, init=0)
        rd_trans = ovalid & oready_in

        rd_port = memory.read_port()
        m.d.comb += rd_port.addr.eq(rd_addr)
        m.d.comb += odata_out.eq(rd_port.data)

        with m.Switch(Cat(wr_trans, rd_trans)):
            with m.Case("00"):
                pass # do nothing

            with m.Case("01"):
                # read out
                m.d.sync += rd_addr.eq(rd_addr + 1)
                m.d.sync += full.eq(0)
                m.d.sync += empty.eq(rd_addr == wr_addr)

            with m.Case("10"):
                # write in
                m.d.sync += wr_addr.eq(wr_addr + 1)
                m.d.sync += empty.eq(0)
                m.d.sync += full.eq(rd_addr == wr_addr)

            with m.Case("11"):
                # both
                m.d.sync += rd_addr.eq(rd_addr + 1)
                m.d.sync += wr_addr.eq(wr_addr + 1)

        m.d.comb += iready_out.eq(iready)
        m.d.comb += ovalid_out.eq(ovalid)

        return m

def main() -> None:
    width = 8
    depth = 7
    uut = AxisFifo(width, depth)

    # from amaranth.back import verilog
    # v_out = verilog.convert(uut, ports=[], emit_src=False)
    # help(verilog.convert)

    async def bench(ctx):
        assert ctx.get(uut.ovalid_out) == 0
        ctx.set(uut.idata_in, 0)
        ctx.set(uut.ivalid_in, 0)
        ctx.set(uut.oready_in, 0)
        await ctx.tick()

        # TODO: validate things...

    sim = Simulator(uut)
    sim.add_clock(Period(MHz=1))
    sim.add_testbench(bench)
    sim.run()

if __name__ == "__main__":
    main()
