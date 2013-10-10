#!/usr/bin/perl

@vars = split(/&/, $ENV{'QUERY_STRING'});

for $v (@vars) {
	($key, $val) = split(/=/, $v, 2);
	$val =~ s/[^0-9]//g;
	$var{$key} = $val;
}

if ($ENV{'PATH_INFO'} =~ /^\/([0-9]+)\/([0-9]+)\/([0-9]+)/) {
	$var{'z'} = $1;
	$var{'x'} = $2;
	$var{'y'} = $3;
}

unless ($var{'z'} =~ /^[0-9]+$/ &&
        $var{'x'} =~ /^[0-9]+$/ &&
        $var{'y'} =~ /^[0-9]+$/) {
	print "Content-type: text/html\n\nUnrecognized tile format\n";
	exit 0;
}

print "Content-type: image/png\n\n";

$cache = "/tmp/tile";
$cachefile = "$cache/$var{'z'}/$var{'x'}/$var{'y'}.png";
mkdir "$cache";

if (-f $cachefile) {
	# print STDERR "serve $cachefile from cache\n";
	open(IN, "$cachefile");
	while (<IN>) {
		print;
	}
	close(IN);
	exit(0);
}

#system "/home/enf/datamaps/render /home/enf/shapes/current -g -c FFAA00 $var{'z'} $var{'x'} $var{'y'} | pngquant 64";

open(IN, "/home/enf/datamaps/render -f /home/enf/shapes/current -t 0 -g -c FFAA00 /home/enf/shapes/main $var{'z'} $var{'x'} $var{'y'} | pngquant 64 |");
open(OUT, ">$cache/$$");

$data = "";
while (<IN>) {
	print OUT;
	$data .= $_;
}

close(OUT);
close(IN);

mkdir "$cache/$var{'z'}";
mkdir "$cache/$var{'z'}/$var{'x'}";

chmod(0777, "$cache/$$");
rename("$cache/$$", $cachefile);
# print STDERR "make $cachefile for cache\n";

print $data;
