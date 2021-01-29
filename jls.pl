#!/usr/bin/perl
# jls.pl

use warnings;
use strict;
use JSON;
use utf8;


print "[$_]\n" foreach @ARGV;

my %folders = ();
my %files   = ();
my $teljar  = 0;

jls( $ARGV[0] );

my $json_folders = JSON->new->pretty->encode(\%folders);

my $writefolders = "folders.json";

open( my $fh, '>', $writefolders )
  or die "Couldn't open $writefolders for writing: $!\n";

print $fh $json_folders;

close($fh);

my $writefile = "files.json";

my $json_files = JSON->new->pretty->encode(\%files);

open( $fh, '>', $writefile )
  or die "Couldn't open $writefile for writing: $!\n";

print $fh $json_files;

close($fh);

print "\nTil slutt vart det $teljar mapper.\n";


sub jls {
    $teljar++;
    
    my $mappe = $_[0] || "";
    
    print "$mappe ";

    my %thisFolder = (
        numberOfFiles   => 0,
        numberOfFolders => 0,
        children        => []
    );

    $folders{$mappe} = \%thisFolder;

    open( my $handle, "-|", qq(jotta-cli ls -l "$mappe") );

    my $header = <$handle>;

    my @dashes = split /\s+/, <$handle>;

    my $namelength     = length( $dashes[0] );
    my $sizelength     = length( $dashes[1] );
    my $checksumlength = length( $dashes[2] );
    my $datelength     = length( $dashes[3] );

    while (<$handle>) {

        # print $_;

        if (
/(.{$namelength})\s+(.{$sizelength})\s+(.{$checksumlength})\s+(.{$datelength})/
          )
        {
            

            my $name     = trim($1);
            my $size     = trim($2);
            my $checksum = trim($3);
            my $date     = trim($4);
            
            my $path = $mappe . "/" . $name;

            if ( length($size) == 0 ) {
                print "$name ";

                push( @{ $thisFolder{children} }, $name );
                $thisFolder{numberOfFolders}++;

                jls($path);
            }
            else {
                $thisFolder{numberOfFiles}++;

                push( @{ $files{$checksum} },{
                    name => $name,
                    size => $size,
                    date => $date,
                    path => $path
                } );

            }

        }

    }

    close $handle;

}

sub trim {
    my ($str) = @_;
    $str =~ s/^\s+//;
    $str =~ s/\s+$//;
    $str;
}

#foreach (@result) {
#  if (/^.{30}[drwox]*\t(\d+)$/) {
#    $size += $1;
#  }
#}

