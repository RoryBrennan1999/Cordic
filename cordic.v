// CORDIC Implementation
// Rory Brennan 18237606

module CORDIC(output signed[1:-16] cosine,
            output signed[1:-16] sine,
            output done,
            input signed[1:-16] target_angle,
            input init, clk);
			
	parameter ITERATIONS = 15;
	
	// Register flip flops to hold results/flags
	reg signed [1:-16] sine;
	reg signed [1:-16] cosine;
	reg done;
			
	// Generate table of atan values
	wire signed [1:-16] atan_table [0:16-1];
	assign atan_table[00] = 18'b00_1100100100001111; // 0.78539 rads -> atan(2^0)
	assign atan_table[01] = 18'b00_0111011010110001; // 0.46364 rads -> atan(2^-1)
	assign atan_table[02] = 18'b00_0011111010110110; // 0.12435 rads -> atan(2^-2)
	assign atan_table[03] = 18'b00_0001111111010101; // atan(2^-3)
	assign atan_table[04] = 18'b00_0000111111111010;
	assign atan_table[05] = 18'b00_0000011111111110;
	assign atan_table[06] = 18'b00_0000001111111111;
	assign atan_table[07] = 18'b00_0000000111111111;
	assign atan_table[08] = 18'b00_0000000011111111;
	assign atan_table[09] = 18'b00_0000000001111111;
	assign atan_table[10] = 18'b00_0000000000111111;
	assign atan_table[11] = 18'b00_0000000000011111;
	assign atan_table[12] = 18'b00_0000000000001111;
	assign atan_table[13] = 18'b00_0000000000000111;
	assign atan_table[14] = 18'b00_0000000000000011;
	assign atan_table[15] = 18'b00_0000000000000001;
	
	reg signed [1:-16] C; // cos result
    reg signed [1:-16] S; // sine result
    reg signed [1:-16] A; // angle result
	
	// Difference vectors
	reg signed [1:-16] dA;
	reg signed [1:-16] dC;
	reg signed [1:-16] dS;
	
	reg [5:0] i; // Cycle counter
	reg stage;   // 0: Initial Stage
				 // 1: 0 ----> (n - 1) Stage
	
	// Main behavioural block
	always @(posedge clk) begin
		if (init) begin
			stage = 0;
			done <= 0;
			cosine <= 0;
			sine <= 0;
			C = 0;
			S = 0;
			A = 0;
			i = 0;
		end 
		else begin
			case (stage)
				0: begin // Initial Stage
					C = 18'b00_1001101101111011; // constant K, 0.60725
					S = 0;
					A = 0;
					i = 0;
					done <= 0;
					stage = 1;
				end
				1: begin // 0 ---> n - 1 Stage
					
					// Update rules
					dC = (S >>> i);
					dS = (C >>> i);
					dA = atan_table[i];
					
					if ( A > {1'b0,target_angle[0:-16]} ) begin // overshoot
						C = C + dC;
						S = S - dS;
						A = A - dA;
					end else begin // undershoot
						C = C - dC;
						S = S + dS;
						A = A + dA;
					end
					
					// Check if max number of iterations reached
					// Final stage flip flops
					if (i == (ITERATIONS - 1)) begin
						done <= 1;
						// If angle is negative, sine result is 
						// negative of sine of positive angle
						if (target_angle < 0) begin
							sine <= {1'b1,S[0:-16]};
						end else begin
							sine <= S;
						end
						cosine <= C;
					// Iterate
					end else begin
						i = i + 1;
					end
				end
			endcase
		end
	end
	
endmodule