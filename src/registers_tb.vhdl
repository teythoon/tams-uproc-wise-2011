library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.types.all;

entity registers_tb is
end registers_tb;

architecture behavior of registers_tb is

  constant register_count : integer := 32;

  component registers
    generic (
      register_count : integer range 1 to 64 := register_count);
    port (
      select_a, select_b : in integer range 0 to register_count;
      value_a, value_b   : inout data_bus;
      write              : in std_logic;  -- set to 1 to write
      enabled            : in std_logic);  -- set to 1 to enable
  end component;

  for registers_0: registers use entity work.registers;

  signal select_a, select_b : integer range 1 to register_count;
  signal value_a, value_b   : data_bus;
  signal write              : std_logic;
  signal enabled            : std_logic;

  begin
      registers_0: registers port map (
        select_a => select_a,
        select_b => select_b,
        value_a  => value_a,
        value_b  => value_b,
        write    => write,
        enabled  => enabled
      );

      -- purpose: testbench for registers
      -- type   : sequential
      execute_test: process
        type registers_test is record         -- a single test
          select_a, select_b : integer range 0 to register_count;
          value_a, value_b   : data_bus;
        end record;

        type registers_tests is array (natural range <>) of registers_test;
        constant tests : registers_tests :=
          (
            -- TODO: figure out why 0 results in a bounds error
            (1, 2, zero_word, one_word),
            (1, 2, one_word, zero_word),
            (3, 4, two_word, zero_word),
            (1, 2, zero_word, three_word),
            (3, 4, zero_word, zero_word)
          );

      begin  -- process
        for i in tests'range loop
          enabled <= '0';
          wait for 1 ns;

          -- write phase
          select_a <= tests(i).select_a;
          select_b <= tests(i).select_b;
          value_a <= tests(i).value_a;
          value_b <= tests(i).value_b;
          enabled <= '1';
          write <= '1';

          -- generate enabled pulse
          enabled <= '1';
          wait for 1 ns;

          -- prepare for read phase, set bus on high impedance
          value_a <= z_word;
          value_b <= z_word;
          enabled <= '0';
          write <= '0';

          enabled <= '0';
          wait for 1 ns;

          -- read phase
          select_a <= tests(i).select_a;
          select_b <= tests(i).select_b;
          enabled <= '1';

          -- generate enabled pulse
          enabled <= '1';
          wait for 1 ns;

          assert value_a = tests(i).value_a and value_b = tests(i).value_b
            report "bad result" severity error;
        end loop;

        assert false report "end of test" severity note;
        wait;

      end process;
end behavior;
