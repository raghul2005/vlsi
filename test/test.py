# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start 1-bit Full Adder Verification")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset sequence
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Testing all 8 combinations of A, B, and Cin")

    # Loop through all combinations of A (ui_in[0]), B (ui_in[1]), and Cin (ui_in[2])
    for a in range(2):
        for b in range(2):
            for cin in range(2):
                
                # Map inputs: ui_in[0]=A, ui_in[1]=B, ui_in[2]=Cin
                dut.ui_in.value = (cin << 2) | (b << 1) | a

                # Wait for one clock cycle
                await ClockCycles(dut.clk, 1)

                # Compute expected software values
                expected_sum  = a ^ b ^ cin
                expected_cout = (a & b) | (cin & (a ^ b))

                # Extract actual hardware values (bit 0 of uo_out and uio_out)
                actual_sum  = int(dut.uo_out.value) & 1
                actual_cout = int(dut.uio_out.value) & 1

                dut._log.info(f"Inputs -> A:{a}, B:{b}, Cin:{cin} | Expected -> Sum:{expected_sum}, Cout:{expected_cout} | Got -> Sum:{actual_sum}, Cout:{actual_cout}")

                # Assertions to verify correctness
                assert actual_sum == expected_sum, f"Sum mismatch for A={a}, B={b}, Cin={cin}: got {actual_sum}, expected {expected_sum}"
                assert actual_cout == expected_cout, f"Cout mismatch for A={a}, B={b}, Cin={cin}: got {actual_cout}, expected {expected_cout}"

    dut._log.info("All 1-bit full adder tests passed successfully!")
