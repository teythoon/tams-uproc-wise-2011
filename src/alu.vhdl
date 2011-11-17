if(rising_edge(Clk)) then
  case OpCode is
    when "000" =>
      Reg1 = Reg1 + Reg2;
    when "001" =>
      Reg1 = Reg1 - Reg2;
    when "010" =>
      Reg1 = Reg1 and Reg2;
    when "011" => 
      Reg1 = Reg1 or Reg2;
    when "100" => 
      Reg1 = Reg1 xor Reg2;
    when "101" =>
      Reg1 = not Reg1;
    when others =>
      NULL;
  end case;
end if;
