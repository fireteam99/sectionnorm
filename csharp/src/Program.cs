namespace SectionNormalization
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel.DataAnnotations;
    using System.IO;
    using System.Linq;
    using McMaster.Extensions.CommandLineUtils;
    using Newtonsoft.Json;
    using Newtonsoft.Json.Serialization;

    public class Program
    {
        [Required]
        [FileExists]
        [Option("--manifest <MANIFEST>", CommandOptionType.SingleValue)]
        public string Manifest { get; }

        [FileExists]
        [Option("--input <INPUT>", CommandOptionType.SingleValue)]
        public string Input { get; }

        [Option("--section <SECTION>", CommandOptionType.SingleValue)]
        public string Section { get; }

        [Option("--row <ROW>", CommandOptionType.SingleValue)]
        public string Row { get; }

        public static int Main(string[] args)
            => CommandLineApplication.Execute<Program>(args);

        private void OnExecute() 
        {
            var normalizer = new Normalizer(Manifest);
            normalizer.ReadManifest();

            if (!string.IsNullOrEmpty(Input))
            {
                var samples = ReadCSVInput(Input);
                normalizer.Normalize(samples);
                OutputSamples(samples);
            }
            else if (Section != null && Row != null)
            {
                var normalized = normalizer.Normalize(Section, Row);
                Console.WriteLine($"Input:\n    [section] {Section}\t[row] {Row}\nOutput:\n    [section_id] {normalized.SectionId}\t[row_id] {normalized.RowId}\nValid?:\n    {normalized.Valid}");
            }
        }

        private void OutputSamples(IEnumerable<SampleRecord> samples)
        {
            var serializer = new JsonSerializer();

            serializer.ContractResolver = new DefaultContractResolver 
            {
                NamingStrategy = new SnakeCaseNamingStrategy()
            };

            foreach (var sample in samples)
            {
                serializer.Serialize(Console.Out, sample);
                Console.WriteLine();
            }
        }

        private IEnumerable<SampleRecord> ReadCSVInput(string filename)
        {
            return File.ReadAllLines(filename).Skip(1).Select(
                line =>
                {
                    var split = line.Split(',');
                    return new SampleRecord
                    {
                        Input = new SampleInput
                        {
                            Section = split[0],
                            Row = split[1]
                        },
                        Expected = new SampleExpected
                        {
                            SectionId = int.TryParse(split[2], out var section) ? section : -1,
                            RowId = int.TryParse(split[3], out var row) ? row : -1,
                            Valid = bool.Parse(split[4])
                        }
                    };
                });
        }
    }
}
