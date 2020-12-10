<?php

namespace SeatGeek;

/**
 * SeatGeek ticket normalizer, it needs to load a manifest first, then
 * normalize a section and row pair input based on that manifest.
 *
 * @package SeatGeek
 */
final class Normalizer
{
    /**
     * reads a manifest file
     *
     * manifest should be a CSV containing the following columns
     * 	* section_id
     * 	* section_name
     * 	* row_id
     * 	* row_name
     *
     * @param string $path_to_manifest
     */
    public function read_manifest(string $path_to_manifest)
    {
        ## your code goes here
    }

    /**
	 * Normalize a single (section, row) input
     *
     *  Given a Section, Row input, returns [section_id, row_id, valid]
     *  where
     *      section_id = int or None
     *      row_id = int or None
     *      valid = True or False
     *
     * @param string $section The section description
     * @param string $row|null The row name
     * @return array
     */
    public function normalize(string $section, string $row = null)
    {
        ## your code goes here
    }
}
