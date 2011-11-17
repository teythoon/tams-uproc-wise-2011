-- Todo: add missing alu operations and encode opcodes

if(rising_edge(Clk)) then
  case OpCode is
    when "" =>
      Reg1 = Reg1 + Reg2;
    when "" =>
      Reg1 = Reg1 - Reg2;
    when "" =>
      Reg1 = Reg1 * Reg2;
    when "" =>
      Reg1 = Reg1 / Reg2;
    when "" =>
      Reg1 = Reg1 and Reg2;
    when "" => 
      Reg1 = Reg1 or Reg2;
    when "" => 
      Reg1 = Reg1 xor Reg2;
    when "" =>
      Reg1 = not Reg1;
    when others =>
      NULL;
  end case;
end if;
