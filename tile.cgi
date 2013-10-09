#!/usr/bin/perl

print "Content-type: image/png\n\n";

@vars = split(/&/, $ENV{'QUERY_STRING'});

for $v (@vars) {
	($key, $val) = split(/=/, $v, 2);
	$val =~ s/[^0-9]//g;
	$var{$key} = $val;
}

#system "/home/enf/datamaps/render /home/enf/shapes/current -g -c FFAA00 $var{'z'} $var{'x'} $var{'y'} | pngquant 64";

system "/home/enf/datamaps/render -f /home/enf/shapes/current -t 0 -g -c FFAA00 /home/enf/shapes/main $var{'z'} $var{'x'} $var{'y'} | pngquant 64";
