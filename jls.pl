#!/usr/bin/perl
# jls.pl

use warnings;
use strict;

print "[$_]\n" foreach @ARGV;

my %folders = ();
my %files =();

jls( $ARGV[0] );


sub jls {
    

    my $mappe = $_[0] || "/";

    my $thisFolder{name} = $mappe;

    $folders{$mappe} = $thisFolder; 
    


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
            
            
            if (length($size) == 0) {
              
              
              print "Namnet er $name og banen er $path og dette er runde $teljar.\n";

              $folders{$folder} = 

              jls($folder);
            }

            
        }

    }

    close $handle;

}

sub trim {
  my($str) = @_;
  $str =~ s/^\s+//;
  $str =~ s/\s+$//;
  $str;
}

#foreach (@result) {
#  if (/^.{30}[drwox]*\t(\d+)$/) {
#    $size += $1;
#  }
#}

