`timescale 1ns/1ns

/* WARNING: DO NOT MODIFY THE PREDEFINED NAMES OF THE MODULES AND THE PORTS! */
/* NOTE: YOU CAN ADD NEW MODULES, PORTS, WIRES, AND REGISTERS AS NEEDED! */

//
// RV32I Opcode map = Inst[6:0]
//
`define OP_R		      7'b0110011
`define OP_I_Arith    7'b0010011
`define OP_I_Load     7'b0000011
`define OP_I_JALR     7'b1100111 
`define OP_S          7'b0100011 
`define OP_B          7'b1100011
`define OP_U_LUI      7'b0110111
`define OP_U_AUIPC    7'b0010111
`define OP_J_JAL      7'b1101111

module maindec(input        rst,
               input        clk,
               input  [6:0] opcode,
               output [1:0] ALUSrcA,
               output [1:0] ALUSrcB,
               output       IRWrite,
               output       PCWrite,
               output [1:0] ResultSrc,
               output       RegWrite,
               output       MemWrite,
               output       branch,
               output reg   ALUOp);  //ALU must do add at Fetch stage, ALUOp = 1 to add

  reg [3:0] state, n_state;

  localparam IF 	      = 4'b0000;	    //Fetch
  localparam Decode 	  = 4'b0001;	    //Decode
  localparam ExR 	      = 4'b0010;	    //Execute (R type)
  localparam ExI      = 4'b0011;   // Execute (I-type instruction)
  localparam ExLui    = 4'b0100;   // Execute (U-type LUI instruction)
  localparam ExJal    = 4'b0101;   // Execute (PC + 4) for write rd register and jump to the target address
  localparam WReg     = 4'b0110;   // Write ALU result back to the register
  localparam ExLS     = 4'b0111;   // Execute (Memory access address calculation I-Load and S-type)
  localparam Mem_Read = 4'b1000;   // memory read operation
  localparam WRegL    = 4'b1001;   // Write loaded memory data back to the register
  localparam Mem_Write = 4'b1010;  // memory write operation
  localparam ExJalr   = 4'b1011;   // Execute jump to the target address
  localparam WRegJr   = 4'b1100;   // Execute (PC + 4) for write rd register and write back to the register
  localparam ExB      = 4'b1101;   // Execute (Branch condition evaluation) and branch


  reg [10:0] controls;

  assign {ALUSrcA, ALUSrcB, IRWrite, PCWrite, ResultSrc, RegWrite, MemWrite, branch} = controls;

  always @(negedge clk, negedge rst) begin
    if(!rst)
      state <= IF;
    else
      state <= n_state;
  end

  always @(*) begin
    case(state)
    IF:	begin
      controls <= 11'b00_10_11_00_000; 
      ALUOp <= 1;                      // add, PC + 4
    end
    Decode:	begin
      controls <= 11'b01_01_00_00_000; // calculate target address
      ALUOp <= 1;                      // add, OldPC + imm
    end
    ExR:	begin
      controls <= 11'b10_00_00_00_000; // rs1, rs2
      ALUOp <= 0;
    end
    ExI: begin
      controls <= 11'b10_01_00_00_000; // Use rs1 and immediate value as ALU inputs
      ALUOp <= 0; 
    end
    ExLui: begin
      controls <= 11'b11_01_00_00_000; // Load upper immediate (LUI) value into the register
      ALUOp <= 1; // add, 0 + lui imm
    end
    ExJal: begin
      controls <= 11'b01_10_01_10_000; // Calculate the return address (OldPC + 4) and jump to the target address(calculated in Decode state)
      ALUOp <= 1; //  add, OldPC + 4
    end
    WReg: begin
      controls <= 11'b00_00_00_10_100; // Write ALU result register value to the destination register (rd)
      ALUOp <= 0; 
    end
    ExLS: begin
      controls <= 11'b10_01_00_11_000; // Calculate the memory access address, 
      ALUOp <= 1; // add, rs1 + imm
    end
    Mem_Read: begin
      controls <= 11'b00_00_00_10_000; // Select ALU result register as memory address to read data
      ALUOp <= 0; 
    end
    WRegL: begin
      controls <= 11'b00_00_00_01_100; // Write memory read data to the destination register (rd)
      ALUOp <= 0; 
    end
    Mem_Write: begin
      controls <= 11'b00_00_00_10_010; // Select ALU result register as memory address to write data
      ALUOp <= 0;
    end
    ExJalr: begin
      controls <= 11'b10_01_01_00_000; // Calculate the jump target address (rs1 + imm) and jump
      ALUOp <= 1; // add, rs1 + imm
    end
    WRegJr: begin
      controls <= 11'b01_10_00_00_100; // Write the return address (OldPC + 4) to the destination register (rd)
      ALUOp <= 1; // add, OldPC + 4
    end
    ExB: begin
      controls <= 11'b10_00_00_10_001; // If branch condition is accepted, jump to the target address (calculated in Decode state)
      ALUOp <= 0; 
    end
    default: begin
      controls <= 11'b00_00_00_00_000;
      ALUOp <= 0;
    end
    endcase
  end

  always @(*) begin
    case(state)
    IF:	
    begin
      n_state <= Decode; // After IF state, transition to Decode state
    end
    Decode:	
    begin
      if (opcode == `OP_R) n_state <= ExR; // If opcode is R-type, transition to ExR
      else if (opcode == `OP_I_Arith) n_state <= ExI; // If opcode is I-type Arithmetic, transition to ExI
      else if (opcode == `OP_I_Load || opcode == `OP_S) n_state <= ExLS;  // If opcode is Load or Store, transition to ExLS
      else if (opcode == `OP_B) n_state <= ExB; // If opcode is Branch, transition to ExB
      else if (opcode == `OP_J_JAL) n_state <= ExJal; // If opcode is JAL, transition to ExJal
      else if (opcode == `OP_I_JALR) n_state <= ExJalr; // If opcode is JALR, transition to ExJalr
      else if (opcode == `OP_U_LUI) n_state <= ExLui; // If opcode is LUI, transition to ExLui
    end
    ExR:
    begin 	   
      n_state <= WReg; // After executing R-type, transition to WReg
    end
    ExI:
    begin 	   
      n_state <= WReg; // After executing I-type Arithmetic, transition to WReg
    end
    ExLui:
    begin 	   
      n_state <= WReg; // After executing LUI, transition to WReg
    end
    ExJal:
    begin 	   
      n_state <= WReg; // After executing JAL, transition to WReg
    end
    WReg:
    begin
      n_state <= IF; // Transition back to IF after writing register
    end
    ExLS:
    begin 	
      if (opcode == `OP_I_Load) n_state <= Mem_Read; // If opcode is Load, transition to Mem_Read
      else if (opcode == `OP_S) n_state <= Mem_Write; // If opcode is Store, transition to Mem_Write
    end
    Mem_Read:
    begin 	
      n_state <= WRegL; // After reading memory, transition to WRegL (Write Register Load)
    end
    WRegL:
    begin
      n_state <= IF; // Transition back to IF after writing register
    end
    Mem_Write:
    begin 	
      n_state <= IF; // Transition back to IF after memory write
    end
    ExJalr:
    begin
      n_state <= WRegJr; // Transition to WRegJr after jump to target address
    end
    WRegJr:
    begin 	   
      n_state <= IF; // Transition to IF after writing rd = OldPC + 4 register
    end
    ExB:
    begin
      n_state <= IF; // Transition back to IF after executing Branch 
    end
    default:    n_state <= IF;
    endcase
  end

endmodule

//
// ALU decoder generates ALU control signal (alucontrol)
//
module aludec(input      [6:0] opcode,           // opcode
              input      [6:0] funct7,           // funct7
              input      [2:0] funct3,           // funct3
              input            ALUOp, 
              output reg [4:0] alucontrol);      // ALU control signal

  always @(*)
    if (ALUOp) alucontrol <= 5'b00000;
    else
    begin
      case(opcode)
        `OP_R:   		    // R-type
        begin
          case({funct7,funct3})
          10'b0000000_000: alucontrol <= 5'b00000; // addition (add)
          10'b0100000_000: alucontrol <= 5'b10000; // subtraction (sub)
          10'b0000000_111: alucontrol <= 5'b00001; // and (and)
          10'b0000000_110: alucontrol <= 5'b00010; // or (or)
          default:         alucontrol <= 5'bxxxxx;
          endcase
        end

        `OP_I_Arith:    // I-type Arithmetic
        begin
          case(funct3)
          3'b000:  alucontrol <= 5'b00000; // addi
          3'b110:  alucontrol <= 5'b00010; // ori
          3'b111:  alucontrol <= 5'b00001; // andi
          default: alucontrol <= 5'bxxxxx;
          endcase
        end

        `OP_I_Load: 	  // I-type Load (LW, LH, LB...)
        alucontrol <= 5'b00000; //add

        `OP_I_JALR:		  // I-type Load (JALR)
        alucontrol <= 5'b00000; //add

        `OP_B:   		    // B-type Branch (BEQ, BNE, ...)
        alucontrol <= 5'b10000; //sub

        `OP_S:   		    // S-type Store (SW, SH, SB)
        alucontrol <= 5'b00000; //add

        `OP_U_LUI: 		  // U-type (LUI)
        alucontrol <= 5'b00000; //add
        
        `OP_U_AUIPC:
        alucontrol <= 5'b00000; //add
      
        default:
          alucontrol <= 5'b00000;
      endcase
    end
    
endmodule


//
// CPU datapath
//
module datapath(input         clk, reset_n, // clock and reset signals
                input  [31:0] inst,       // incoming instruction
                input         regwrite,   // register write
                input  [4:0]  alucontrol, // ALU control signal
                input         branch,     // branch
                input         PCWrite, IRWrite,    // PC reg, inst. reg enable
                input  [1:0]  ALUSrcA, ALUSrcB, ResultSrc,  // mux
                output reg [31:0] pc,     // program counter
                output reg [31:0] rd_data,
                output [31:0] aluout,     // ALU output
                output [31:0] MemWdata,   // data to write to memory
                input  [31:0] MemRdata,   // data read from memory
                input  [31:0] OldPC);     // save current PC  

  wire [4:0]  rs1, rs2, rd;               // register addresses
  wire [6:0]  opcode;                     // opcode
  wire [2:0]  funct3;                     // funct3
  wire [31:0] rs1_data, rs2_data;         // data read from registers
  wire [20:1] jal_imm;                    // JAL immediate
  wire [31:0] se_jal_imm;                 // sign-extended JAL immediate
  wire [12:1] jalr_imm;                   // JALR immediate
  wire [31:0] se_jalr_imm;                // sign-extended JALR immediate
  wire [12:1] br_imm;                     // branch immediate
  wire [31:0] se_br_imm;                  // sign-extended branch immediate
  wire [31:0] se_imm_itype;               // sign-extended I-type immediate
  wire [31:0] se_imm_stype;               // sign-extended S-type immediate
  wire [31:0] auipc_lui_imm;              // AUIPC and LUI immediate
  reg  [31:0] alusrc1;                    // 1st source to ALU
  reg  [31:0] alusrc2;                    // 2nd source to ALU
  reg  [31:0] rs1_data_reg, rs2_data_reg; // registers that hold data from register file
  reg  [31:0] aluout_reg;                 // alu out register
  wire		  Nflag, Zflag, Cflag, Vflag;           // DO NOT MODIFY THESE PORTS!
  wire		  f3beq, f3bne, f3blt, f3bgeu;          // funct3 for branch
  wire		  beq_taken;                            // branch taken (BEQ)
  wire		  bne_taken;                            // branch taken (BNE)
  wire 		  bgeu_taken;                           // branch taken (BGEU)
  wire		  blt_taken;                            // branch taken (BLT)

  assign beq_taken  =  branch & f3beq & Zflag;
  assign bne_taken  =  branch & f3bne & ~Zflag;
  assign blt_taken  =  branch & f3blt & (Nflag != Vflag);
  assign bgeu_taken =  branch & f3bgeu & Cflag;

  assign MemWdata = rs2_data_reg;                  

  // JAL immediate
  assign jal_imm[20:1] = {inst[31],inst[19:12],inst[20],inst[30:21]};
  assign se_jal_imm[31:0] = {{11{jal_imm[20]}},jal_imm[20:1],1'b0};
  
  // JALR immediate
  assign jalr_imm[12:1] = {inst[31:20]};
  assign se_jalr_imm[31:0] = {{19{jalr_imm[12]}},jalr_imm[12:1],1'b0};

  // Branch immediate
  assign br_imm[12:1] = {inst[31],inst[7],inst[30:25],inst[11:8]};
  assign se_br_imm[31:0] = {{19{br_imm[12]}},br_imm[12:1],1'b0};

	assign se_imm_itype[31:0] = {{20{inst[31]}},inst[31:20]};
	assign se_imm_stype[31:0] = {{20{inst[31]}},inst[31:25],inst[11:7]};
	assign auipc_lui_imm[31:0] = {inst[31:12],12'b0};

  /* ------------------------------------------------------------------------ */

  assign rs1 = inst[19:15];   // register rs1
  assign rs2 = inst[24:20];                                     
  assign rd  = inst[11:7];                                    
  assign funct3  = inst[14:12];                               
  assign opcode  = inst[6:0];
  //
  // PC (Program Counter) logic 
  //
  assign f3beq  = (funct3 == 3'b000); // BEQ
  assign f3bne  = (funct3 == 3'b001);                                                
  assign f3blt  = (funct3 == 3'b100);                                                 
  assign f3bgeu = (funct3 == 3'b111);                                                

  // Program Counter (PC) logic
  always @(negedge clk, negedge reset_n)
  begin
    if (!reset_n)
      pc <= 0;                                                
    else if (PCWrite | beq_taken | bne_taken | blt_taken | bgeu_taken)       
    begin
	    pc <= rd_data; // Assign the value of rd_data to pc (calculated in rd_data logic)
    end
  end
  
	// 1st source to ALU (alusrc1)
  always @(*)  
  begin
    if      (ALUSrcA == 2'b00) alusrc1[31:0] = pc; 
    else if (ALUSrcA == 2'b01) alusrc1[31:0] = OldPC; // If ALUSrcA is 2'b01, assign OldPC to alusrc1  
    else if (ALUSrcA == 2'b10) alusrc1[31:0] = rs1_data_reg; // If ALUSrcA is 2'b10, assign rs1_data_reg to alusrc1
    else alusrc1[31:0] = 32'd0; // assign 0 to alusrc1 (used for LUI immediate calculation)
  end 

  // 2nd source to ALU (alusrc2)
  always @(*)  
  begin
    if      (ALUSrcB == 2'b00) alusrc2[31:0] = rs2_data_reg;
    else if (ALUSrcB == 2'b01) begin
      if (opcode == `OP_B) alusrc2[31:0] = se_br_imm[31:0]; // For branch instructions, use the branch immediate as the second ALU input.
      else if (opcode == `OP_J_JAL) alusrc2[31:0] = se_jal_imm[31:0];// For JAL (Jump and Link) instruction, use the JAL immediate as the second ALU input.
      else if (opcode == `OP_I_JALR) alusrc2[31:0] = se_jalr_imm[31:0]; // For JALR (Jump and Link Register) instruction, use the JALR immediate as the second ALU input.
      else if ((opcode == `OP_I_Arith) || (opcode == `OP_I_Load)) alusrc2[31:0] = se_imm_itype[31:0]; // For I-type instructions use the I-type immediate as the second ALU input.
      else if (opcode == `OP_S) alusrc2[31:0] = se_imm_stype[31:0]; // For S-type instructions, use the S-type immediate as the second ALU input.
      else if (opcode == `OP_U_LUI) alusrc2[31:0] = auipc_lui_imm[31:0]; // For U-type instructions (LUI), use the U-type immediate as the second ALU input.
    end
    else if (ALUSrcB == 2'b10) alusrc2[31:0] = 32'd4; // For pc + 4 or OldPC + 4
    else alusrc2[31:0] = 32'd0; // no case, deault 0
  end
	// result for register file, memory, and PC (rd_data)
	always @(*)
	begin
		if	    (ResultSrc == 2'b00)  rd_data[31:0] = aluout;
		else if (ResultSrc == 2'b01)  rd_data[31:0] = MemRdata; // Write memory read data to rd_data
		else if (ResultSrc == 2'b10)  rd_data[31:0] = aluout_reg; // Write ALU output register to rd_data
		else rd_data[31:0] = 32'b0; // To prevent unnecessary rd_data(set rd_data = 0) assignments and speed up the timer increment, it is used in the ExLS state(I-Load or S-type).
	end

  // rd1 register 
  always @(negedge clk, negedge reset_n) 
  begin
    if (!reset_n) rs1_data_reg <= 0;
    else rs1_data_reg <= rs1_data; //set rs1_data register to rs1_data for use another state
  end

  // rd2 register 
  always @(negedge clk, negedge reset_n) 
  begin
    if (!reset_n) rs2_data_reg <= 0;
    else rs2_data_reg <= rs2_data; //set rs2_data register to rs2_data for use another state
  end
  // ALUOut register 
  always @(negedge clk, negedge reset_n) 
  begin
    if (!reset_n) aluout_reg <= 0;
    else aluout_reg <= aluout; //set aluout register to aluout for use next state
  end

  regfile i_regfile(
    .clk			(clk),
    .we			  (regwrite),
    .rs1			(rs1),
    .rs2			(rs2),
    .rd			  (rd),
    .rd_data	(rd_data),
    .rs1_data	(rs1_data),
    .rs2_data	(rs2_data));

	alu i_alu(
		.a			  (alusrc1),
		.b			  (alusrc2),
		.alucont	(alucontrol),
		.result	  (aluout),
		.N			  (Nflag),
		.Z			  (Zflag),
		.C			  (Cflag),
		.V			  (Vflag));

endmodule

module RV32I (
		      input         clk, reset_n, // clock and reset signals
          output [31:0] pc,		  		// program counter for instruction fetch
          input  [31:0] inst, 			// incoming instruction
          output [3:0] 	be,         // DO NOT MODIFY THIS PORT!
          output        Memwrite, 	// 'memory write' control signal
          output 				Memread,    // 'memory read' control signal
          output [31:0] Memaddr,  	// memory address 
          output [31:0] MemWdata, 	// data to write to memory
          input  [31:0] MemRdata); 	// data read from memory

  wire [4:0]  alucontrol;
  wire        IRWrite, PCWrite, RegWrite, MemWrite;           
  wire [1:0]  ALUSrcA, ALUSrcB, ResultSrc; 
  wire        branch;
  reg  [31:0] inst_reg, OldPC;           
  reg  [31:0] MemRdata_reg;      
  assign Memwrite = MemWrite;
  assign Memread = ~MemWrite;
  assign be = 4'b1111;

  // inst, OldPC register
  always @(negedge clk, negedge reset_n) 
  begin
    if (!reset_n)  
    begin
      inst_reg <= 0;
      OldPC <= 0;
    end
    else if (IRWrite)   
    begin
      inst_reg <= inst; // //set inst_reg to inst when IRWrite signal was enable(IF state) for use another state
      OldPC <= pc; //set OldPC to pc when IRWrite signal was enable(IF state) for use another state
    end
  end

  // MemRdata register
  always @(negedge clk, negedge reset_n) 
  begin
    if (!reset_n)  MemRdata_reg <= 0;
    else MemRdata_reg <= MemRdata; // set MemRdata register to MemRdata for use next state
  end


  // Instantiate Controller
  controller i_controller(
    .opcode		  (inst_reg[6:0]), 
		.funct7		  (inst_reg[31:25]), 
		.funct3		  (inst_reg[14:12]), 
    .reset_n    (reset_n),
    .clk        (clk),
    .inst       (inst_reg[31:0]),
		.alucontrol	(alucontrol),
    .ALUSrcA    (ALUSrcA),
    .ALUSrcB    (ALUSrcB),
    .IRWrite    (IRWrite),
    .PCWrite    (PCWrite),
    .ResultSrc  (ResultSrc),
    .RegWrite   (RegWrite),
    .MemWrite   (MemWrite),
    .branch     (branch));

  // Instantiate Datapath
  datapath i_datapath(
		.clk				(clk),
		.reset_n		(reset_n),
		.branch			(branch),
		.regwrite		(RegWrite),
    .PCWrite    (PCWrite),
    .IRWrite    (IRWrite),
    .ALUSrcA    (ALUSrcA),
    .ALUSrcB    (ALUSrcB),
    .ResultSrc  (ResultSrc),
		.alucontrol	(alucontrol),
		.pc				  (pc),
    .rd_data    (Memaddr),
		.inst				(inst_reg),
		.aluout			(aluout), 
		.MemWdata		(MemWdata),
		.MemRdata		(MemRdata_reg),
    .OldPC      (OldPC));

endmodule

//
// Instruction Decoder 
// to generate control signals for datapath
//
module controller(input  [6:0] opcode,
                  input  [6:0] funct7,
                  input  [2:0] funct3,
                  input        reset_n,
                  input        clk,
                  input  [31:0] inst,
                  output [4:0] alucontrol,
                  output [1:0] ALUSrcA,
                  output [1:0] ALUSrcB,
                  output       IRWrite,
                  output       PCWrite,
                  output [1:0] ResultSrc,
                  output       RegWrite,
                  output       MemWrite,
                  output branch);

  maindec i_maindec(
    .rst       (reset_n),
    .clk       (clk),
    .opcode    (opcode),
    .ALUSrcA   (ALUSrcA),
    .ALUSrcB   (ALUSrcB),
    .IRWrite   (IRWrite),
    .PCWrite   (PCWrite),
    .ResultSrc (ResultSrc),
    .RegWrite  (RegWrite),
    .MemWrite  (MemWrite),
    .branch    (branch),
    .ALUOp     (ALUOp));

	aludec i_aludec( 
		.opcode     (opcode),
		.funct7     (funct7),
		.funct3     (funct3),
    .ALUOp      (ALUOp),
		.alucontrol (alucontrol));

endmodule