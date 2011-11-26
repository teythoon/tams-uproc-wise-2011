library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.types.all;

entity alu_tb is
end alu_tb;

architecture behavior of alu_tb is

  component alu
    port (
      operand_0, operand_1 : in data_bus;
      result               : out data_bus;
      Clk        : in std_logic;          -- clock
      OpCode     : in alu_opcode);
  end component;

  for alu_0: alu use entity work.alu;
  
  signal operand_0, operand_1, result : data_bus;
  signal Clk : std_logic;
  signal OpCode : alu_opcode;

begin

  alu_0: alu port map (
    operand_0 => operand_0,
    operand_1 => operand_1,
    result => result,
    Clk => Clk,
    OpCode => OpCode);

  -- purpose: testbench for alu
  -- type   : sequential
  process

    type alu_test is record               -- a single test
      operand_0, operand_1 : data_bus;    -- inputs
      result     : data_bus;              -- result
      OpCode     : alu_opcode;            -- what to do
    end record;

    type alu_tests is array (natural range <>) of alu_test;
    constant tests : alu_tests :=
      ((zero_word, one_word, one_word, alu_add),
       (one_word, one_word, two_word, alu_add),
       (one_word, two_word, zero_word, alu_and));

  begin  -- process
    for i in tests'range loop
      Clk <= '0';
      wait for 1 ns;

      operand_0 <= tests(i).operand_0;
      operand_1 <= tests(i).operand_1;
      OpCode <= tests(i).OpCode;

      Clk <= '1';
      wait for 1 ns;

      assert result = tests(i).Result
        report "bad result" severity error;
    end loop;

    assert false report "end of test" severity note;
    wait;
  end process;

end behavior;
