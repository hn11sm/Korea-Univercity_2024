//altpll CBX_DECLARE_ALL_CONNECTED_PORTS="OFF" clk0_divide_by=1 clk0_duty_cycle=50 clk0_multiply_by=1 clk0_phase_shift="0" clk1_divide_by=1 clk1_duty_cycle=50 clk1_multiply_by=1 clk1_phase_shift="25000" compensate_clock="CLK0" device_family="Cyclone IV E" inclk0_input_frequency=100000 intended_device_family="Cyclone IV E" operation_mode="normal" port_clk0="PORT_USED" port_clk1="PORT_USED" port_clk2="PORT_UNUSED" port_clk3="PORT_UNUSED" port_clk4="PORT_UNUSED" port_clk5="PORT_UNUSED" port_extclk0="PORT_UNUSED" port_extclk1="PORT_UNUSED" port_extclk2="PORT_UNUSED" port_extclk3="PORT_UNUSED" port_inclk1="PORT_UNUSED" port_phasecounterselect="PORT_UNUSED" port_phasedone="PORT_UNUSED" port_scandata="PORT_UNUSED" port_scandataout="PORT_UNUSED" clk inclk locked
//VERSION_BEGIN 9.1SP2 cbx_altpll 2010:03:24:20:43:42:SJ cbx_cycloneii 2010:03:24:20:43:43:SJ cbx_mgl 2010:03:24:21:01:05:SJ cbx_stratixii 2010:03:24:20:43:43:SJ cbx_util_mgl 2010:03:24:20:43:43:SJ  VERSION_END
//CBXI_INSTANCE_NAME="RV32I_System_ALTPLL_clkgen_pll0_altpll_altpll_component"
// synthesis VERILOG_INPUT_VERSION VERILOG_2001
// altera message_off 10463



// Copyright (C) 1991-2010 Altera Corporation
//  Your use of Altera Corporation's design tools, logic functions 
//  and other software and tools, and its AMPP partner logic 
//  functions, and any output files from any of the foregoing 
//  (including device programming or simulation files), and any 
//  associated documentation or information are expressly subject 
//  to the terms and conditions of the Altera Program License 
//  Subscription Agreement, Altera MegaCore Function License 
//  Agreement, or other applicable license agreement, including, 
//  without limitation, that your use is for the sole purpose of 
//  programming logic devices manufactured by Altera and sold by 
//  Altera or its authorized distributors.  Please refer to the 
//  applicable agreement for further details.



//synthesis_resources = cycloneive_pll 1 
//synopsys translate_off
`timescale 1 ps / 1 ps
//synopsys translate_on
module  ALTPLL_clkgen_altpll
	( 
	clk,
	inclk,
	locked) /* synthesis synthesis_clearbox=1 */;
	output   [5:0]  clk;
	input   [1:0]  inclk;
	output   locked;
`ifndef ALTERA_RESERVED_QIS
// synopsys translate_off
`endif
	tri0   [1:0]  inclk;
`ifndef ALTERA_RESERVED_QIS
// synopsys translate_on
`endif

	wire  [4:0]   wire_pll1_clk;
	wire  wire_pll1_fbout;
	wire  wire_pll1_locked;

	cycloneive_pll   pll1
	( 
	.activeclock(),
	.clk(wire_pll1_clk),
	.clkbad(),
	.fbin(wire_pll1_fbout),
	.fbout(wire_pll1_fbout),
	.inclk(inclk),
	.locked(wire_pll1_locked),
	.phasedone(),
	.scandataout(),
	.scandone(),
	.vcooverrange(),
	.vcounderrange()
	`ifndef FORMAL_VERIFICATION
	// synopsys translate_off
	`endif
	,
	.areset(1'b0),
	.clkswitch(1'b0),
	.configupdate(1'b0),
	.pfdena(1'b1),
	.phasecounterselect({3{1'b0}}),
	.phasestep(1'b0),
	.phaseupdown(1'b0),
	.scanclk(1'b0),
	.scanclkena(1'b1),
	.scandata(1'b0)
	`ifndef FORMAL_VERIFICATION
	// synopsys translate_on
	`endif
	);
	defparam
		pll1.clk0_divide_by = 1,
		pll1.clk0_duty_cycle = 50,
		pll1.clk0_multiply_by = 1,
		pll1.clk0_phase_shift = "0",
		pll1.clk1_divide_by = 1,
		pll1.clk1_duty_cycle = 50,
		pll1.clk1_multiply_by = 1,
		pll1.clk1_phase_shift = "25000",
		pll1.compensate_clock = "clk0",
		pll1.inclk0_input_frequency = 100000,
		pll1.operation_mode = "normal",
		pll1.lpm_type = "cycloneive_pll";
	assign
		clk = {1'b0, wire_pll1_clk[4:0]},
		locked = wire_pll1_locked;
endmodule //ALTPLL_clkgen_altpll
//VALID FILE
