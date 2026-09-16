/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // ui_in[0]: A, ui_in[1]: B, ui_in[2]: Cin
    output wire [7:0] uo_out,   // uo_out[0]: Sum
    input  wire [7:0] uio_in,   // IOs: Input path (unused)
    output wire [7:0] uio_out,  // uio_out[0]: Cout
    output wire [7:0] uio_oe,   // IOs: Enable path (1 = output, 0 = input)
    input  wire       ena,      // always 1 when the design is powered
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Internal wires for the 1-bit inputs
    wire a   = ui_in[0];
    wire b   = ui_in[1];
    wire cin = ui_in[2];

    // Full Adder Logic equations
    wire sum  = a ^ b ^ cin;
    wire cout = (a & b) | (cin & (a ^ b));

    // Assign outputs (pad remaining bits with 0)
    assign uo_out  = {7'b0, sum};
    assign uio_out = {7'b0, cout};
    
    // Configure uio_out[0] as an output (active high)
    assign uio_oe  = 8'b00000001;

    // List all unused inputs to prevent synthesis/lint warnings
    wire _unused = &{ena, clk, rst_n, ui_in[7:3], uio_in, 1'b0};

endmodule
