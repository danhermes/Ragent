# CLI YAMLgen Usage

## Example Commands

```bash
python cli.py --input-file path/to/automate_technical_design.md --tool n8n
python cli.py --input-file path/to/automate_technical_design.md --tool n8n --enhance
```

## CLI Flags

- `--input-file`    Path to input `.md` file
- `--tool`          Target tool (autocoder, n8n, proof, etc.)
- `--output`        (Optional) Output file path
- `--enhance`       (Optional) Call Elias agent
- `--verbose`       (Optional) Verbose mode
