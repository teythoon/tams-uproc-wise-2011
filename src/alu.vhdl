library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.types.all;

entity alu is

  port (
    operand_0, operand_1 : in data_bus;
    result               : out data_bus;
    enabled              : in std_logic;
    OpCode     : in alu_opcode);

end alu;

-- Todo: add missing alu operations and encode opcodes

architecture behavior of alu is
begin  -- behavior
  alu_process: process (enabled)
  variable add_result : std_logic_vector(word_width downto 0);  -- one bit wider than word
  begin  -- process
    if(rising_edge(enabled)) then
      case OpCode is
        when alu_add =>
          add_result := std_logic_vector(unsigned('0' & operand_0) + unsigned('0' & operand_1));
          result <= add_result(add_result'high - 1 downto 0);
        --when alu_sub =>
        --  result <= operand_0 - operand_1;
        --when alu_mul =>
        --  result <= operand_0 * operand_1;
        --when alu_div =>
        --  result <= operand_0 / operand_1;
        when alu_and =>
          result <= operand_0 and operand_1;
        when alu_or =>
          result <= operand_0 or operand_1;
        when alu_xor =>
          result <= operand_0 xor operand_1;
        when alu_not =>
          result <= not operand_0;
        when others =>
          NULL;
      end case;
    end if;
  end process;
end behavior;
