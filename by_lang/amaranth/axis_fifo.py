# AXI-Stream FIFO queue
#
# https://github.com/amaranth-lang/amaranth/issues/1523

from amaranth import Module, Signal, unsigned, Cat, C, Shape, Mux
from amaranth.lib.memory import Memory
from amaranth.lib.wiring import In, Out, Component
from amaranth.sim import Simulator, Period

class AxisFifo(Component):
    """AXI-Stream compatible FIFO queue."""

    def __init__(self, shape, depth) -> None:
        assert depth > 0, "Queue depth/size must be positive"

        self.shape = shape
        self.depth = depth

        super().__init__({
            # write interface
            "ivalid_in": In(1),
            "idata_in": In(shape),
            "iready_out": In(1),

            # read interface
            "ovalid_out": Out(1),
            "odata_out": Out(shape),
            "oready_in": In(1),
        })

    def elaborate(self, _platform) -> Module:
        m = Module()

        shape = self.shape
        depth = self.depth

        ivalid_in = self.ivalid_in
        idata_in = self.idata_in
        iready_out = self.iready_out
        ovalid_out = self.ovalid_out
        odata_out = self.odata_out
        oready_in = self.oready_in

        # https://amaranth-lang.org/docs/amaranth/latest/stdlib/memory.html
        m.submodules.memory = memory = Memory(
            shape=self.shape,
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
        m.d.comb += [
            wr_port.en.eq(wr_trans),
            wr_port.addr.eq(wr_addr),
            wr_port.data.eq(idata_in),
        ]

        rd_addr = Signal(Address, init=0)
        rd_trans = ovalid & oready_in

        rd_port = memory.read_port(domain="comb")
        m.d.comb += [
            rd_port.addr.eq(rd_addr),
            odata_out.eq(rd_port.data),
        ]

        next_rd_addr = Mux(rd_addr == depth - 1, 0, rd_addr + 1)
        next_wr_addr = Mux(wr_addr == depth - 1, 0, wr_addr + 1)

        with m.Switch(Cat(rd_trans, wr_trans)):
            with m.Case("00"):
                pass # do nothing

            with m.Case("01"):
                # read out
                m.d.sync += [
                    rd_addr.eq(next_rd_addr),
                    full.eq(0),
                    empty.eq(next_rd_addr == wr_addr),
                ]

            with m.Case("10"):
                # write in
                m.d.sync += [
                    wr_addr.eq(next_wr_addr),
                    empty.eq(0),
                    full.eq(rd_addr == next_wr_addr),
                ]

            with m.Case("11"):
                # both
                m.d.sync += [
                    rd_addr.eq(next_rd_addr),
                    wr_addr.eq(next_wr_addr),
                ]

        m.d.comb += iready_out.eq(iready)
        m.d.comb += ovalid_out.eq(ovalid)

        return m

def main() -> None:
    width = 8
    depth = 7
    uut = AxisFifo(unsigned(width), depth)

    # from amaranth.back import verilog
    # v_out = verilog.convert(uut, ports=[], emit_src=False)
    # help(verilog.convert)

    async def bench(ctx):
        assert ctx.get(uut.ovalid_out) == 0
        assert ctx.get(uut.iready_out) == 1
        ctx.set(uut.idata_in, 0)
        ctx.set(uut.ivalid_in, 0)
        ctx.set(uut.oready_in, 0)
        await ctx.tick()

        values = [(i + 1) * 2 for i in range(depth)]

        for v in values:
            assert ctx.get(uut.iready_out) == 1
            ctx.set(uut.idata_in, v)
            ctx.set(uut.ivalid_in, 1)
            await ctx.tick()

            assert ctx.get(uut.ovalid_out) == 1

        assert ctx.get(uut.iready_out) == 0
        ctx.set(uut.ivalid_in, 0)

        for v in values:
            assert ctx.get(uut.odata_out) == v
            ctx.set(uut.oready_in, 1)
            await ctx.tick()

        assert ctx.get(uut.ovalid_out) == 0

    sim = Simulator(uut)
    sim.add_clock(Period(MHz=1))
    sim.add_testbench(bench)
    with sim.write_vcd("waveform.vcd"):
        sim.run()

if __name__ == "__main__":
    main()
