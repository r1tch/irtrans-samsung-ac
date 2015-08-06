#!/usr/bin/perl -w 
# vim:sw=2:ts=8

use strict;

my $remote = shift || "s";

# -- read a line: <>;


#&learnall();

sub learnall {
  &flag('N');
  &flag('Q');
  &flag('S');
}

sub flag {
  my $flag = shift;
  &fan($flag, 'A');
# auto fan enough for now...
  #&fan($flag, 'L');
  #&fan($flag, 'M');
  #&fan($flag, 'H');
}

sub fan {
  my $flag = shift;
  my $fan = shift;
  &swing($flag, $fan, 'S');
  &swing($flag, $fan, 'N');
}

sub swing {
  my $flag = shift;
  my $fan = shift;
  my $swing = shift;
  &mode($flag, $fan, $swing, 'C');
  &mode($flag, $fan, $swing, 'D');
  #&mode($flag, $fan, $swing, 'F');
  &mode($flag, $fan, $swing, 'H');
  &mode($flag, $fan, $swing, 'A');
}

sub mode {
  my $flag = shift;
  my $fan = shift;
  my $swing = shift;
  my $mode  = shift;
  &learn("$flag$fan$swing$mode", $mode);
}


sub learn {
  my $cmdbase = shift;
  my $mode = shift;

  return if $cmdbase eq "NASC" or $cmdbase eq "NASD";

  print "PRESS BUTTON FOR $cmdbase...\n";
  my $start = 16;
  $start = 18 if ($mode eq "D");


  for (my $i = $start; $i <= 30; ++$i) {
    open(IRCLIENT, "|/usr/local/irtrans/irclient localhost >/dev/null") || die "can't popen irclient: $0";

    print IRCLIENT "2\n";
    sleep .1;
    print IRCLIENT "1\n";
    sleep .1;
    print IRCLIENT "s\n";
    sleep .1;


    print IRCLIENT "4\n";
    sleep .1;
    print IRCLIENT "$cmdbase$i\n";
    sleep .1;
    print IRCLIENT "99\n";
    sleep .1;
    print IRCLIENT "99\n";
    sleep .1;
    close IRCLIENT;
  }
}

learn("NAND", "D");
learn("NANH", "H");
learn("NANA", "A");



print "done\n";
