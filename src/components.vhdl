library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.types.all;

package components is
  component alu is
    port (
      operand_0, operand_1 : in data_bus;
      result               : out data_bus;
      Clk        : in std_logic;          -- clock
      OpCode     : in alu_opcode);
  end component;
end components;
