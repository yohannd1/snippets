// Tri-state buffer implementation in SystemVerilog.

module tri_buf #(type T) (
  input logic rw,
  input T data,
  inout T bus
);
  assign bus = rw ? data : 'bZ;
endmodule

`timescale 1ns/1ns
module tb_tri_buf;
  typedef logic[7:0] bus_t;

  logic rw;
  bus_t bus, data;
  tri_buf #( .T(bus_t) ) uut( .* );

  localparam bus_t all_z = 'bZ;

  initial begin
    rw = 0;
    #1;
    assert (bus === all_z);

    data = 5;
    rw = 1;
    #1;
    assert (bus == 5);

    rw = 0;
    data = 6;
    #1;
    assert (bus === all_z);

    rw = 1;
    #1;
    assert (bus == 6);

    $finish;
  end
endmodule
