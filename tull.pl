#!/usr/bin/perl

use warnings;
use strict;

hei();

sub hei {
open(my $incoming_pipe, '-|', 'ls -l')             or die $!;

my @listing = <$incoming_pipe>;          # Lines from output of ls -l

print $listing[1];
}
