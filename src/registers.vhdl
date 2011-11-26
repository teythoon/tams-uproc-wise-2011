library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.types.all;

entity registers is
  
  generic (
    register_count : integer range 1 to 64 := 32);  -- number of registers

  port (
    select_a, select_b : in integer range 0 to register_count;
    value_a, value_b   : inout data_bus;
    write              : in std_logic;   -- set to 1 to write
    enabled            : in std_logic;   -- set to 1 to enable
    clock              : in std_logic);  -- register bank clock is doubled
end registers;

architecture behavior of registers is

  type register_bank_t is array (0 to register_count - 1) of data_bus;  -- a register bank
  
begin  -- behavior
  -- purpose: read and write values
  -- type   : sequential
  -- inputs : clock, select_a, select_b, value_a, value_b, enabled, write
  -- outputs: value_a, value_b
  process (clock)
    variable register_bank : register_bank_t;  -- the register bank
  begin  -- process
    value_a <= z_word;
    value_b <= z_word;

    if clock'event and clock = '1' and enabled = '1' then
      case write is
        when '1' =>
          register_bank(select_a) := value_a;
          register_bank(select_b) := value_b;
        when '0' =>
          value_a <= register_bank(select_a);
          value_b <= register_bank(select_b);
          --value_b <= zero_word;
        when others =>
          null;
      end case;
    end if;
  end process;
end behavior;
