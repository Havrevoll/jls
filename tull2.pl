#!/usr/bin/perl

use warnings;
use strict;
use JSON;

my $mappe = "/";

my %thisFolder = (
    name            => $mappe,
    numberOfFiles   => 0,
    numberOfFolders => 0,
    children        => []
);

$thisFolder{numberOfFiles}++;

push( @{ $thisFolder{children} }, "Archive" );
push( @{ $thisFolder{children} }, "Sync" );
push( @{ $thisFolder{children} }, "Haiss" );

foreach ( keys %thisFolder ) {
    print "$_ bur i $thisFolder{$_}\n";
}

print "i Children er: @{$thisFolder{children}}\n";

my %folders;

$folders{$mappe} = \%thisFolder; 

print "$folders{$mappe} er det og $folders{$mappe}{numberOfFiles} så\n";

$thisFolder{numberOfFiles}++;

print "$folders{$mappe} er det og $folders{$mappe}{numberOfFiles} så\n";

open( my $fh, '>', "tull.txt" )
  or die "Couldn't open for writing: $!\n";

print $fh "Blåbærsyltetøy";

my $perl_scalar = {Namn => "Blåbærsyltetøy"};

my $json_text = JSON->new->encode($perl_scalar);

print $fh $json_text;

close($fh);