library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.types.all;

entity processor is

  port (
    reset_in : in std_logic;            -- reset input
    clock_in : in std_logic);           -- clock input

end processor;

architecture behavior of processor is

  constant register_count : integer := 32;

  -- alu
  component alu
    port (
      operand_0, operand_1 : in data_bus;
      result               : out data_bus;
      clk                  : in std_logic;
      opcode               : in alu_opcode);
  end component;

  for alu_0 : alu
    use entity work.alu;

  -- alu signals
  signal alu_operand_0 : data_bus;
  signal alu_operand_1 : data_bus;
  signal alu_result    : data_bus;
  signal alu_opcode    : alu_opcode;
  
  -- register bank
  component registers
    generic (
      register_count : integer range 1 to 64 := register_count);
    port (
      select_a, select_b : in integer range 0 to register_count;
      value_a, value_b   : inout data_bus;
      write              : in std_logic;
      enabled            : in std_logic;
      clock              : in std_logic);
  end component;

  for registers_0: registers use entity work.registers;

  -- register signals
  signal register_select_a, register_select_b : integer range 1 to register_count;
  signal register_value_a, register_value_b   : data_bus;
  signal register_write                       : std_logic;
  signal register_enabled                     : std_logic;

  -- clock signals
  signal clock : std_logic;

begin

  alu_0: alu port map (
    operand_0 => alu_operand_0,
    operand_1 => alu_operand_1,
    result => alu_result,
    opcode => alu_opcode,
    clk => clock);

  registers_0: registers port map (
    select_a => register_select_a,
    select_b => register_select_b,
    value_a  => register_value_a,
    value_b  => register_value_b,
    write    => register_write,
    enabled  => register_enabled,
    clock    => clock);

end behavior;
