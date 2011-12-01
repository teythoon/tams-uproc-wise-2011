library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.types.all;

entity control is
  port (
    -- TODO: enable later
    --instruction : in opcode;            -- instruction to execute
    interrupt   : in std_logic;         -- interrupt input
    clock       : in std_logic;         -- clock signal

    -- alu signals
    alu_operand_0   : out data_bus;
    alu_operand_1   : out data_bus;
    alu_result      : in data_bus;
    alu_instruction : out alu_opcode_t;   -- alu instruction
    alu_enabled     : out std_logic;    -- enable alu?

    -- register signals
    register_select_a, register_select_b : out integer range 1 to 32;
    register_value_a, register_value_b   : inout data_bus;
    register_write, register_enabled     : out std_logic);
end control;

architecture behavior of control is

begin  -- behavior

  -- purpose: control execution of the current instruction
  -- type   : sequential
  -- inputs : clock, instruction, interrupt
  -- outputs: various
  execute: process (clock)
  begin  -- process execute
    if clock'event then
      -- initialize signals
      alu_enabled <= '0';
      register_value_a <= z_word;
      register_value_b <= z_word;
      register_enabled <= '0';
    
      if clock = '1' then
        -- rising clock edge
        alu_operand_0 <= one_word;
        alu_operand_1 <= two_word;
        alu_instruction <= alu_add;
        alu_enabled <= '1';
      else
        -- falling clock edge
        register_value_a <= alu_result;
        register_select_a <= 0;
        register_enabled <= '1';
        register_write <= '1';
      end if;
    end if;
  end process execute;

end behavior;
