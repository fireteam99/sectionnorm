namespace SectionNormalization
{
    using System;
    using System.Collections.Generic;

    public class Normalizer
    {
        private readonly string _manifestPath;

        public Normalizer(string manifestPath)
        {
            this._manifestPath = manifestPath;
        }

        /**
        * reads a manifest file
        * manifest should be a CSV containing the following columns
        * * section_id
        * * section_name
        * * row_id
        * * row_name
        */
        public void ReadManifest()
        {
            // TODO your code goes here
            Console.WriteLine("Reading from " + this._manifestPath);
        }

        /**
        * normalize a single (section, row) input
        * Given a (Section, Row) input, returns (section_id, row_id, valid)
        * where
        * section_id = int or None
        * row_id = int or None
        * valid = True or False
        * Arguments:
        * section {[type]} -- [description]
        * row {[type]} -- [description]
        */
        public NormalizationResult Normalize(string section, string row)
        {
            // initialize return data structure
            var r = new NormalizationResult();
            r.SectionId = -1;
            r.RowId = -1;
            r.Valid = false;

            // TODO your code goes here
            return r;
        }

        public void Normalize(IEnumerable<SampleRecord> samples)
        {
            foreach (var sample in samples)
            {
                var result = this.Normalize(sample.Input.Section, sample.Input.Row);
                sample.Output.SectionId = result.SectionId;
                sample.Output.RowId = result.RowId;
                sample.Output.Valid = result.Valid;
            }
        }
    }
}
