import unittest
import yaml
from pathlib import Path
from yaml_parser import YamlParser
from yaml_generator import YAMLGenerator

class TestYAMLGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(__file__).parent

    def load_yaml(self, path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def test_autocoder_test_framework(self):
        # Load input spec
        input_path = self.test_dir / 'test_framework_spec.yaml'
        parser = YamlParser(input_path)
        spec = parser.load()
        unified_spec = parser.to_unified_spec()

        # Generate YAML
        generator = YAMLGenerator(unified_spec)
        generated = generator.generate_autocoder_yaml()

        # Load expected output
        expected_path = self.test_dir / 'test_framework_expected.yaml'
        expected = self.load_yaml(expected_path)

        # Compare
        self.assertEqual(generated, expected, 
                        "Generated AutoCoder test framework YAML doesn't match expected output")

    def test_autocoder_webapp(self):
        # Load input spec
        input_path = self.test_dir / 'webapp_spec.yaml'
        parser = YamlParser(input_path)
        spec = parser.load()
        unified_spec = parser.to_unified_spec()

        # Generate YAML
        generator = YAMLGenerator(unified_spec)
        generated = generator.generate_autocoder_yaml()

        # Load expected output
        expected_path = self.test_dir / 'webapp_expected.yaml'
        expected = self.load_yaml(expected_path)

        # Compare
        self.assertEqual(generated, expected,
                        "Generated AutoCoder webapp YAML doesn't match expected output")

    def test_litlegos_tech_writing(self):
        # Load input spec
        input_path = self.test_dir / 'tech_writing_spec.yaml'
        parser = YamlParser(input_path)
        spec = parser.load()
        unified_spec = parser.to_unified_spec()

        # Generate YAML
        generator = YAMLGenerator(unified_spec)
        generated = generator.generate_litlegos_yaml()

        # Load expected output
        expected_path = self.test_dir / 'tech_writing_expected.yaml'
        expected = self.load_yaml(expected_path)

        # Compare
        self.assertEqual(generated, expected,
                        "Generated LitLegos tech writing YAML doesn't match expected output")

if __name__ == '__main__':
    unittest.main() 