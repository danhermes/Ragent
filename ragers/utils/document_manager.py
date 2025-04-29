import os
import shutil
from datetime import datetime
import logging
from pathlib import Path

# dm = DocumentManager('/projects/project_xyz')
# dm.initialize_project_docs()

# # Later, before a meeting:
# current_charter = dm.inject_document_into_prompt('/projects/project_xyz/charters/code_project_charter.md')

# # After meeting:
# updated_content = "Updated charter after strategy discussion..."
# dm.save_document('/projects/project_xyz/charters/code_project_charter.md', updated_content)
# dm.checkpoint_document('/projects/project_xyz/charters/code_project_charter.md')

class DocumentManager:
    def __init__(self, project_folder, project_type):
        self.logger = logging.getLogger(__name__)
        logging.info(f"Initializing DocumentManager for project at {project_folder}")   
        
        self.project_folder = project_folder
        self.charters_folder = os.path.join(project_folder, 'charters')
        self.deliverables_folder = os.path.join(project_folder, 'deliverables')
        self.meetings_folder = os.path.join(project_folder, 'meetings')

        self.project_type = project_type

        self.ragers_dir = Path(__file__).parent
        self.templates_folder =  self.ragers_dir / ".." / "templates" / self.project_type

    def initialize_project_docs(self):
        """Sets up a new project folder structure and copies templates into place."""
        # os.makedirs(self.charters_folder, exist_ok=True)
        # os.makedirs(self.deliverables_folder, exist_ok=True)
        # os.makedirs(self.meetings_folder, exist_ok=True)
        logging.info(f"Initializing project docs at {self.project_folder}")

        charter_templates = ['code_project_charter.md']
        deliverable_templates = [
            'code_design_meeting.md',
            'code_implementation_meeting.md',
            'code_technical_design.md'
        ]

        for filename in charter_templates:
            shutil.copy(os.path.join(self.templates_folder, filename), self.charters_folder)

        for filename in deliverable_templates:
            shutil.copy(os.path.join(self.templates_folder, filename), self.deliverables_folder)

        self.logger.info(f"Project initialized at {self.project_folder}")

    def load_document(self, doc_path):
        """Loads a document from disk."""
        with open(doc_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        # EMOJI and UNICODE character KILLER
        cleaned_file_content = ''.join(c for c in file_content if c.isascii() or (c.isprintable() and not (0x1F300 <= ord(c) <= 0x1FAFF)))
        return cleaned_file_content

    def save_document(self, doc_path, content):
        """Saves content to a document."""
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def checkpoint_document(self, doc_path):
        """Creates a checkpoint copy of a document with timestamp."""
        base_folder, filename = os.path.split(doc_path)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        checkpoint_name = f"{name}_checkpoint_{timestamp}{ext}"
        checkpoint_path = os.path.join(base_folder, checkpoint_name)
        shutil.copy(doc_path, checkpoint_path)
        print(f"📝 Checkpoint created: {checkpoint_path}")

    def inject_document_into_prompt(self, doc_path):
        """Formats the document for injection into a meeting prompt."""
        content = self.load_document(doc_path)
        return f"\n\n---\n📄 **Current Document State:**\n\n{content}\n\n---\n"

    def list_current_docs(self):
        """Lists all charter and deliverable documents."""
        charters = os.listdir(self.charters_folder)
        deliverables = os.listdir(self.deliverables_folder)
        return {
            "charters": charters,
            "deliverables": deliverables
        }
