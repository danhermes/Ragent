🔧 HIGHER-LEVEL FUNCTION LIST
Here’s a rough breakdown of the kinds of modular functions or services you'd write to build a full book-proofing pipeline using LanguageTool (and optionally GPT for finesse):

***  workflow Functions
proof_file_to_file(in_file, out_file)	Full pipeline: reads, proofreads, writes.

***  Proofing Functions
proof_with_languagetool(text)	Uses LanguageTool to check grammar/spelling/style issues.
apply_languagetool_suggestions(text, suggestions)	Rewrites text using LanguageTool's recommendations.
proof_with_chatgpt(text)	Refines or rewrites for tone, clarity, or flow (GPT polishing).
apply_chatgpt_suggestions(text, suggestions)	Rewrites text using ChatGPT's recommendations.

*** Utility / Support Functions
load_book(filepath)	Reads full book text from file or folder (Markdown, DOCX, TXT, etc.).
highlight_issues(text, matches)	Highlights grammar/style problems for review (HTML or Markdown).
custom_dictionary(words)	Adds your terms to LT to avoid false positives.

*** Optional Advanced
run_proof_pipeline(file_path)	End-to-end proofing of a full book file.
generate_annotated_report(text, issues)	PDF/HTML output showing changes, explanations.
interactive_proof_ui()	GUI or CLI where you approve suggestions chunk by chunk.
version_compare(original, edited)	Diffs changes for review or git-style tracking.
