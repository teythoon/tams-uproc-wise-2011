library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package types is
  constant word_width : integer := 32;

  subtype data_bus is std_logic_vector(word_width - 1 downto 0);   -- word type

  constant z_word     : std_logic_vector(word_width - 1 downto 0) := (others => 'Z');
  constant zero_word  : data_bus := data_bus(to_signed(0, word_width));
  constant one_word   : data_bus := data_bus(to_signed(1, word_width));
  constant two_word   : data_bus := data_bus(to_signed(2, word_width));
  constant three_word : data_bus := data_bus(to_signed(3, word_width));
  
  type alu_opcode_t is (
    alu_add, alu_sub, alu_mul, alu_div,
    alu_and, alu_or, alu_xor, alu_not);                          -- opcodes

end types;
