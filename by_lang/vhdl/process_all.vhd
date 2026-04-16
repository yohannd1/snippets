-- Simple example of how `process (all)` works.
--
-- It can be used to implement combinatorial processes without worrying about
-- specifying the sensitivity list, like SystemVerilog's `always_comb`. It
-- seems this feature is from VHDL 2008.
--
-- TODO: can it be used for clocked processes? I think so but I'm not sure.

library ieee;
use ieee.std_logic_1164.all;

library std;

entity main is
end entity main;

architecture behavioral of main is
  signal a : integer := 0;
  signal b : integer := 0;
  signal c : bit := '0';
begin
  process
  begin
    a <= 0;
    b <= 10;
    wait for 1 ns;
    report "c = " & to_string(c);
    assert c = '1';

    a <= 5;
    b <= 2;
    wait for 1 ns;
    report "c = " & to_string(c);
    assert c = '0';

    std.env.stop;
    wait;
  end process;

  process (all)
  begin
    -- NOTE: obviously this is quite simple and doesn't need to even be inside
    -- a process, but you get the idea.
    if a < b then
      c <= '1';
    else
      c <= '0';
    end if;
  end process;
end architecture;
