// CORDIC Implementation Testbench
// Rory Brennan 18237606

`timescale 1ns/1ps

module CORDIC_TESTBENCH;

	// Inputs
	reg [1:-16] angle;
	reg clk;
	reg init;
	
	// Outputs
	wire [1:-16] cos, sine;
	wire done;
	reg finished;
	
	// Module instantiation
	CORDIC TEST_RUN(cos, sine, done, angle, init, clk);
	
	// Generate clock
	initial begin 
		forever begin
		clk = 0;
		#5 clk = ~clk;
		end 
	end
	
	// Go through test angles
	initial begin
		
		init = 0;
		#5
		
		// Test 1
		$display("Test 1: 60 degrees");
		angle = 18'b01_0000110000010101; // 60 degrees
		init = 1;
		
		#5
		init = 0;
		
		#300
		// Check if calculation done, if so load new angle
		// Display output cosine and sine values in binary format
		// Report will convert binary results to radians
		if (done == 1) begin
			$display("Results: Cos=%b Sine=%b", cos, sine);
			angle = 18'b00_1100100100001111; // 45 degrees
			init = 1;
		end
		
		// Test 2
		$display("Test 2: 45 degrees");
		
		#5
		init = 0;
		
		#300
		if (done == 1) begin
			$display("Results: Cos=%b Sine=%b", cos, sine);
			angle = 18'b10_1100100100001111; // -45 degrees
			init = 1;
		end
		
		// Test 3
		$display("Test 3: -45 degrees");
		
		#5
		init = 0;
		
		#300
		if (done == 1) begin
			$display("Results: Cos=%b Sine=%b", cos, sine);
			angle = 18'b00_1000011000001010; // 30 degrees
			init = 1;
		end
		
		// Test 4
		$display("Test 4: 30 degrees");
		
		#5
		init = 0;
		
		
		#300
		if (done == 1) begin
			$display("Results: Cos=%b Sine=%b", cos, sine);
			angle = 18'b10_0010110010101110; // -10 degrees
			init = 1;
		end
		
		// Test 5
		$display("Test 5: -10 degrees");
		
		#5
		init = 0;
		
		#300 // After final test, stop program
		if (done == 1) begin
			$display("Results: Cos=%b Sine=%b", cos, sine);
			$stop;
		end
		
	end
	
	
endmodule