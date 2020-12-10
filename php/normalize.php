#!/usr/bin/php
<?php

require_once 'normalizer.php';

function to_bool($s)
{
    return (bool)preg_match('/^(true|t|yes|y|1)$/i', $s);
}


function read_input($input_path)
{
    $samples = [];
    $file = fopen($input_path, 'r');
    $i = 0;
    while (($line = fgetcsv($file, 1000, ',')) !== FALSE) {
        if ($i === 0) {
            // Table header, skip
            $i++;
            continue;
        }
        $i++;

        [
            $section,
            $row,
            $section_id,
            $row_id,
            $valid
        ] = $line;

        $valid = to_bool($valid);

        $sample = [
            'input' => ['section' => $section, 'row' => $row],
            'expected' => ['section_id' => (int)$section_id, 'row_id' => (int)$row_id, 'valid' => $valid]
        ];

        $samples[] = $sample;
    }
    fclose($file);

    return $samples;
}

function normalize_samples($normalizer, $samples, $verbose = false)
{
    $matched = [];
    foreach ($samples as $sample) {

        $section = $sample['input']['section'];
        $row = $sample['input']['row'];

        [$section_id, $row_id, $valid] = $normalizer->normalize($section, $row);
        $sample['output'] = [
            'section_id' => $section_id,
            'row_id' => $row_id,
            'valid' => $valid
        ];
        $matched[] = $sample;
    }
    return $matched;
}

function output_samples($matched)
{
    foreach ($matched as $match) {
        fwrite(STDOUT, json_encode($match) . PHP_EOL);
    }
}

function main()
{
    $long_opts = [
        'manifest:',
        'input:',
        'section:',
        'row:',
    ];

    $defaults = [
        'input' => null,
        'manifest' => null,
        'row' => null,
        'section' => null,
    ];
    
    $options = getopt(null, $long_opts);
    $options += $defaults;

    if (!($manifest = $options['manifest'] ?? false)) {
        throw new InvalidArgumentException('Missing required argument --manifest');
    }

    $normalizer = new \SeatGeek\Normalizer();
    $normalizer->read_manifest($manifest);

    if ($section = $options['section'] && $row = $options['row']) {
        [$section_id, $row_id, $valid] = $normalizer->normalize($section, $row);
        print 
"Input:
    [section] {$section}
    [row] {$row}
Output:
    [section_id] {$section_id}
    [row_id] {$row_id}
Valid?:
    {$valid}
";
    } elseif ($input = $options['input']) {
        $samples = read_input($input);
        $matched = normalize_samples($normalizer, $samples, false);
        output_samples($matched);
    }
}

main();
