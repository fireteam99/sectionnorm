namespace SectionNormalization
{
    public sealed class SampleRecord
    {
        public SampleInput Input { get; set; }
        public SampleExpected Expected { get; set; }
        public SampleOutput Output { get; set; } = new SampleOutput();
    }

    public class SampleInput 
    {
        public string Section { get; set; }
        public string Row { get; set; }
    }

    public class SampleExpected 
    {
        public int SectionId { get; set; }
        public int RowId { get; set; }
        public bool Valid { get; set; }
    }

    public class SampleOutput 
    {
        public int SectionId { get; set; } = -1;
        public int RowId { get; set; } = -1;
        public bool Valid { get; set; }
    }
}
