from ..utils.sample import SampleGenerator

class TestSample:
    def test_space_between(self):
        sample_gen = SampleGenerator(
            stations=6,
            max_passengers=10,
            total_width=500,
            total_height=500,
            space_between=70
        )
        samples = sample_gen.create_samples(100)
        
        for sample in samples:
            for r1, row1 in enumerate(sample):
                for r2, row2 in enumerate(sample):
                    if r1 == r2: continue
                    assert not(row1[1] == row2[1] and row1[2] == row2[2])