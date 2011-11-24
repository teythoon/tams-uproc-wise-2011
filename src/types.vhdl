library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package types is
  constant word_width : integer := 32;
  constant zero_word : std_logic_vector(word_width - 1 downto 0) := (others => '0');  -- zero result
  subtype data_bus is std_logic_vector(word_width - 1 downto 0);   -- word type
  
  type alu_opcode is (
    alu_add, alu_sub, alu_mul, alu_div,
    alu_and, alu_or, alu_xor, alu_not);                          -- opcodes

end types;
