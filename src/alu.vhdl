-- Todo: add missing alu operations and encode opcodes

if(rising_edge(Clk)) then
  case OpCode is
    when "" =>
      Reg0 = Reg0 + Reg1;
    when "" =>
      Reg0 = Reg0 - Reg1;
    when "" =>
      Reg0 = Reg0 * Reg1;
    when "" =>
      Reg0 = Reg0 / Reg1;
    when "" =>
      Reg0 = Reg0 and Reg1;
    when "" => 
      Reg0 = Reg0 or  Reg1;
    when "" => 
      Reg0 = Reg0 xor Reg1;
    when "" =>
      Reg0 = not Reg0;
    when others =>
      NULL;
  end case;
end if;
