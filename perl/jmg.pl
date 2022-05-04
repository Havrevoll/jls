#!/usr/bin/perl
# jls.pl

use warnings;
use strict;
use JSON;
use utf8;
use Storable;

print "[$_]\n" foreach @ARGV;

#my %folders = ();
#my %files   = ();
#my $teljar  = 0;


my $json;
{
    local $/;    #Enable 'slurp' mode
    open my $fh, "<", "files.json";
    $json = <$fh>;
    close $fh;
}

my $data = decode_json($json);

print 



